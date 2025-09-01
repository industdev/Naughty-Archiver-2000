import os

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from lib.Enums import Validation
from lib.ui.UnixCreator_manager import UnixCreator
from lib.ui.GeneralTab_ui import Ui_TabGeneral
from lib.ConsoleLogger import ConsoleLogger
from lib.ConfigManager import Config, Configure

from lib.ConsoleLogger import LogLevel
import time
from datetime import datetime

from lib.ui.OutputHandlerCreator_manager import OutputHandlerCreator


class General(QWidget):
    def __init__(self, main):
        super().__init__()
        try:
            start = time.perf_counter()
            self.main = main
            self.inv = self.main._inv

            self.name = "General"
            self.main.cmd.info(f"[{datetime.now()}] Configuring {self.name}")

            self.ui = Ui_TabGeneral()
            self.ui.setupUi(self)
            self.logsPath = self.main.logPath
            self.id = 0
            self.configName = f"{self.name}_{self.id}_"
            self.fullName = f"{self.name} ({self.id})"

            self.configFPath = os.path.join(main._extConfigDPath, f"{self.configName}Settings.json")

            #   Data and config
            self.widgetsConnection = [
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
                {Configure.WIDGET: "cfgui_looptime", Configure.KEY: "looptime", Configure.VALIDATION: Validation.INTEGER},
                {Configure.WIDGET: "cfgui_maxlogsize", Configure.KEY: "maxlogsize", Configure.VALIDATION: Validation.INTEGER},
                {Configure.WIDGET: "cfgui_maximumruns", Configure.KEY: "maximumruns", Configure.VALIDATION: Validation.INTEGER},
                {Configure.WIDGET: "cfgui_maxdlspeed", Configure.KEY: "maxdlspeed", Configure.VALIDATION: Validation.INTEGER},
                {Configure.WIDGET: "cfgui_errortrigger", Configure.KEY: "stoptrigger", Configure.VALIDATION: Validation.INTEGER},
                {
                    Configure.WIDGET: "cfgui_errorboxes",
                    Configure.KEY: "errorboxes",
                },
                {
                    Configure.WIDGET: "cfgui_exitcode",
                    Configure.KEY: "exitcoderestart",
                },
                {
                    Configure.WIDGET: "cfgui_randomizelist",
                    Configure.KEY: "randomizeusers",
                },
                {
                    Configure.WIDGET: "cfgui_nostatsupdate",
                    Configure.KEY: "nostatsupdate",
                },
                {
                    Configure.WIDGET: "cfgui_autotester",
                    Configure.KEY: "autotester",
                },
                {
                    Configure.WIDGET: "cfgui_nounixupdate",
                    Configure.KEY: "nounixupdate",
                },
                {
                    Configure.WIDGET: "cfgui_nocursorupdate",
                    Configure.KEY: "nocursorupdate",
                },
                {
                    Configure.WIDGET: "cfgui_extendedmetadata",
                    Configure.KEY: "extendedmetadata",
                },
                {
                    Configure.WIDGET: "cfgui_skiploadingbars",
                    Configure.KEY: "skiploadingbars",
                    Configure.FUNCTION: self.main.loadingBar.terminate(),
                },
                {
                    Configure.WIDGET: "cfgui_showontaskbar",
                    Configure.KEY: "showtaskbar",
                },
                {
                    Configure.WIDGET: "cfgui_nosqlcreation",
                    Configure.KEY: "nosqlcreation",
                },
                {Configure.WIDGET: "cfgui_maxlogentries", Configure.KEY: "maxlogentries", Configure.VALIDATION: Validation.INTEGER},
                {Configure.WIDGET: "cfgui_sleepmodulate", Configure.KEY: "sleepmodulate", Configure.VALIDATION: Validation.INTEGER},
                {Configure.WIDGET: "btn_StopRun", Configure.FUNCTION: lambda: main.extractorsManager.startExtractors()},
                {Configure.WIDGET: "btn_insert", Configure.FUNCTION: lambda: main.extractorsManager.addExtractor()},
                {Configure.WIDGET: "btn_downloadTools", Configure.FUNCTION: lambda: main.downloader.setup()},
                {Configure.WIDGET: "btn_showUnixCreator", Configure.FUNCTION: lambda: self.showUnixCreator()},
                {Configure.WIDGET: "btn_showOutputHandlerCreator", Configure.FUNCTION: lambda: self.showOutputHandlerCreator()},
            ]
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.tabWidget.currentChanged.connect(self.main.tabSwitched)

            self.configTemplate = {
                "looptime": 3600,
                "maximumruns": 100,
                "maxdlspeed": 2500,
                "errorboxes": True,
                "maxlogsize": 1000,
                "showtaskbar": True,
                "consoleshowinfo": True,
                "consoleshowalerts": True,
                "consoleshowerrors": True,
                "consoleshowothers": False,
                "consoleshowdebug": False,
                "consoleshowsuccess": True,
                "maxlogentries": 10000,
                "randomizeusers": False,
                "comboboxIndex": 0,
                "sleepmodulate": 5,
                "nounixupdate": False,
                "nostatsupdate": False,
                "nocursorupdate": False,
                "extendedmetadata": False,
                "exitcoderestart": True,
                "supersecretoption": False,
                "skiploadingbars": False,
                "nosqlcreation": False,
                "stoptrigger": 20,
                "Downloader": {"everdownloaded": False, "gdlversion": "0", "gdlprompt": True},
                "uuid": None,
                "autotester": False,
                "extractors": [],
            }

            self.config = Config(self.main, self.configTemplate, self.configFPath, self.fullName, self, self.widgetsConnection, self.ui)
            self.logger = ConsoleLogger(self.main, self.ui.theLogPlace, self.logsPath, self.configName, self.config.settings)
            self.unixCreator = UnixCreator(self.main)
            self.outputHandlerCreator = OutputHandlerCreator(self.main, self)

            self.generalLogger = self.logger

            self.main.configurator.loadwidgetsConnection(self, self.logger)
            self.config.updateUI()

            self.main.qtHelper.setIcon(self.ui.btn_StopRun, "imageres_1013.ico")
            self.main.qtHelper.setIcon(self.ui.btn_insert, "hdwwiz_100.ico", size=(16, 16))
            self.main.qtHelper.setIcon(self.ui.btn_downloadTools, "FM20ENU_5.ico", size=(16, 16))
            self.main.qtHelper.setIcon(self.ui.btn_showUnixCreator, "ieframe_20783.ico", size=(16, 16))
            self.main.qtHelper.setIcon(self.ui.btn_showOutputHandlerCreator, "FXSRESM_2101.ico", size=(16, 16))

            self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")
        except Exception:
            raise

    def showUnixCreator(self):
        self.main.debuggy(f"General::showUnixCreator", self)
        self.unixCreator.setWindowState(Qt.WindowState.WindowNoState)
        self.unixCreator.show()
        self.unixCreator.raise_()
        self.unixCreator.activateWindow()

    def showOutputHandlerCreator(self):
        self.main.debuggy(f"General::btn_showOutputHandlerCreator", self)
        self.outputHandlerCreator.setWindowState(Qt.WindowState.WindowNoState)
        self.outputHandlerCreator.show()
        self.outputHandlerCreator.raise_()
        self.outputHandlerCreator.activateWindow()
