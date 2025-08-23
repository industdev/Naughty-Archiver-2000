from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp

import logging
import os
import base64
import json
from datetime import datetime
import uuid
import time


class GlobaldataHelper:
    def __init__(self, main: "MainApp"):
        start = time.perf_counter()
        self.main = main
        self.inv = main._inv

        self.logPath = f"{self.main.logPath}/ExtractionData.data"
        self.dataLogger = logging.getLogger("GlobalDataHelper")
        self.initLogger()
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def initLogger(self):
        #   GlobalDataHelper Logger
        self.dataLogger.setLevel(logging.DEBUG)

        self.dataLogger.handlers.clear()
        self.dataLogger.propagate = False
        handler = logging.FileHandler(self.logPath, encoding="utf-8")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.dataLogger.addHandler(handler)

        self._logInit()

    def _logInit(self):
        if self.main.General.config.settings["uuid"] is None:
            ArchiverUUID = str(uuid.uuid4())
            self.main.General.config.settings["uuid"] = ArchiverUUID
            self.dataLogger.info(f"Archiver: {self.main.General.config.settings['uuid']} at {datetime.now()}")

    def log(self, text: str):
        self.dataLogger.info(text)

    def stop(self):
        self.main.cmd.info(f"[{datetime.now()}] Stopping datahelper...")
        try:
            _statsJson = self.main.stats.counter.config.settings
            _statsJsonString = json.dumps(_statsJson)
            _bytes = base64.b64encode(_statsJsonString.encode("utf-8"))
            stats = _bytes.decode("ascii")

            statString = f"Stats:{stats}"
            self.log(statString)
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"Error writing stats to .data file: {e}")
