import multiprocessing
import time
import subprocess
import psutil
import sys
from datetime import datetime
from pathlib import Path


class CrashHelper:
    def __init__(self, mainPid: int, title: str, logPath: str, logger):
        super().__init__()
        start = time.perf_counter()

        self.mainPid = mainPid
        self.title = title
        self.logPath = logPath
        self.check_interval = 3
        self.process = None

        #   Use multiprocessing primitives
        self.event_stop = multiprocessing.Event()
        self.pidList = multiprocessing.Manager().list()

        Path(logPath).mkdir(parents=True, exist_ok=True)
        self.start()
        logger.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def start(self):
        if self.process and self.process.is_alive():
            self._log(f"Crash monitor already running")
            return

        self.process = multiprocessing.Process(
            target=self._monitor,
            args=(self.mainPid, self.title, self.logPath, self.event_stop, self.pidList),
            daemon=False,
        )
        self.process.start()
        self._log(f"Crash monitor started as PID: {self.process.pid}")

    def stop(self):
        if self.process and self.process.is_alive():
            self.event_stop.set()
            self.process.join(timeout=5)

            if self.process.is_alive():
                self.process.kill()
                self.process.join()

        self._log(f"Crash monitor stopped")

    def register(self, process):
        pid = process.pid if hasattr(process, "pid") else process
        self.pidList.append(pid)
        self._log(f"Registered subprocess PID: {pid}")

    def unregister(self, pid):
        if pid in self.pidList:
            self.pidList.remove(pid)
            self._log(f"Unregistered subprocess PID: {pid}")

    def _log(self, message):
        file = Path(self.logPath) / "CrashHandler.log"
        try:
            with open(file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] {message}\n")
        except Exception:
            pass

    def _monitor(self, mainPid, title, logPath, event_stop, pidList):
        file = Path(logPath) / "CrashHandler.log"

        def log(message):
            try:
                with open(file, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] {message}\n")
                    f.flush()
            except Exception:
                pass

        log(f"Crash monitor process started, monitoring PID: {mainPid}")

        while not event_stop.is_set():
            try:
                if not psutil.pid_exists(mainPid):
                    log(f"Main PID {mainPid} no longer exists")
                    CrashHelper._handleCrash(title, logPath, list(pidList), log)
                    break

                time.sleep(3)

            except Exception as e:
                log(f"Monitor error: {e}")
                time.sleep(3)

        log(f"Crash monitor process ending")

    @staticmethod
    def _handleCrash(title, logPath, monitored_pids, log_func):
        try:
            #   Cleanup processes
            count = 0
            log_func(f"Cleaning up {len(monitored_pids)} processes...")

            for pid in monitored_pids:
                try:
                    if psutil.pid_exists(pid):
                        subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, capture_output=True)
                        count += 1
                except Exception as e:
                    log_func(f"Could not kill PID {pid}: {e}")

            log_func(f"Cleanup complete. Killed {count} processes.")

            #   Show notification
            crash_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cmd = f'start cmd /k "echo {title} crashed at {crash_time} && echo Check logs in {logPath} && pause"'
            subprocess.Popen(cmd, shell=True)

            #   Log crash report
            with open(Path(logPath) / "CrashHandler.log", "a", encoding="utf-8") as f:
                f.write(f"Crash Time: {crash_time}\n")
                f.write(f"Monitored PIDs: {monitored_pids}\n")
                f.write(f"Python Version: {sys.version}\n")

        except Exception as e:
            log_func(f"Error handling crash: {e}")
