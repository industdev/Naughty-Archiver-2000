from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.ExtractorLogger import ExtractorLogger
    from lib.Extractor import Extractor
    from lib.RunnerManager import RunnerManager

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


class FileCreationHandler(FileSystemEventHandler):
    def __init__(self, logger: "ExtractorLogger", main: "MainApp", fileMonitor: "ExtractorFileMonitor", extractor: "Extractor"):
        self.main = main
        self.inv = self.main._inv
        self.extractor = extractor

        self.cwd = fileMonitor.watchPath
        self.logger = logger
        self.processedFiles = set()
        self.skipExt = (".sql-journal", ".part", ".tmp", ".aria2__temp", ".aria2")
        self.mediaExt = (".png", ".jpg", ".mp4", ".mov", ".jpeg", ".gif", ".wepb")
        self.metadataExt = (".json", ".sql", ".txt", ".html", ".js")
        super().__init__()

    def getRelativePath(self, filePath: str) -> str:
        try:
            watchPath = os.path.abspath(self.cwd)
            filePath = os.path.abspath(filePath)

            #   Folder name of watchPath itself
            watchFolder = os.path.basename(os.path.normpath(watchPath))

            #   Relative path of file to the watchPath
            relativePath = os.path.relpath(filePath, watchPath)

            fullRelativePath = os.path.join(watchFolder, relativePath)
            return f"\\{fullRelativePath}"

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"Error getting relative path in FileCreationHandler: {e}")
            return os.path.basename(filePath)

    def processFile(self, filePath):
        filename = os.path.basename(filePath)
        filenameLow = filename.lower()
        relativePath = self.getRelativePath(filePath)

        if filenameLow.endswith(self.skipExt):
            return False

        if filePath in self.processedFiles:
            return False

        self.processedFiles.add(filePath)

        if filenameLow.endswith(self.metadataExt):
            self.increaseSizeCounter(filePath, "totMetadataSize", 1)
            self.inv(lambda: self.main.stats.counter.increase(1, "totMetadataAmount"))
            self.inv(lambda: self.main.dataHelper.log(f"[0]{self.extractor.name}{relativePath}"))

        elif filenameLow.endswith(self.mediaExt):
            self.increaseSizeCounter(filePath, "totMediaSize", 5)
            self.inv(lambda: self.main.stats.counter.increase(1, "totMediaAmount"))
            self.inv(lambda: self.main.dataHelper.log(f"[1]{self.extractor.name}{relativePath}"))

        self.inv(lambda f=filename: self.logger.success(f"[+] {f}"))
        return True

    def on_created(self, event):
        if event.is_directory:
            return

        self.processFile(event.src_path)

    def on_moved(self, event):
        if event.src_path in self.processedFiles:
            self.processedFiles.add(event.dest_path)
            return

        self.processFile(event.dest_path)

    def increaseSizeCounter(self, filePath, counterType, sleepms=5):
        def _monitorFileSize():
            try:
                #   Initial delay
                time.sleep(sleepms)

                if not os.path.exists(filePath) or not os.path.isfile(filePath):
                    self.inv(lambda: self.logger.debug(f"File not found or not accessible: {filePath}"))
                    return

                previous_size = -1
                cSize = os.path.getsize(filePath)
                sizeTimesStable = 0
                max_attempts = 12
                attempt = 0

                while previous_size != cSize and attempt < max_attempts:
                    previous_size = cSize
                    time.sleep(5)

                    if not os.path.exists(filePath):
                        self.inv(lambda: self.logger.debug(f"File disappeared during monitoring: {filePath}"))
                        return

                    cSize = os.path.getsize(filePath)
                    attempt += 1

                    #   If size hasn't changed
                    if previous_size == cSize:
                        sizeTimesStable += 1
                    else:
                        sizeTimesStable = 0

                    #   If size is stable for two consecutive checks, consider it done
                    if sizeTimesStable >= 2:
                        break

                if attempt >= max_attempts:
                    self.inv(lambda: self.logger.debug(f"File size monitoring timed out for {filePath} after {max_attempts * 5} seconds"))

                #    Update
                self.inv(lambda c=cSize: self.main.stats.counter.increase(c, counterType))

                self.main.debuggy(f"{counterType}+={cSize} ({attempt} checks) for ({filePath})", self)

            except Exception as e:
                self.inv(lambda e=e: self.logger.alert(f"Error measuring file size for {filePath}: {str(e)}"))

        #   Start monitoring in a separate thread
        monitoringThread = threading.Thread(target=_monitorFileSize)
        monitoringThread.daemon = True
        monitoringThread.start()


