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
    def __init__(
        self,
        main: "MainApp",
        configTemplate: dict,
        configFPath: str,
        name: str,
        par: object,
        widgetsConnection: list | None = None,
        ui=None,
    ):
        start = time.perf_counter()
        self.par = par
        self.main = main
        self.name = name
        self.ui = ui
        self.widgetsConnection = widgetsConnection
        self.configFPath = configFPath
        self.configBackupDPath = os.path.dirname(configFPath) + "/backup"
        self.configTemplate = configTemplate

        # Configuration for backup management
        self.maxBackupLevels = 3  # Number of backup levels to maintain

        #   Can only be a dictionary
        self.settings: dict = {}

        #   Intervals
        self.saveInterval = 2
        self.currentInterval = 0

        self.loadConfig(self.configFPath)
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def legacy_userTableTransform(self, data: dict) -> dict:
        #   Update userTable to version v1.2 where it became a dictionary containing a list of dictionaries instead of a list of dictionaries
        if isinstance(data, list) and "Users" in self.name:
            self.main.debuggy(f"Transforming legacy userTable format to v1.2 for {self.name}", self.par)
            return {"users": data}
        else:
            return data

    def _getBackupFilePath(self, level: int) -> str:
        """Get the backup file path for a specific backup level."""
        if level < 1 or level > self.maxBackupLevels:
            raise ValueError(f"Backup level must be between 1 and {self.maxBackupLevels}")

        name = Path(self.configFPath).name
        return os.path.join(self.configBackupDPath, f"{name}.bak{level}")

    def _rotateBackups(self):
        try:
            #   Create backup directory
            os.makedirs(self.configBackupDPath, exist_ok=True)

            oldest = self._getBackupFilePath(self.maxBackupLevels)
            if os.path.exists(oldest):
                self.main.safeTrash(oldest)
                self.main.debuggy(f"Removed oldest backup: {oldest}", self.par)

            #   Rotate existing backups
            for level in range(self.maxBackupLevels - 1, 0, -1):
                current = self._getBackupFilePath(level)
                next = self._getBackupFilePath(level + 1)

                if os.path.exists(current):
                    shutil.move(current, next)
                    self.main.debuggy(f"Rotated backup: {current} -> {next}", self.par)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"Error rotating backups: {e}")
            raise

    def _createBackup(self):
        """Create a backup of the current config file."""
        try:
            if not os.path.exists(self.configFPath):
                self.main.debuggy("No config file to backup", self.par)
                return

            #   Validate the current config file
            with open(self.configFPath, "r") as f:
                json.load(f)

            #   Rotate existing backups
            self._rotateBackups()

            path = self._getBackupFilePath(1)
            shutil.copy2(self.configFPath, path)
            self.main.debuggy(f"Created backup: {path}", self.par)

        except json.JSONDecodeError as e:
            self.main.cmd.error(f"Current config file is corrupted, skipping backup: {e}")
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"Error creating backup: {e}")
            raise

    def _writeConfigToFile(self, settings: dict, file_path: str):
        """Safely write configuration to file using temporary file approach."""
        try:
            #   Write to a temporary file first
            temp_dir = os.path.dirname(file_path)
            with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False) as tmp:
                json.dump(settings, tmp, indent=4)
                tmp.flush()
                os.fsync(tmp.fileno())
                tmpFPath = tmp.name

            os.replace(tmpFPath, file_path)
            self.main.debuggy(f"Successfully wrote config to: {file_path}", self.par)

        except Exception as e:
            #   Clean up temp file if it exists
            if "tmpFPath" in locals() and os.path.exists(tmpFPath):
                try:
                    self.main.safeTrash(tmpFPath)
                except:
                    pass
            raise

    def saveConfig(self, overwrite=None, forced=False):
        try:
            self.main.debuggy(f"Saving {self.name} config", self.par)
            self.main.debuggy(f" :{self.currentInterval=}, {self.saveInterval=}, {forced=}, overwrite={overwrite is not None}", self.par)

            #   Overwrite settings if specified
            if overwrite is not None:
                self.settings = overwrite
                settings = overwrite
            else:
                settings = self.settings

            #   Save on interval unless forced
            if not forced and self.currentInterval % self.saveInterval != 0:
                self.main.debuggy("Skipping save due to interval", self.par)
                return

            self._createBackup()
            self._writeConfigToFile(settings, self.configFPath)

            self.main.debuggy(f"Successfully saved {self.name} config", self.par)

        except Exception as e:
            self.main.varHelper.exception(e)
            error_msg = f"Error saving {self.name} config: {e}"
            self.main.cmd.error(f"[{datetime.now()}] {error_msg}")
            self.main.qtHelper.Throw(error_msg)
            raise Exception(f"[{datetime.now()}] {error_msg}")
        finally:
            self.currentInterval += 1
            self.main.debuggy(f"- - - -", self.par)

    def _getAllConfigFilePaths(self) -> list[str]:
        if not os.path.exists(self.configBackupDPath):
            return [self.configFPath]

        paths = [self.configFPath]
        for level in range(1, self.maxBackupLevels + 1):
            path = self._getBackupFilePath(level)
            if os.path.exists(path):
                paths.append(path)

        return paths

    def _mergeMissingFromTemplate(self, config: dict, template: dict) -> bool:
        """Recursively merge missing keys from template into config. Returns True if changes were made"""
        changed = False
        for key, value in template.items():
            if key not in config:
                self.main.debuggy(f"{self.name} config[{key}] <- template[{key}] = '{value}'", "init")
                config[key] = value
                changed = True
            elif isinstance(value, dict) and isinstance(config.get(key), dict):
                if self._mergeMissingFromTemplate(config[key], value):
                    changed = True
        return changed

    def _loadConfigFromFile(self, fPath: str) -> dict:
        """Load and validate configuration from a specific file"""
        if not os.path.exists(fPath):
            raise FileNotFoundError(f"Config file not found: {fPath}")

        with open(fPath, "r") as file:
            config = json.load(file)

        config = self.legacy_userTableTransform(config)

        return config

    def loadConfig(self, configFPath, errored=False):
        """Load configuration with fallback to backups and template merging."""
        try:
            self.main.debuggy(f"Loading {self.name} config from {configFPath}", self.par)

            #   Get all possible config file paths
            files = self._getAllConfigFilePaths()
            self.main.debuggy(f"Config load order: {files}", self.par)

            config = None
            backupLoaded = False

            for attempt, fPath in enumerate(files):
                try:
                    config = self._loadConfigFromFile(fPath)

                    if attempt > 0:
                        backupLoaded = True
                        self.main.cmd.warning(f"[{datetime.now()}] {self.name}: Successfully loaded from backup: {fPath}")
                    else:
                        self.main.debuggy(f"Loaded {self.name} config from main file", self.par)
                    #   Successfully loaded
                    break

                except FileNotFoundError:
                    if attempt == 0:
                        self.main.cmd.info(f"[{datetime.now()}] {self.name}: Main config not found, checking backups")
                    continue

                except (json.JSONDecodeError, Exception) as e:
                    if attempt == 0:
                        self.main.cmd.error(f"[{datetime.now()}] {self.name}: Error reading main config {fPath}: {e}")
                        if len(files) > 1:
                            self.main.cmd.warning(f"[{datetime.now()}] {self.name}: Trying backup files...")
                    else:
                        self.main.cmd.error(f"[{datetime.now()}] {self.name}: Error reading backup {fPath}: {e}")
                    continue

            #   If no config was loaded, use template
            if config is None:
                if errored:
                    error_msg = f"{self.name}: All config files failed to load, cannot continue"
                    self.main.cmd.error(f"[{datetime.now()}] {error_msg}")
                    raise Exception(error_msg)

                self.main.cmd.warning(f"[{datetime.now()}] {self.name}: All files failed, using template config")
                config = {}

            #   Merge missing keys from template
            templateMerged = self._mergeMissingFromTemplate(config, self.configTemplate)

            #   Save the updated config if we loaded from backup or merged template keys
            if (backupLoaded or templateMerged) and not errored:
                try:
                    self.settings = config
                    self.saveConfig(forced=True)
                    self.main.debuggy(f"Saved updated {self.name} config after loading", self.par)
                except Exception as save_error:
                    self.main.cmd.warning(f"Could not save updated config: {save_error}")

            self.settings = config
            self.main.debuggy(f"Successfully loaded {self.name} config with {len(config)} keys", self.par)

            return config

        except Exception as e:
            if not errored:
                self.main.varHelper.exception(e)
                self.main.cmd.error(f"[{datetime.now()}] {self.name}: Error in loadConfig: {e}")
                #   Try again with errored flag to prevent infinite recursion
                return self.loadConfig(configFPath, errored=True)
            else:
                self.main.cmd.error(f"[{datetime.now()}] {self.name}: Critical error loading config: {e}")
                raise

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
        if not self.widgetsConnection:
            return

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
            self.main.qtHelper.Throw(f"Error updating UI from extractor config: {e}")
