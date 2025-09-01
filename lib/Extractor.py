from typing import TYPE_CHECKING, List

from lib.Enums import Configure, ExtractorState, LogLevel, MessageType, Return, SpecialWidgets, Validation

if TYPE_CHECKING:
    from na2000 import MainApp

import os
import json
import threading
import re
import random

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt

from lib.ui.UserTable_manager import UserTable
from lib.ui.CookieEdit_manager import CookieEdit
from lib.ui.ErroredLister_manager import ErroredLister
from lib.ui.UrlManager_manager import URLManager
from lib.ui.ExtractorUi import Ui_Extractor
from lib.ConsoleLogger import ConsoleLogger
from lib.FileMonitor import FileMonitor
from lib.GalleryRunner import GalleryRunner
from lib.ConfigManager import Config
from lib.QtHelper import QtHelper
from lib.Logic import Logic
from threading import Event
from datetime import datetime

from lib.ui.UserTable_manager import Table

import time


class Extractor(QWidget):
    def __init__(self, settings, main: "MainApp", id: int):
        super().__init__()
        try:
            start = time.perf_counter()
            self.main = main
            self.inv = main._inv

            self.settings = settings
            self.name = self.settings.extractorName
            self.main.cmd.info(f"[{datetime.now()}] Configuring {self.name}")

            self.id = id
            self.initTest: bool = True if self.id == "init_test" else False
            self.configName: str = f"{self.name}_{id}_"
            self.fullName: str = f"{self.name} ({id})"
            self.galleryName: str = self.settings.galleryName
            self.currentOperations: list[ExtractorState] = [ExtractorState.IDLE]

            if self.initTest:
                self.logsPath = main._tempDPath
                self.cookiesPath = os.path.join(main._tempDPath, self.configName)
                self.usersFPath = os.path.join(main._tempDPath, f"{self.configName}Users.json")
                self.configFPath = os.path.join(main._tempDPath, f"{self.configName}Settings.json")
                self.erroredFPath = os.path.join(main._tempDPath, f"{self.configName}Errored.json")
                self.runningConfigFPath = os.path.join(main._tempDPath, f"{self.configName}Conf.json")
            else:
                self.logsPath = main.logPath
                self.cookiesPath = os.path.join(main._cookiesDPath, self.configName)
                self.usersFPath = os.path.join(main._usersDPath, f"{self.configName}Users.json")
                self.configFPath = os.path.join(main._extConfigDPath, f"{self.configName}Settings.json")
                self.erroredFPath = os.path.join(main._extConfigDPath, f"{self.configName}Errored.json")
                self.runningConfigFPath = os.path.join(main._runningConfigPath, f"{self.configName}Conf.json")

            self.ui = Ui_Extractor()
            self.ui.setupUi(self)

            #   Data and config
            self.event_loopStop = Event()
            self.cursorExtractionEnabled = self.settings.cursorExtractionEnabled
            self.widgetsConfiguration = self.settings.getUiConfiguration(self, self.main)
            self.widgetsConnection = self.buildConnectionsMap(self.widgetsConfiguration)
            self.configTemplate = self.buildTemplate(self.widgetsConfiguration)
            table = self.settings.getUsertableTemplate()
            self.tableTemplate = table[0]
            self.comboTemplate = table[1]
            self.userIdentificaiton = table[2]
            self.setupDefaultConfig()

            self.config = Config(self.main, self.configTemplate, self.configFPath, self.fullName, self, self.widgetsConnection, self.ui)

            #   Logging
            self.logger = ConsoleLogger(self.main, self.ui.theLogPlace, self.logsPath, self.configName, self.config.settings)
            self.generalLogger = main.General.logger

            self.errorLister = ErroredLister(main, self)
            self.galleryRunner = GalleryRunner(main, self)
            self.monitor = FileMonitor(self.logger, self.galleryRunner, main)
            self.users = UserTable(main, self)
            self.commonUserOptions = settings.commonUserOptions
            self.statCounter = main.stats.counter
            self.logic = Logic(self.main.General.config.settings, self)
            self.urlManager = URLManager(self.main, self)

            # Logic
            self.resetConfigCursor = False
            self.jobIndex = 0
            self.loopStopRequested = False
            self.loopRunning = False
            self.filterAppend = settings.filterAppend
            self.argsAppend = settings.argsAppend
            self.inhibitRunSignals = False
            self.runThread = None
            self.user = dict()

            #   Ui
            self.setupDefaultUi()
            self.ui.tabWidget.setCurrentIndex(0)

            self.main.qtHelper.setIcon(self.ui.btn_StopRun, "imageres_5365.ico")
            self.main.qtHelper.setIcon(self.ui.btn_skipJob, "comres_2855.ico")
            self.main.qtHelper.setIcon(self.ui.btn_showUsersTable, "explorer_261.ico")
            self.main.qtHelper.setIcon(self.ui.btn_showCookiesTable, "dsuiext_4110.ico")
            self.main.qtHelper.setIcon(self.ui.btn_showErrored, "cryptui_3417.ico")
            self.main.qtHelper.setIcon(self.ui.btn_deleteExtractor, "aclui_126.ico")
            self.main.qtHelper.setIcon(self.ui.btn_copyLastCursor, "dsquery_153.ico")
            self.main.qtHelper.setIcon(self.ui.btn_customRun, "inetcpl_1315.ico")

            if not self.cursorExtractionEnabled:
                self.ui.btn_copyLastCursor.setVisible(False)

            self.main.cmd.debug(f" :{__name__}::__init__ -> {self.configName}, {(time.perf_counter() - start) * 1000:.6f}ms")
        except Exception as e:
            self.main.varHelper.exception(e)
            if hasattr(self.main, "General"):
                self.main.General.logger.error(f"Something went wrong while creating the extractor: {e}")
            raise

    def _fillUserEntries(self, userlist):
        template = self.tableTemplate
        for row in template:
            keyname = row[3]
            defaultvalue = row[4]
            if keyname == None:
                continue

            for user in userlist:
                if keyname not in user:
                    self.inv(
                        lambda: self.logger.debug(f"Missing '{keyname}' in user {user.get('UserHandle', '?')} = '{str(defaultvalue)}'")
                    )
                    user[keyname] = defaultvalue

    def getUserList(self) -> list[dict]:
        self._fillUserEntries(self.users.config.settings["users"])
        return self.users.config.settings["users"]

    def showUsersTable(self):
        self.main.debuggy(f"Extractor::showUsersTable", self)
        self.users.setWindowState(Qt.WindowState.WindowNoState)
        self.users.show()
        self.users.raise_()
        self.users.activateWindow()

    def showCookiesTable(self):
        self.main.debuggy(f"Extractor::showCookiesTable", self)
        self.cookiesTableUi.setWindowState(Qt.WindowState.WindowNoState)
        self.cookiesTableUi.show()
        self.cookiesTableUi.raise_()
        self.cookiesTableUi.activateWindow()

    def showErroredTable(self):
        self.main.debuggy(f"Extractor::showErroredTable", self)
        self.errorLister.setWindowState(Qt.WindowState.WindowNoState)
        self.errorLister.show()
        self.errorLister.raise_()
        self.errorLister.activateWindow()

    def showCustomRunTable(self):
        self.main.debuggy(f"Extractor::showCustomRunTable", self)
        self.urlManager.setWindowState(Qt.WindowState.WindowNoState)
        self.urlManager.updateUi()
        self.urlManager.show()
        self.urlManager.raise_()
        self.urlManager.activateWindow()

    def _initStartButton(self):
        if hasattr(self.ui, "btn_StopRun"):
            button = self.ui.btn_StopRun
            button.setText("Run")
            if button.receivers("clicked()") > 0:
                button.clicked.disconnect()

            button.clicked.connect(self.startExtraction)
            self.event_loopStop.clear()

        if hasattr(self.errorLister.ui, "btn_retrySelected"):
            button = self.errorLister.ui.btn_retrySelected
            button.setEnabled(True)

    def _initStopButton(self):
        if hasattr(self.ui, "btn_StopRun"):
            button = self.ui.btn_StopRun
            button.clicked.disconnect()
            button.setText("Force stop")
            button.clicked.connect(self.stop)

        if hasattr(self.errorLister.ui, "btn_retrySelected"):
            button = self.errorLister.ui.btn_retrySelected
            button.setEnabled(False)

    def stop(self):
        self.inv(lambda: self.logger.debug("Extractor::stop"))
        if self.inhibitRunSignals:
            return
        self.loopStopRequested = True
        self.event_loopStop.set()
        self.galleryRunner.forceStop()

    def run(self, jobOverride, operationOverride) -> None:
        """First function that initializes an extraction
        If provided if jobOverride it will call to run the jobs in that dictionary
        Else it will call to run the user list
        Settings are saved so that they cannot change during extraction
        """
        try:
            #   Initialize
            self.inv(lambda: self.logger.debug("Extractor::run"))
            self.event_loopStop.clear()
            self.loopRunning = True
            self.loopStopRequested = False
            self.inv(self._initStopButton)
            self.main.threadTimeCounter.extRunning()

            #   Save settings
            settings = self.main.General.config.settings
            self.inhibitCursorUpdate = settings["nocursorupdate"]
            self.inhibitUnixUpdate = settings["nounixupdate"]
            self.inhibitErrorBoxes = settings["errorboxes"]
            self.restartOnCode = settings["exitcoderestart"]
            self.maximumruns = settings["maximumruns"]
            self.looptime = settings["looptime"]
            self.randomizeUsers = settings["randomizeusers"]
            self.defaultDestPath = self.config.settings["defaultpath"]

            self.inv(
                lambda s=self.loopStopRequested, e=self.event_loopStop.is_set(): self.logger.debug(
                    f"Extractor::run -> loopStopRequested: {s}, event_loopStop.is_set(): {e}"
                )
            )
            self.inv(
                lambda a=self.inhibitCursorUpdate, b=self.inhibitUnixUpdate: self.logger.debug(
                    f"inhibitCursorUpdate: {a}, inhibitUnixUpdate: {b}"
                )
            )

            #   Loop maximumruns times
            for i in range(self.maximumruns):
                if self.loopStopRequested:
                    break

                if jobOverride:
                    self.setCurrentOperations(operationOverride)
                    status = self._processJobOverride(jobOverride, ", ".join(s.name for s in operationOverride))
                    self.loopStopRequested = True
                    continue
                else:
                    status = self._processUsers()

                if status == Return.FAILED:
                    break

                if i + 1 != self.maximumruns:
                    self.inv(lambda i=i: self.logger.success(f"Will run again in {self.looptime} seconds ({i + 2}/{self.maximumruns})"))
                    self.event_loopStop.clear()
                    if self.event_loopStop.wait(timeout=self.looptime):
                        break
                else:
                    self.inv(lambda: self.logger.info(f"All runs completed"))
                    break

        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.logger.error(f"General Error: {e}"))
        finally:
            self.setCurrentOperations([ExtractorState.IDLE])
            self.monitor.stop()
            self.jobIndex = 0
            self.inv(lambda: self.generalLogger.log(f"{self.fullName} extraction stopped"))
            self.inv(lambda: self.logger.log(f"Extraction stopped"))
            self.loopStopRequested = False
            self.main.tray.refreshMenu()
            self.main.threadTimeCounter.extStopped()
            self.inv(self._initStartButton)
            self.inv(self._disableSkipbutton)
            self.loopRunning = False
            self.inhibitRunSignals = False
            self.user = {}
            self.resetConfigCursor = False

    def _processUsers(self) -> Return:
        try:
            userList = self.getUserList()
            if self.randomizeUsers:
                random.shuffle(userList)

            for _userIndex, self.user in enumerate(userList):
                if self.loopStopRequested:
                    break

                self.jobIndex = 0
                if self._skipUser():
                    continue

                value = self._prepare()
                if value == Return.FAILED:
                    return Return.FAILED
                try:
                    jobs = self.settings.getJobs(
                        self.user,
                        self.config.settings,
                        self.main.General.config.settings,
                        self.logic.getBaseConf(self.user),
                        self.logic.deepUpdate,
                        self.main,
                    )[0]

                except Exception as e:
                    self.inv(lambda e=e: self.logger.error(f"Error during parsing the job: {e}"))
                    raise Exception("Error during parsing the job")

                self.inv(self._enableSkipbutton)
                self.setCurrentOperations([ExtractorState.NORMAL_EXTRACTION])
                status = self._runJobs(jobs, self.user, False)
                self.main.debuggy(f"self._runJobs returned {status}", self)
                self.inv(self._disableSkipbutton)

                if status == Return.USER_SKIPPED:
                    continue
                elif status == Return.FAILED:
                    return status

                if not self.inhibitUnixUpdate:
                    self.inv(lambda u=self.user["UserHandle"]: self.users.setUserKey(u, "LastExtracted", int(time.time())))
            return Return.SUCCESS
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Error when processing users: {e}")

    def _processJobOverride(self, jobOverride, operationOverride) -> Return:
        try:
            self.inhibitCursorUpdate = True
            self.jobIndex = 0

            self.inv(lambda: self.logger.info(f"- - - - - Starting extraction for {len(jobOverride)} URLs - - - - -"))
            for job in jobOverride:
                #   Set user
                user = job["userData"]
                user["Skip"] = False
                self.user = user

                #   Prepare settings
                value = self._prepare(jobOverride)
                if value == Return.FAILED:
                    return Return.FAILED

                #   Stop if in loop
                if self.loopStopRequested:
                    return Return.SUCCESS

                #   Check to skip user
                if self._skipUser():
                    continue

                #   Run extraction
                self.inv(self._enableSkipbutton)
                url, config, type = job["url"], job["config"], job["type"]
                status = self._runJob(url, config, type, user, True)
                self.main.debuggy(f"self._runJobs returned {status}", self)
                self.inv(self._disableSkipbutton)

                #   Check status, since there's only 1 user skipping it would mean terminating
                if status == Return.USER_SKIPPED:
                    break
                elif status == Return.FAILED:
                    return status

            return Return.SUCCESS
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Error when processing jobs: {e}")

    def _skipUser(self) -> bool:
        if self.user["Skip"]:
            self.inv(lambda userHandle=self.user["UserHandle"]: self.logger.info(f"Skipping {userHandle}: Set to skip in user table"))
            return True

        try:
            if self.commonUserOptions and all(self.user[opt] is False for opt in self.commonUserOptions):
                self.inv(
                    lambda userHandle=self.user["UserHandle"]: self.logger.warning(
                        f"Skipping {userHandle}: Common extraction options are all off"
                    )
                )
                return True
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.logger.error(f"Failed checking common settings: {e}"))

        try:
            _userExtractedUnix = int(self.user["LastExtracted"])
            _todayUnix = int(datetime.now().timestamp())
            _unixOffset = 3500
            if _userExtractedUnix + _unixOffset > _todayUnix:
                self.logger.debug(f"UNIX: {_userExtractedUnix + _unixOffset} > {_todayUnix}")
                self.inv(
                    lambda userHandle=self.user["UserHandle"]: self.logger.info(f"Skipping {userHandle}: User was already extracted today")
                )
                return True
            else:
                self.logger.debug(f"UNIX: {_userExtractedUnix + _unixOffset} <= {_todayUnix}")
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.logger.error(f"Failed setting up the user's date: {e}"))

        return False

    def _prepare(self, jobOverride=None) -> Return:
        if not os.path.exists(self.defaultDestPath):
            self.main.qtHelper.Throw(
                f"The default destination path does not exist",
                title=f"{self.name} error",
                type=MessageType.WARNING,
                logger=self.logger,
            )
            return Return.FAILED

        _userPath = (
            self.user["DestinationPath"]
            if self.user["DestinationPath"] != "default"
            else f"{self.defaultDestPath}/{self.user['UserHandle']}"
        )
        self.main.debuggy(f"UserData: {self.user}", self)
        if not jobOverride:
            userHandle = self.user["UserHandle"]
            self.inv(lambda u=userHandle: self.logger.info(f"- - - - - Starting extraction for user: {u} - - - - -"))
            self.inv(lambda: self.main.stats.counter.increase(1, "totAmount"))
        try:
            #   Change filemonitor folder
            self.inv(lambda u=_userPath: self.monitor.changeDir(u))
            self.inv(self.monitor.start)
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.logger.error(f"Error during the filemonitor init: {e}"))
            return Return.FAILED

        return Return.SUCCESS

    def _runJob(self, url, config, type, user, isOverridden) -> Return:
        _userExtractedDate = self.toDate(int(user["LastExtracted"]))
        _argDateFilter = (
            f'--filter "{self.filterAppend}date >= datetime({_userExtractedDate}) or abort()"' if not self.inhibitUnixUpdate else ""
        )
        _cmdArgs = f'"{url}" --no-input -v --config "{self.runningConfigFPath}" {self.argsAppend} {_argDateFilter}'

        self.inv(lambda type=type: self.logger.info(f"Extracting {type}..."))
        self.jobIndex += 1
        self.main.debuggy(f"index {self.jobIndex} {url} -> {type}", self)

        if not self._writeCriticalFile(config, self.runningConfigFPath, 100, 1):
            return Return.FAILED

        try:
            #   Retry loop
            while True:
                self._resetConfigCursor(config)
                self.inv(lambda: self.logger.debug(f"Command: {self.main.galleryFPath} {_cmdArgs}"))
                galleryStatus = self.galleryRunner.run(self.main.galleryFPath, _cmdArgs, self.main._scriptDir)
                self.inv(lambda: self.logger.debug("Extractor::_runJob -> gallery-dl process stopped"))

                userHandle = user["UserHandle"]

                if galleryStatus[0]:
                    break

                error = galleryStatus[1]
                if error == Return.FORCE_TERMINATED:
                    if isOverridden:
                        self.inv(lambda: self.logger.alert(f"Extraction forcefully stopped at {userHandle}'s URL "))
                    else:
                        self.inv(lambda: self.logger.alert(f"Extraction forcefully stopped at user {userHandle}"))
                    self.inv(lambda: self.generalLogger.alert(f"{self.fullName} extraction stopped forcefully"))
                    return Return.FAILED

                elif error == Return.JOB_SKIPPED:
                    self.inv(lambda type=type: self.logger.alert(f"Skipping job {type}"))
                    break

                elif error == Return.USER_SKIPPED:
                    if isOverridden:
                        self.inv(lambda: self.logger.alert("Stopping url extraction"))
                        return Return.FORCE_TERMINATED
                    else:
                        self.inv(lambda u=user["UserHandle"]: self.logger.alert(f"Skipping user {u}"))
                        return Return.USER_SKIPPED

                elif error == Return.ERR_GALLERY_CODE1:
                    if self.restartOnCode:
                        if not self.inhibitErrorBoxes:
                            self.main.qtHelper.Throw(
                                "Gallery-dl decided to give up\nThe extraction of the job will be restarted",
                                type=MessageType.WARNING,
                                title=f"{self.name} Warning",
                            )
                        self.inv(lambda: self.logger.warning("The extraction of the job will be restarted"))
                        self.inv(lambda type=type: self.logger.info(f"Extracting {type}..."))
                        continue
                    else:
                        if isOverridden:
                            msg0 = "Gallery-dl decided to give up\nStopping Extraction"
                            msg1 = "Skipping to the next user"
                        else:
                            msg0 = "Gallery-dl decided to give up\nSkipping to the next user"
                            msg1 = "Stopping Extraction"

                        if not self.inhibitErrorBoxes:
                            self.main.qtHelper.Throw(
                                msg0,
                                type=MessageType.WARNING,
                                title=f"{self.name} Warning",
                            )
                        self.inv(lambda: self.logger.alert(msg1))
                        return Return.USER_SKIPPED

                elif error == Return.ERR_GALLERY_RETRY:
                    self.inv(lambda: self.logger.info("The extraction of the job will be restarted"))
                    self.inv(lambda type=type: self.logger.info(f"{type}..."))
                    continue

                else:
                    self.inv(lambda: self.logger.error(f"Extraction failed at user {userHandle}"))
                    self.inv(lambda g=error: self.logger.error(f"Reason: {g}"))
                    self.inv(lambda: self.generalLogger.error(f"{self.fullName} extraction stopped with error"))
                    return Return.FAILED

            self.main.debuggy("Out of while", self)
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda e=e: self.logger.error(f"Failed executing gallery-dl: {e}"))
            raise

        return Return.SUCCESS

    def _runJobs(self, jobs, user, isOverridden) -> Return:
        for job in jobs:
            url, config, type = job["url"], job["config"], job["type"]

            status = self._runJob(url, config, type, user, isOverridden)
            if status != Return.SUCCESS:
                return status
        return Return.SUCCESS

    def _resetConfigCursor(self, data):
        if self.resetConfigCursor and self.cursorExtractionEnabled:
            data["extractor"][self.galleryName]["cursor"] = ""
            self._writeCriticalFile(data, self.runningConfigFPath, 100, 1)
            self.resetConfigCursor = False

    def _writeCriticalFile(self, data, filename, max_attempts, delay) -> bool:
        attempts = 0
        while attempts < max_attempts:
            try:
                with open(filename, "w") as file:
                    json.dump(data, file, indent=4)

                self.inv(lambda: self.logger.debug(f"Extractor::_writeCriticalFile -> Wrote {filename}"))
                return True

            except Exception as e:
                attempts += 1
                self.inv(
                    lambda e=e, a=attempts: self.logger.error(
                        f"Extractor::_writeCriticalFile -> Writing to extraction config n.{a} failed: {str(e)}"
                    )
                )

                if attempts < max_attempts:
                    time.sleep(delay)
        self.inv(lambda: self.logger.error("Extractor::_writeCriticalFile -> Writing to the extractor's config failed"))
        return False

    @staticmethod
    def toDate(timestamp) -> str:
        dt = datetime.fromtimestamp(timestamp)
        return f"{dt.year}, {dt.month}, {dt.day}"

    def setupDefaultConfig(self):
        #   Config
        defaultConfigTemplateOptions = {
            "enabled": True,
            "defaultpath": "",
            "cookiespath": "",
            "consoleshowinfo": True,
            "consoleshowalerts": True,
            "consoleshowerrors": True,
            "consoleshowothers": False,
            "consoleshowdebug": False,
            "consoleshowsuccess": True,
            "sleeptime": self.settings.sleepTime,
        }
        self.configTemplate.update(defaultConfigTemplateOptions)
        self.configTemplate.update({})

        #   Table
        prepend = [
            [Table.HIDE, Table.CHECKBOX, "Sel", "Selected", False, None],
            [Table.HIDE, Table.CHECKBOX, "Skip", "Skip", False, None],
            [Table.SHOW, Table.TEXTBOX, "Note", "Note", "Note", None],
            [Table.SHOW, Table.TEXTBOX, self.userIdentificaiton, "UserHandle", "User", Validation.EMPTY],
            [Table.SHOW, Table.TEXTBOX, "Destination Path", "DestinationPath", "default", Validation.DIR_PATH],
            [Table.SHOW, Table.DESTINATION, "", None, None, None],
        ]

        append = [
            [Table.HIDE, Table.TEXTBOX, "Last Extracted (Unix)", "LastExtracted", 0, Validation.INTEGER],
            [Table.HIDE, Table.AUTOTIMESTAMP, "", None, None, None],
            [Table.HIDE, Table.SQLDELETER, "", None, None, None],
        ]

        if self.cursorExtractionEnabled:
            append.append([Table.HIDE, Table.TEXTBOX, "Cursor ID", "Cursor", "", None])

        self.tableTemplate = prepend + self.tableTemplate + append

    def setupDefaultUi(self):
        try:
            self.ui.grpbox_tabconsole.setStyleSheet("""
            QGroupBox::title {
                color: rgb(153, 153, 153)
            }
            """)
            self.ui.grpbox_settings.setStyleSheet("""
            QGroupBox::title {
                color: rgb(153, 153, 153)
            }
            """)

            extWidgets = [
                {
                    Configure.WIDGET: "cfgui_consoleshowWHITE",
                    Configure.KEY: "consoleshowinfo",
                    Configure.FUNCTION: lambda value: self.logger.setLevelVisibility(LogLevel.WHITE, value),
                },
                {
                    Configure.WIDGET: "cfgui_consoleshowYELLOW",
                    Configure.KEY: "consoleshowalerts",
                    Configure.FUNCTION: lambda value: self.logger.setLevelVisibility(LogLevel.YELLOW, value),
                },
                {
                    Configure.WIDGET: "cfgui_consoleshowRED",
                    Configure.KEY: "consoleshowerrors",
                    Configure.FUNCTION: lambda value: self.logger.setLevelVisibility(LogLevel.RED, value),
                },
                {
                    Configure.WIDGET: "cfgui_consoleshowOTHER",
                    Configure.KEY: "consoleshowothers",
                    Configure.FUNCTION: lambda value: self.logger.setLevelVisibility(LogLevel.OTHER, value),
                },
                {
                    Configure.WIDGET: "cfgui_consoleshowGREY",
                    Configure.KEY: "consoleshowdebug",
                    Configure.FUNCTION: lambda value: self.logger.setLevelVisibility(LogLevel.GREY, value),
                },
                {
                    Configure.WIDGET: "cfgui_consoleshowGREEN",
                    Configure.KEY: "consoleshowsuccess",
                    Configure.FUNCTION: lambda value: self.logger.setLevelVisibility(LogLevel.GREEN, value),
                },
                {
                    Configure.WIDGET: "grpbox_settings",
                    Configure.VALIDATION: SpecialWidgets.EXT_GRPBOX,
                    Configure.KEY: "enabled",
                },
                {
                    Configure.WIDGET: "label_2",
                    Configure.VALIDATION: SpecialWidgets.EXT_COOKIESLABEL,
                    Configure.KEY: "cookiespath",
                },
                {Configure.WIDGET: "btn_showCookiesTable", Configure.FUNCTION: lambda: self.showCookiesTable()},
                {Configure.WIDGET: "btn_showUsersTable", Configure.FUNCTION: lambda: self.showUsersTable()},
                {Configure.WIDGET: "btn_customRun", Configure.FUNCTION: lambda: self.showCustomRunTable()},
                {Configure.WIDGET: "btn_showErrored", Configure.FUNCTION: lambda: self.showErroredTable()},
                {
                    Configure.WIDGET: "btn_deleteExtractor",
                    Configure.FUNCTION: lambda: self.main.extractorsManager.removeExtractor(self),
                },
                {
                    Configure.WIDGET: "cfgui_defaultpath",
                    Configure.KEY: "defaultpath",
                    Configure.VALIDATION: Validation.PATH,
                },
                {
                    Configure.WIDGET: "cfgui_sleeptime",
                    Configure.KEY: "sleeptime",
                    Configure.VALIDATION: Validation.INTEGER,
                },
                {
                    Configure.WIDGET: "btn_pathselect",
                    Configure.VALIDATION: SpecialWidgets.EXT_BROWSER,
                    Configure.FUNCTION: lambda: QtHelper.browseFolder(self.ui.cfgui_defaultpath, self.main),
                },
            ]
            self.widgetsConnection.extend(extWidgets)

            self.cookiesTableUi = CookieEdit(self.cookiesPath, self.main.galleryFPath, self)
            self._initStartButton()

            self.ui.btn_skipJob.setDisabled(True)
            self.ui.btn_skipJob.clicked.connect(self.skipJob)
        except Exception as e:
            raise Exception(f"Failed to setup default ui: {e}")

    def skipJob(self):
        self.inv(lambda: self.logger.debug("Extractor::skipJob"))

        #   Get the current keyboard modifiers
        modifiers = QApplication.keyboardModifiers()

        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            self.galleryRunner.skipUser()
        else:
            self.galleryRunner.skip()

    def _disableSkipbutton(self):
        if hasattr(self.ui, "btn_skipJob"):
            self.inv(lambda: self.logger.debug("Extractor::_disableSkipbutton"))
            btn = self.ui.btn_skipJob
            btn.setDisabled(True)

    def _enableSkipbutton(self):
        if hasattr(self.ui, "btn_skipJob"):
            self.inv(lambda: self.logger.debug("Extractor::_enableSkipbutton"))
            btn = self.ui.btn_skipJob
            btn.setDisabled(False)

    #   Starts the extractor by checking some preliminary things like deactivating / activating buttons
    #   Then starts a thread that will run the loop
    #   The loop will take all users from the usertable and get their jobs
    #   Then a galleryRunner function will start gallery-dl
    def startExtraction(self, jobOverride=None, operationOverride: list[ExtractorState] | None = None):
        self.logger.debug(f"Extractor::startExtraction -> {True if jobOverride else False}")

        #   If asked to start while already running
        if self.loopRunning or self.galleryRunner.running:
            return

        if jobOverride:
            count = sum(1 for item in jobOverride if item.get("url") != "Unknown")
            self.logger.debug(f"Jobs overridden with {count} urls")
            self.main.debuggy(f"Jobs overridden with {count} urls", self)

        #   Reset state for new run
        self.loopStopRequested = False
        self.event_loopStop.clear()
        self.galleryRunner.stopReason = None
        self.galleryRunner.running = False
        self.galleryRunner._reset()
        self.logic = Logic(self.main.General.config.settings, self)

        self.inhibitRunSignals = True
        self.loopRunning = True
        self.inv(self._initStopButton)
        self.generalLogger.info(f"{self.name} extraction started")

        #   Cookies Path Check
        cookiesPath = self.config.settings["cookiespath"]

        checks = [
            (cookiesPath, "The path to the cookies does not exist"),
            (
                os.path.join(self.main.toolsPath, "ffmpeg.exe"),
                "ffmpeg does not exist! Please download it in ./external/ffmpeg.exe",
            ),
            (
                os.path.join(self.main.toolsPath, "mkvmerge.exe"),
                "mkvmerge does not exist! Please download it in ./external/mkvmerge.exe",
            ),
            (
                os.path.join(self.main.toolsPath, "gallery-dl.exe"),
                "gallery-dl does not exist! Please download it in ./external/gallery-dl.exe",
            ),
        ]

        for path, msg in checks:
            if not os.path.exists(path):
                self._checkMissingTools(msg)
                return

        #   Thread start
        self.runThread = threading.Thread(target=lambda: self.run(jobOverride, operationOverride), daemon=True)
        self.runThread.start()

        self.logger.info(f"{self.name} started")
        self.statCounter.increase(1, "totExtractorsRuns")
        self.main.tray.refreshMenu()
        self.inhibitRunSignals = False

    def _checkMissingTools(self, msg):
        self.logger.error(msg)
        self.generalLogger.error(f"{self.name} stopped with an error")
        self.loopRunning = False
        self.inhibitRunSignals = False
        self.inv(self._initStartButton)
        self.inv(self._disableSkipbutton)

    def buildTemplate(self, uiConfiguration):
        template = {}
        for entry in uiConfiguration:
            key = entry.get(Configure.KEY)
            value = entry.get(Configure.DEFAULT)

            if key != None and value != None:
                template[key] = value

        return template

    def buildConnectionsMap(self, uiConfiguration):
        template = []
        for entry in uiConfiguration:
            append = {}

            widget = entry.get(Configure.NAME)
            key = entry.get(Configure.KEY)
            validation = entry.get(Configure.VALIDATION)
            function = entry.get(Configure.FUNCTION)

            if not widget:
                raise Exception("A widget does not have a name! configure the name as {Configure.NAME: 'name'} ")

            if widget is not None:
                append[Configure.WIDGET] = widget
            if key is not None:
                append[Configure.KEY] = key
            if validation is not None:
                append[Configure.VALIDATION] = validation
            if function is not None:
                append[Configure.FUNCTION] = function

            template.append(append)
        return template

    def setCurrentOperations(self, states: List[ExtractorState]):
        string = ", ".join(state.name for state in states)
        self.logger.debug(f"Setting current operations to [{string}]")
        self.currentOperations = states


class ExtractorEntry:
    def __init__(self, extractor):
        self.extractor = extractor

    @property
    def ext(self):
        return self.extractor

    @property
    def enabled(self):
        return self.extractor.config.settings.get("enabled", True)