class ExtractorFileMonitor:
    def __init__(self, main: "MainApp", extractor: "Extractor", runnerManager: "RunnerManager", watchPath="."):
        start = time.perf_counter()
        self.main = main
        self.inv = self.main._inv

        self.logger = extractor.logger
        self.watchPath = os.path.abspath(watchPath)
        self.observer = Observer()
        self.thread = None
        self.isRunning = False
        self.galleryRunner = runnerManager
        self.event_handler = FileCreationHandler(self.logger, self.main, self, extractor)
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def start(self):
        if self.isRunning:
            self.inv(lambda: self.logger.debug("File monitor already running"))
            return

        try:
            self.observer.schedule(self.event_handler, self.watchPath, recursive=True)
            self.thread = threading.Thread(target=self._runObserver)
            self.thread.daemon = True
            self.isRunning = True
            self.inv(lambda: self.logger.debug("File monitor started"))

            self.thread.start()

        except Exception as e:
            self.inv(lambda e=e: self.logger.error(f"Failed to start monitoring: {str(e)}"))

    def stop(self):
        if not self.isRunning:
            self.inv(lambda: self.logger.debug("File monitor already stopped"))
            return

        try:
            #   Break the loop in observer
            self.isRunning = False
            if self.observer.is_alive():
                self.observer.stop()
                self.observer.join()
            self.inv(lambda: self.logger.debug("File monitor stopped"))
        except Exception as e:
            self.stopGalleryrunner(f"Error stopping monitor: {e}", False)

    def stopGalleryrunner(self, errorText, clear=True):
        self.inv(lambda e=errorText: self.logger.error(f"Stopping from FileMonitor: {e}"))
        self.main.cmd.error(f"Stopping from FileMonitor: {errorText}")
        self.galleryRunner._stop(f"Stopping from FileMonitor: {errorText}")
        self.stop()
        if clear:
            self.event_handler.processedFiles.clear()

    #   Change the directory being monitored
    def changeDir(self, newPath):
        try:
            newPath = os.path.abspath(newPath)

            if not os.path.exists(newPath):
                self.inv(lambda: self.logger.alert(f"Creating directory: {newPath}"))
                try:
                    os.makedirs(newPath, exist_ok=True)
                except Exception as e:
                    self.main.varHelper.exception(e)
                    self.stopGalleryrunner(f"Failed to create directory: {newPath}; {str(e)}")
                    return

            self.event_handler.processedFiles.clear()
            pastRunning = self.isRunning

            if pastRunning:
                self.stop()

            self.watchPath = newPath
            self.event_handler.cwd = newPath
            self.inv(lambda: self.logger.success(f"Working dir: {self.watchPath}"))
            if pastRunning:
                self.start()
        except Exception as e:
            self.inv(lambda e=e: self.logger.error(f"Error switching dir to {self.watchPath}: {e}"))

    #   Run the observer in a separate thread
    #   Always create a new Observer if the previous one is not alive
    def _runObserver(self):
        try:
            if not self.observer.is_alive():
                self.observer = Observer()
                self.observer.schedule(self.event_handler, self.watchPath, recursive=True)
                self.observer.start()
            while self.isRunning:
                time.sleep(1)
        except Exception as e:
            self.inv(lambda e=e: self.logger.error(f"Observer error: {str(e)}"))
        finally:
            if self.observer.is_alive():
                self.observer.stop()
                self.observer.join()
