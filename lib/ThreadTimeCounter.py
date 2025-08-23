from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp

import threading
import time
from datetime import datetime


class ThreadTimeCounter:
    def __init__(self, main: "MainApp"):
        start = time.perf_counter()
        self.main = main
        self.inv = main._inv
        self.counter = main.stats.counter
        self.activeThreads = 0
        self.lock = threading.Lock()
        self.running = True
        self.sleepTime = 1

        #   Hour tracking variables
        self.hours = 0
        self.secondsCounter = 0
        self.currentSecretIndex = 0
        self.thread = threading.Thread(target=self.startCounter, name="timeCounterThread", daemon=True)

        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def extRunning(self):
        with self.lock:
            self.activeThreads += 1

    def extStopped(self):
        with self.lock:
            self.activeThreads = max(0, self.activeThreads - 1)

    def updateDrawing(self, value):
        self.inv(lambda: self.main.stats.counter.updateDrawing(value))

    def startCounter(self):
        while self.running:
            time.sleep(self.sleepTime)
            with self.lock:
                self.secondsCounter += self.sleepTime

                #   Stat increase every second only when extractors are on
                if self.activeThreads > 0:
                    self.inv(lambda: self.counter.increase(1, "totExtractorsRuntime", False))

                #   Refresh image
                if self.main.General.config.settings["supersecretoption"]:
                    if self.secondsCounter in {3600, 10800, 21600, 43200, 86400, 172800}:
                        value = int(self.secondsCounter / 3600)
                        self.updateDrawing(value)

                #   Remove exceeding log entries every 10 seconds
                if self.secondsCounter % 10 == 0:
                    self.inv(lambda: self.main.extractorsManager.trimLogs())

                #   Reset QtHelper error boxes counter every 60 seconds
                if self.secondsCounter % 60 == 0:
                    self.main.debuggy("Reset all extractors error counter", self)
                    self.inv(lambda: self.main.extractorsManager.resetExtractorsErrorsPerMinute())

    def stop(self):
        self.main.cmd.info(f"[{datetime.now()}] Stopping time counter...")
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
