from typing import TYPE_CHECKING

from lib.Enums import Return

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor, ExtractorEntry

import subprocess
import time
import threading
from threading import Lock
import psutil
from lib.QtHelper import QtHelper
from lib.GalleryOutputHandler import GalleryOutputHandler


class GalleryRunner:
    def __init__(self, main: "MainApp", extractor: "Extractor"):
        start = time.perf_counter()
        self.main = main
        self.inv = main._inv

        self.extractor = extractor

        self.event_loopStop = extractor.event_loopStop
        self.generalLogger = extractor.generalLogger

        self.process = None
        self.running = False
        self.stopReason = None

        #   Output settings
        self.batchSize = 100
        self.batchTimeout = 0.02  #  Seconds

        self._batch = []
        self._batchLock = Lock()
        self._last_flush = time.monotonic()
        self._flushTimer = None

        self.debugTextTest = None
        self.lineCount = 0

        self.reloadPatterns = False

        if extractor.errorLister.errorListEnabled:
            errorLogger = extractor.errorLister.runnerSettings
        else:
            errorLogger = None

        self.lineChanger = GalleryOutputHandler(
            main, self, self.main.General.config.settings["errorboxes"], errorLogger, self.main.General.config.settings["stoptrigger"]
        )
        self.main.cmd.debug(f" :{__name__}::__init__ ->{(time.perf_counter() - start) * 1000:.6f}ms")

    def _startFlushTimer(self):
        """Start the periodic flush timer"""
        if self._flushTimer is not None:
            self._flushTimer.cancel()

        self._flushTimer = threading.Timer(self.batchTimeout, self._flusher)
        self._flushTimer.daemon = True
        self._flushTimer.start()

    def _flusher(self):
        """Flush batch when timer expires"""
        with self._batchLock:
            current_time = time.monotonic()
            if self._batch and current_time - self._last_flush >= self.batchTimeout:
                self.__flush(self._batch.copy())
                self._batch.clear()
                self._last_flush = current_time

        # Restart timer if still running
        if self.running:
            self._startFlushTimer()

    def _processOutput(self, stream):
        try:
            self._startFlushTimer()

            # Process lines from stream
            for raw in iter(stream.readline, b""):
                if not self.running:
                    break

                if stream.closed:
                    break

                line = raw.decode("utf-8", errors="replace").strip()

                if not line:
                    continue

                self.lineCount += 1

                #   Debug
                if self.lineCount % 10 == 0 and self.debugTextTest:
                    line = self.debugTextTest
                    self.main.debuggy(self.lineChanger.levelChanger(line), self)

                level = self.lineChanger.levelChanger(line)
                if level:
                    with self._batchLock:
                        self._batch.append((line, level))
                        current_time = time.monotonic()

                        #   Flush if batch is full
                        if len(self._batch) >= self.batchSize:
                            self.__flush(self._batch.copy())
                            self._batch.clear()
                            self._last_flush = current_time

            #   Final flush of remaining items
            with self._batchLock:
                if self._batch:
                    self.__flush(self._batch.copy())
                    self._batch.clear()

        except (ValueError, OSError, IOError) as e:
            if not stream.closed and self.running:
                self.inv(lambda e=e: self.extractor.logger.warning(f"GalleryRunner::_process_output -> Stream read error: {e}"))
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.extractor.logger.error(f"GalleryRunner::_process_output -> Unexpected error: {e}"))
        finally:
            if self._flushTimer is not None:
                self._flushTimer.cancel()
                self._flushTimer = None

    def __flush(self, batch):
        if not batch:
            return

        def log():
            for line, level in batch:
                self.extractor.logger.log(line, level)

        self.inv(log)

    def run(self, exePath, args, cwd, timeout=None) -> tuple[bool, str | Return]:
        self.inv(
            lambda r=self.running, s=self.stopReason, v=self.reloadPatterns: self.extractor.logger.debug(
                f"GalleryRunner::run -> running: {r}, stopReason: {s}, reloadPatterns: {v}"
            )
        )
        try:
            if self.reloadPatterns:
                self.lineChanger.reloadPatterns()
                self.reloadPatterns = False
            self._reset()

            #   Start
            command = f'"{exePath}" {args}'
            self.running = True
            self.inv(lambda c=command: self.generalLogger.debug(f"Starting: {c}"))

            self.process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, universal_newlines=False, shell=True
            )
            pid = self.process.pid
            #   Register for crash handling
            self.inv(lambda p=pid: self.extractor.logger.debug(f"Register PID {p}"))
            self.inv(lambda p=pid: self.main.crashHelper.register(p))
            self.stopByOutput = False

            #   Output-reading threads
            out_thread = threading.Thread(target=self._processOutput, args=(self.process.stdout,))
            err_thread = threading.Thread(target=self._processOutput, args=(self.process.stderr,))
            out_thread.daemon = err_thread.daemon = True
            out_thread.start()
            err_thread.start()

            start_time = time.monotonic()

            #   Monitor loop
            while self.running:
                if self.process.poll() is not None:
                    break
                if timeout and (time.monotonic() - start_time) > timeout:
                    self.stopReason = f"Timeout after {timeout}s"
                    self.running = False
                    break
                time.sleep(0.2)

            self.inv(lambda p=pid: self.extractor.logger.debug(f"Unregister PID {p}"))
            self.inv(lambda p=pid: self.main.crashHelper.unregister(p))

            self._terminateProcess()
            out_thread.join(timeout=2)
            err_thread.join(timeout=2)
            if out_thread.is_alive():
                self.inv(lambda: self.extractor.logger.error("stdout thread failed to exit"))
            if err_thread.is_alive():
                self.inv(lambda: self.extractor.logger.error("stderr thread failed to exit"))

            code = self.process.returncode
            if code == 0 and not self.stopReason:
                return True, Return.SUCCESS
            if code != 0:
                if code == 3221225595:
                    self.stopReason = "Download Visual C++ Redistributable at aka.ms/vs/17/release/vc_redist.x86.exe"
                elif code == 2:
                    self.stopReason = "File not found. Check paths"
                elif code == 126:
                    self.stopReason = "Cannot execute the file. Check permissions or format"
                elif code == 3221225477:
                    self.stopReason = "Segmentation fault"
                elif code == 3221225781:
                    self.stopReason = "DLL not found. You may need to install the Microsoft Visual C++ Redistributable"
                elif code == 3221225794:
                    self.stopReason = "DLL initialization failed. The program couldn't start properly"
                elif code == 3221226505:
                    self.stopReason = "Stack buffer overrun. Security issue or corrupted program"
                elif code == -1073741510:
                    self.stopReason = "Gallery-dl process terminated by user"

                msg = self.stopReason or Return.ERR_GALLERY_CODE1
                return False, msg

            return False, self.stopReason if self.stopReason is not None else Return.ERR_GALLERY_GENERAL

        except Exception as e:
            self.inv(lambda e=e: self.extractor.logger.error(f"Failed to run extraction: {e}"))
            return False, str(e)
        finally:
            if self.main.debug:
                self.inv(lambda: self.extractor.logger.debug(f"GalleryRunner::run -> return"))
            self._stopFlushTimer()
            self.running = False
            self.lineChanger.newRun()

    def _stopFlushTimer(self):
        """Stop the flush timer and perform final flush"""
        if self._flushTimer is not None:
            self._flushTimer.cancel()
            self._flushTimer = None

        with self._batchLock:
            if self._batch:
                self.__flush(self._batch.copy())
                self._batch.clear()

    def _stop(self, reason=None):
        self.inv(lambda r=self.running: self.extractor.logger.debug(f"GalleryRunner::_stop -> {reason} running:{r}"))
        if reason:
            self.stopReason = reason
        self.running = False
        self._stopFlushTimer()
        self.event_loopStop.set()

    #   Button is pressed or tray
    def forceStop(self):
        self._stop(Return.FORCE_TERMINATED)

    def skip(self):
        self._stop(Return.JOB_SKIPPED)

    def skipUser(self):
        self._stop(Return.USER_SKIPPED)

    def _terminateProcess(self):
        if not self.process:
            return

        try:
            self.inv(lambda: self.extractor.logger.debug("GalleryRunner::_terminateProcess"))
            pid = self.process.pid

            if self.process.poll() is not None:
                self.inv(lambda: self.extractor.logger.debug("Process already terminated"))
                return

            #   Kill process
            self._killProcessTree(pid)

            #   Force kill if still running
            if self.process.poll() is None:
                try:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True, timeout=5)
                    try:
                        self.process.wait(timeout=5)
                        if self.main.debug:
                            self.inv(lambda: self.extractor.logger.debug("Process force-killed successfully"))
                    except subprocess.TimeoutExpired:
                        self.inv(lambda: self.extractor.logger.error("Process did not terminate after force kill"))

                except Exception as e:
                    self.main.varHelper.exception(e)
                    self.inv(lambda e=e: self.extractor.logger.error(f"Taskkill failed: {e}"))

        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.extractor.logger.error(f"Error in GalleryRunner::_terminateProcess {e}"))
        finally:
            self._closeStreams()

    def _killProcessTree(self, pid):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            parent.terminate()
        except Exception as e:
            self.inv(lambda e=e: self.extractor.logger.debug(f"GallerRunner::_killProcessTree -> Process tree termination failed: {e}"))
            raise

    def _closeStreams(self):
        try:
            if self.process:
                if self.process.stdout and not self.process.stdout.closed:
                    self.process.stdout.close()
                if self.process.stderr and not self.process.stderr.closed:
                    self.process.stderr.close()
        except Exception as e:
            self.inv(lambda e=e: self.extractor.logger.debug(f"Stream cleanup error: {e}"))

    def _reset(self):
        self.stopReason = None
        self.running = False
        self.lineCount = 0
        self.event_loopStop.clear()
        self._stopFlushTimer()
        #   Clear batch
        with self._batchLock:
            self._batch.clear()
        try:
            self._terminateProcess()
        except:
            pass
        self.process = None
