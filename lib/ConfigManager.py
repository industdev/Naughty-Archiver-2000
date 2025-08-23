from typing import TYPE_CHECKING

from lib.Enums import Configure, SpecialWidgets

if TYPE_CHECKING:
    from na2000 import MainApp

from pathlib import Path
import tempfile
import time
from datetime import datetime
from PySide6.QtWidgets import QLineEdit, QGroupBox, QCheckBox, QLabel, QComboBox
import os
import json
import shutil


class Config:
    def __init__(self, main: "MainApp", widgetsConnection: list, configTemplate: dict, configFPath: str, extname: str, ui=None):
        start = time.perf_counter()
        self.main = main
        self.name = extname
        self.ui = ui
        self.widgetsConnection = widgetsConnection
        self.configFPath = configFPath
        self.configBackupFPath = self.configFPath + ".bak"
        self.configTemplate = configTemplate
        self.settings = {}
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

        self.loadConfig(self.configFPath)

    def saveConfig(self):
        self.main.cmd.info(f"[{datetime.now()}] ExtractorConfigurator::saveConfig -> {self.name}")
        try:
            #   Backup existing config
            if os.path.exists(self.configFPath):
                bak = self.configFPath + ".bak"

                #   Validate
                with open(self.configFPath, "r") as f:
                    json.load(f)

                shutil.copy2(self.configFPath, bak)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"[{datetime.now()}] Error validating or backing up config: {e}")

        try:
            #   Write to a temporary file first
            with tempfile.NamedTemporaryFile("w", dir=os.path.dirname(self.configFPath), delete=False) as tmp:
                json.dump(self.settings, tmp, indent=4)
                tmp.flush()
                os.fsync(tmp.fileno())

            #   Replace
            os.replace(tmp.name, self.configFPath)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"[{datetime.now()}] Error saving config: {e}")
            raise Exception(f"[{datetime.now()}] Error saving config: {e}")

    def loadConfig(self, configFPath, errored=False):
        #   Adds missing keys on base based on template
        def _mergeMissing(base, template):
            changed = False
            for key, value in template.items():
                if key not in base:
                    self.main.debuggy(f"[{datetime.now()}] {self.name} config[{key}] <- template[{key}] = '{value}'", "init")
                    base[key] = value
                    changed = True
                elif isinstance(value, dict) and isinstance(base.get(key), dict):
                    if _mergeMissing(base[key], value):
                        changed = True
            return changed

        templateConfig = self.configTemplate

        try:
            if os.path.exists(configFPath):
                with open(configFPath, "r") as file:
                    config = json.load(file)
            else:
                self.main.cmd.info(f"[{datetime.now()}] Loading config template")
                config = {}

            changed = _mergeMissing(config, templateConfig)
            self.settings = config

            if errored and changed:
                try:
                    self.saveConfig()
                except Exception:
                    pass

        except Exception as e:
            self.main.varHelper.exception(e)
            if errored:
                self.main.cmd.error(f"[{datetime.now()}] {self.name}: There was an error reading {configFPath}: {e}")
                raise Exception(f"{self.name}: Couldn't load config backup or template {e}")

            self.main.cmd.error(f"[{datetime.now()}] {self.name}: There was an error reading {configFPath}: {e}")
            self.main.cmd.warning(f"[{datetime.now()}] {self.name}: Retrying with backup: {self.configBackupFPath}")
            self.loadConfig(self.configBackupFPath, True)

    def _pathToCookiesFilename(self, path):
        try:
            if path == "":
                return "No cookie is selected"
            if Path(path).exists():
                return "Selected cookies: " + Path(path).stem
            else:
                return "No cookie is selected"
        except (OSError, RuntimeError):
            return "No cookie is selected"

    def _enabledExtractorText(self, enabled):
        if enabled:
            return f"{self.name} Settings"
        else:
            return f"{self.name} Settings (Disabled)"

    def updateUI(self):
        try:
            tab = self.ui
            keyCount = 0

            for conn in self.widgetsConnection:
                name = conn.get(Configure.WIDGET)
                widget = getattr(tab, name)
                key = conn.get(Configure.KEY)
                validation = conn.get(Configure.VALIDATION)

                #   Normal Widgets
                if key == None:
                    continue
                keyCount += 1

                self.main.debuggy(f" :{name} <- {key}", self)

                value = self.settings[f"{key}"]
                title = ""
                #   Special widgets
                if validation == SpecialWidgets.EXT_COOKIESLABEL:
                    value = self._pathToCookiesFilename(value)
                if validation == SpecialWidgets.EXT_GRPBOX:
                    title = self._enabledExtractorText(value)

                widget.blockSignals(True)
                if isinstance(widget, QGroupBox):
                    widget.setTitle(str(title))
                    widget.setChecked(bool(value))
                if isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QLabel):
                    widget.setText(str(value))
                elif isinstance(widget, QComboBox):
                    widget.setCurrentIndex(int(value))
                widget.blockSignals(False)

            self.main.tray.refreshMenu()
            self.main.cmd.info(f" :Loaded {keyCount} keys")

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"Error updating UI from extractor config: {e}", logger=self.main.General.logger)
