from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from na2000 import MainApp

import os
import time

from lib.Extractor import Extractor, ExtractorEntry
from lib.QtHelper import QtHelper
from PySide6.QtWidgets import QMessageBox
from datetime import datetime

from lib.extractors.pixiv import Pixiv
from lib.extractors.kemono import Kemono
from lib.extractors.furaffinity import Furaffinity
from lib.extractors.inkbunny import Inkbunny
from lib.extractors.itaku import Itaku
from lib.extractors.twitter import Twitter
from lib.extractors.bluesky import Bluesky


class ExtractorsManager:
    def __init__(self, main: "MainApp", safeTrash: Callable):
        start = time.perf_counter()

        self.main = main
        self.inv = self.main._inv

        self.generalLogger = main.General.logger
        self.safeTrash = safeTrash
        self.activeExtractors = {}

        #   Define all available extractor types with their constructors
        #   Each entry maps extractor name to its tab wrapper constructor
        #   Store the constructor as a lambda function, pass 'id' as parameter
        #   The extractor class requires the extractor settings (imported above), the main class, and an id
        try:
            self.extractorFactories = {
                "Twitter": lambda id: Extractor(Twitter(), main, id),
                "Bluesky": lambda id: Extractor(Bluesky(), main, id),
                "Pixiv": lambda id: Extractor(Pixiv(), main, id),
                "Kemonoparty": lambda id: Extractor(Kemono(), main, id),
                "Furaffinity": lambda id: Extractor(Furaffinity(), main, id),
                "Inkbunny": lambda id: Extractor(Inkbunny(), main, id),
                "Itaku": lambda id: Extractor(Itaku(), main, id),
            }
            #   You are done!
        except Exception:
            raise

        self.availableExtractors = list(self.extractorFactories.keys())
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def _generateExtractorId(self):
        existing = set()

        #   Check in activeExtractors
        existing.update(self.activeExtractors.keys())

        #   Check in config
        for ext in self.main.General.config.settings["extractors"]:
            existing.add(int(ext["id"]))

        #   Find the next available number starting from 0
        counter = 0
        while counter in existing:
            counter += 1

        return counter

    def startExtractors(self):
        self.generalLogger.info("- - - Starting new extraction process - - -")

        #   Start each enabled extractor
        for entry in self.main._getExtractors(False):
            isEnabled = entry.enabled
            extractor = entry.ext

            if isEnabled and not extractor.galleryRunner.running:
                extractor.logger.debug("Requested start")
                extractor.startExtraction()

    def setOutputHandlerReloadingFlag(self):
        self.generalLogger.info("Refreshing all extractor's output handlers patterns on next run")
        for entry in self.main._getExtractors(False):
            extractor = entry.ext
            extractor.galleryRunner.reloadPatterns = True

    def stopProcedure(self):
        self.stopExtractors()
        self.closeExtractorsUi()
        self.saveConfigs()

    def stopExtractors(self):
        self.generalLogger.info("Stopping all extractors...")
        for entry in self.main._getExtractors(False):
            extractor = entry.ext
            extractor.stop()
            extractor.users.discardClose()
            self.main.General.logger.info(f"Stopped: {extractor.configName}")

    def resetExtractorsErrorsPerMinute(self):
        for entry in self.main._getExtractors(False):
            extractor: "Extractor" = entry.ext
            extractor.galleryRunner.lineChanger.errorCounter = 0

    def closeExtractorsUi(self):
        self.generalLogger.debug(f"Closing and saving extractors UI...")
        for entry in self.main._getExtractors(False):
            extractor = entry.ext
            extractor.users.saveTable()
            extractor.users.discardClose()
            extractor.urlManager.close()
            extractor.errorLister.close()
            self.main.General.logger.info(f"Closed and saved {extractor.configName} UI")

    def trimLogs(self):
        for entry in self.main._getExtractors(False):
            extractor = entry.ext
            extractor.logger.trim(self.main.General.config.settings["maxlogentries"])

    def initExtractors(self):
        self.main.General.ui.comboBox.clear()
        for extractorType in self.availableExtractors:
            self.main.General.ui.comboBox.addItem(extractorType)
            self.main.General.logger.debug(f"Added {extractorType} to combo box")

        for ext in self.main.General.config.settings["extractors"]:
            start = time.perf_counter()
            extractorId = ext["id"]
            extractorType = ext["type"]

            if extractorId is None or not extractorType:
                self.generalLogger.error(f"Invalid extractor config: {ext}")
                continue

            extractorId = int(extractorId)

            factory = self.extractorFactories.get(extractorType)
            if factory is None:
                self.generalLogger.error(f"Extractor type {extractorType} not found in factories!")
                continue

            try:
                #   Create extractor with the stored ID
                extractor = factory(extractorId)
                self.activeExtractors[extractorId] = extractor

                #   Add to main.extractors list in the required format
                extractorEntry = ExtractorEntry(extractor)
                self.main.extractors.append(extractorEntry)
                self.main.General.logger.debug(f"Loaded {extractor.configName}")

                #   Create tab
                self.main.tabs.addTab(extractor, f"{extractor.name} ({extractorId})")
                self.main.qtHelper.setIcon(self.main.tabs, "dsuiext_4121.ico")

                self.setupExtractor(extractor)

                self.main.cmd.info(
                    f"[{datetime.now()}] Fully initialized {extractor.configName} in {(time.perf_counter() - start) * 1000:.6f}ms"
                )

            except Exception as e:
                self.generalLogger.error(f"Failed to load extractor {extractorType} (ID: {extractorId}): {str(e)}")

        self.main._hideWinConsole()
        if not self.main.args.hidden:
            self.main.show()
            self.main.activateWindow()

    def _initExtractorUi(self, extractor: "Extractor"):
        try:
            tab = extractor.ui.tabWidget
            tab.currentChanged.connect(self.main.tabSwitched)

            self.main.configurator.createWidgetsFromConfig(extractor, self.main)
            self.main.configurator.loadwidgetsConnection(extractor)
        except Exception as e:
            raise Exception(f"Failed to initialize Extractor's ui: {e}")

    def _refreshExtractorUi(self, extractor: "Extractor"):
        try:
            extractor.config.updateUI()
        except Exception as e:
            raise Exception(f"Failed to refresh Extractor's ui: {e}")

    #   Initializes all extractors and deletes them to test their validity
    def initTest(self):
        error = False
        for name, factory in self.extractorFactories.items():
            try:
                extractor = factory("init_test")
                self.setupExtractor(extractor)

            except AttributeError as e:
                self.main.qtHelper.Throw(f"Make sure to have set up widgets correctly for {name}: {e}", logger=self.main.General.logger)
                error = True
            finally:
                del extractor

        self.main.safeTrash(self.main._tempDPath)

        if error:
            self.main.General.logger.warning("init test not passed")
        else:
            self.main.General.logger.info("init test passed")

    #   Creates a new extractors based on selected combobox
    #   Does not initialize all extractors nor load a pre-existing extractor
    def addExtractor(self):
        extractorType = str(self.main.General.ui.comboBox.currentText())
        factory = self.extractorFactories.get(extractorType)

        if factory is None:
            self.main.General.logger.warning(f"No extractor found for {extractorType}!")
            return

        #   Generate unique numeric ID for this extractor
        extractorId = self._generateExtractorId()

        #   Create the extractor with the generated ID
        extractor = factory(extractorId)
        self.activeExtractors[extractorId] = extractor

        extractorEntry = ExtractorEntry(extractor)
        self.main.extractors.append(extractorEntry)

        extractorConfig = {"id": str(extractorId), "type": extractorType}
        self.main.General.config.settings["extractors"].append(extractorConfig)

        self.main.General.logger.debug(f"Adding {extractorType} ({extractorId})")
        self.main.tabs.addTab(extractor, f"{extractor.name} ({extractorId})")
        self.setupExtractor(extractor)
        self.main.qtHelper.setIcon(self.main.tabs, "dsuiext_4121.ico")

    def setupExtractor(self, extractor: "Extractor"):
        self._initExtractorUi(extractor)
        self._refreshExtractorUi(extractor)

    def removeExtractor(self, extractor: "Extractor"):
        try:
            reply = QMessageBox.question(
                self.main,
                "Confirm Deletion",
                f"Do you really want to remove {extractor.name} ({extractor.id})?\nThe files will be sent to the trashbin",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.No:
                return

            extractorId = extractor.id

            #   Ensure extractorId is an integer
            if isinstance(extractorId, str):
                try:
                    extractorId = int(extractorId)
                except ValueError:
                    self.main.General.logger.error(f"[{datetime.now()}] Invalid extractor ID: {extractorId}")
                    return

            if extractorId in self.activeExtractors:
                extractor = self.activeExtractors[extractorId]
                extractor.stop()

                #   Remove tab
                QtHelper.removeCurrentExtractorTab(self.main.tabs)

                #   Remove from main.extractors list
                self.main.extractors = [entry for entry in self.main.extractors if entry.ext != extractor]

                #   Remove from active extractors
                del self.activeExtractors[extractorId]

                #   Remove from config
                self.main.General.config.settings["extractors"] = [
                    ext for ext in self.main.General.config.settings["extractors"] if int(ext.get("id", -1)) != extractorId
                ]

                #   Remove extractor files
                self.safeTrash(extractor.usersFPath)
                self.safeTrash(extractor.configFPath)
                self.safeTrash(extractor.erroredFPath)
                self.safeTrash(extractor.runningConfigFPath)

                self.main.General.logger.info(f"Removed extractor ID: {extractorId}")
                return
            return
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"There was an error deleting the extractor: {e}", title="Error deleting the extractor")
            self.main.General.logger.error(f"There was an error deleting the extractor: {e}")

    #   Loads all extractors from config, their settings will be automatically applied based on ID and name

    def _loadExtractorsFromConfig(self):
        self.generalLogger.debug(f"ExtractorsManager::_loadExtractorsFromConfig")

        for ext in self.main.General.config.settings["extractors"]:
            extractorId = ext["id"]
            extractorType = ext["type"]

            if extractorId is None or not extractorType:
                self.generalLogger.error(f"Invalid extractor config: {ext}")
                continue

            extractorId = int(extractorId)

            factory = self.extractorFactories.get(extractorType)
            if factory is None:
                self.generalLogger.error(f"Extractor type {extractorType} not found in factories!")
                continue

            try:
                #   Create extractor with the stored ID
                extractor = factory(extractorId)
                self.activeExtractors[extractorId] = extractor

                #   Add to main.extractors list in the required format
                extractorEntry = ExtractorEntry(extractor)
                self.main.extractors.append(extractorEntry)
                self.main.General.logger.debug(f"Loaded {extractor.configName}")

                #   Create tab
                self.main.tabs.addTab(extractor, f"{extractor.name} ({extractorId})")
                self.main.qtHelper.setIcon(self.main.tabs, "dsuiext_4121.ico")

            except Exception as e:
                self.main.varHelper.exception(e)
                self.generalLogger.error(f"Failed to load extractor {extractorType} (ID: {extractorId}): {str(e)}")

    def savelogs(self):
        self.generalLogger.info("Saving extractor logs...")
        self.main.cmd.info(f"[{datetime.now()}] Saving extractor logs")
        for entry in self.main._getExtractors():
            extractor = entry.ext
            extractor.logger.info("NA2000 Stopped")
        self._removeExceedingLogs()

    def saveConfigs(self):
        self.generalLogger.info("Saving extractors config")
        self.main.cmd.info(f"[{datetime.now()}] Saving extractors config")
        for entry in self.main._getExtractors():
            extractor = entry.ext
            extractor.config.saveConfig(forced=True)

    def getExtractorById(self, extractorId) -> "Extractor | None":
        # Handle both string and integer IDs
        if isinstance(extractorId, str):
            try:
                extractorId = int(extractorId)
            except ValueError:
                return None
        return self.activeExtractors.get(extractorId)

    def getAllExtractors(self):
        return self.main.extractors

    def _removeExceedingLogs(self):
        _maxSizeMB = self.main.General.config.settings["maxlogsize"]
        maxSizeBytes = _maxSizeMB * 1024 * 1024

        if not os.path.basename(self.main.logPath).lower() == "logs":
            self.main.qtHelper.Throw(
                f"{os.path.basename(self.main.logPath).lower()} is NOT the log place!\nReport this to github",
                logger=self.main.General.logger,
            )

            return

        def __getFolderSize(path):
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.isfile(fp):
                        total += os.path.getsize(fp)
            return total

        def __sortLogsByAge(path):
            #   Collect all logs (.txt)
            files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".txt")]
            return sorted(files, key=os.path.getmtime)

        while __getFolderSize(self.main.logPath) > maxSizeBytes:
            logFiles = __sortLogsByAge(self.main.logPath)
            #   No files to delete
            if not logFiles:
                break
            oldestFile = logFiles[0]
            self.safeTrash(oldestFile)
