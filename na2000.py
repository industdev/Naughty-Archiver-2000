from typing import TYPE_CHECKING, Any, Callable, List

from lib.Extractor import ExtractorEntry
from lib.VarHelper import VarHelper

print(f"Script exec: {__name__}")
if TYPE_CHECKING:
    from na2000 import MainApp

import sys
import os
import subprocess
import traceback
import hashlib
import ctypes
import time
import faulthandler
import multiprocessing

from send2trash import send2trash
from datetime import datetime

from PySide6.QtWidgets import QApplication, QMainWindow, QStyleFactory, QMessageBox, QTabWidget
from PySide6.QtCore import Qt, QEvent, QObject, QObject, Signal, Slot
from PySide6.QtGui import QIcon, QKeySequence, QShortcut

from lib.ui.Statistics_manager import TabStatistics
from lib.ui.GeneralTab import General
from lib.ui.LoadingBar import LoadingBar

from lib.Downloader import Downloader
from lib.QtHelper import QtHelper
from lib.Configurator import Configurator
from lib.ExtractorsManager import ExtractorsManager
from lib.TrayHelper import TrayHelper
from lib.CrashHelper import CrashHelper
from lib.ThreadTimeCounter import ThreadTimeCounter
from lib.ArgHelper import ArgHelper
from lib.GlobaldataHelper import GlobaldataHelper
from lib.CmdLogger import CmdLogger
from lib.PathManager import PathManager
from lib.DebugManager import DebugManager


class MainApp(QMainWindow):
    def __init__(self, logger, crashHelper: CrashHelper, paths: PathManager):
        start = time.perf_counter()
        super().__init__()
        self.name = "Naughty Archiver 2000"
        self.version = "1.2"
        self.release = "release"

        self.name = f"{self.name} {self.release} v{self.version}"
        self.cmd = logger

        ctypes.windll.kernel32.SetConsoleTitleW(self.name)
        self.setWindowTitle(self.name)
        self.resize(800, 600)
        self.setStyle(QStyleFactory.create("WindowsVista"))

        self._scriptDir = paths.getExternalRes("")

        #   Paths
        _externalP = "external"
        self.galleryFPath = paths.getExternalRes(f"{_externalP}/gallery-dl.exe")
        self.toolsPath = paths.getExternalRes(f"{_externalP}")
        self.iconPath = paths.getExternalRes(f"{_externalP}/icon.ico")

        _savedP = "saved"
        os.makedirs(os.path.join(self._scriptDir, _savedP), exist_ok=True)
        self.logPath = paths.getExternalRes(f"{_savedP}/logs")
        self._cookiesDPath = paths.getExternalRes(f"{_savedP}/cookies")
        self._usersDPath = paths.getExternalRes(f"{_savedP}/users")
        self._extConfigDPath = paths.getExternalRes(f"{_savedP}/settings")
        self._tempDPath = paths.getExternalRes(f"{_savedP}/test")
        self._debugDPath = paths.getExternalRes(f"{_savedP}/debug")
        self.exceptionFPath = paths.getExternalRes(f"{_savedP}/latestException.txt")
        self.userOutputPatternsFPath = paths.getExternalRes(f"{_savedP}/userOutputPatterns.json")
        self._runningConfigPath = paths.getExternalRes(f"{_savedP}/run")

        _libP = "lib"
        self._animPath = paths.getInternalRes(f"{_libP}/ui/old/anim")
        self._iconsPath = paths.getInternalRes(f"{_libP}/ui/ico")
        self.defaultOutputPatternsFPath = paths.getInternalRes(f"{_libP}/defaultOutputPatterns.json")

        #   Init
        self.setWindowIcon(QIcon(self.iconPath))
        self.debug = False
        self.argHelper = ArgHelper(self)
        self.args = self.argHelper.args
        if self.args.debug:
            faulthandler.enable()
            faulthandler.enable(open(os.path.join(self.logPath, "fault.log"), "w"))
            self.debug = True
            self.debuggy(f"Debug mode enabled", "init")
            self.debuggy(f"\t{self.galleryFPath=}", "init")
            self.debuggy(f"\t{self.toolsPath=}", "init")
            self.debuggy(f"\t{self.iconPath=}", "init")
            self.debuggy(f"\t{self._runningConfigPath=}", "init")
            self.debuggy(f"\t{self.logPath=}", "init")
            self.debuggy(f"\t{self._cookiesDPath=}", "init")
            self.debuggy(f"\t{self._usersDPath=}", "init")
            self.debuggy(f"\t{self._extConfigDPath=}", "init")
            self.debuggy(f"\t{self._tempDPath=}", "init")
            self.debuggy(f"\t{self._animPath=}", "init")
            self.debuggy(f"\t{self._iconsPath=}", "init")
            self.debuggy(f"\t{self.defaultOutputPatternsFPath=}", "init")

        self.debugManager = DebugManager(self, self._debugDPath)
        self.varHelper = VarHelper(self)
        self.threadHelper = ThreadHelper()
        self.loadingBar = LoadingBar(self)
        self.qtHelper = QtHelper(self)
        self.tray = TrayHelper(self)
        self.configurator = Configurator(self)
        self.General = General(self)
        self.downloader = Downloader(self, self.safeTrash, self.toolsPath)
        self.stats = TabStatistics(self)
        self.threadTimeCounter = ThreadTimeCounter(self)
        self.crashHelper = crashHelper
        self.dataHelper = GlobaldataHelper(self)
        self.extractorsManager = ExtractorsManager(self, self.safeTrash)
        self.extractors: List[ExtractorEntry] = []

        logger.info(f"[{datetime.now()}] Args: {self.argHelper.args}")

        if self.args.runall:
            self.extractorsManager.startExtractors()

        if self.General.config.settings["autotester"]:
            self.extractorsManager.initTest()

        #   Init extractors
        self.initTabs()
        self.extractorsManager.initExtractors()

        self.configurator.updateNonExtractorUI()
        self.tray.trayThread.start()

        self.stats.counter.increase(1, "totSize")

        #   Console
        self.winConsole = True
        self.toggleWinConsole()
        winConsoleAct = QShortcut(QKeySequence("Ctrl+."), self)
        winConsoleAct.activated.connect(self.toggleWinConsole)

        self.threadTimeCounter.thread.start()
        self.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def initTabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(self.stats, "Stats")
        self.tabs.addTab(self.General, "General")
        self.qtHelper.setIcon(self.tabs, "dsuiext_4098.ico", index=0)
        self.qtHelper.setIcon(self.tabs, "devmgr_201.ico", index=1)

    def safeTrash(self, path: str, type: str = "any", safe=True):
        """Send path/file to bin safely, but only if inside the allowed directory and matches type

        Args:
            path (str): Absolute file path to trash
            type (str, optional): "folder", "file", or "any". Only trash if path matches type
        """
        self.debuggy(f"Safe trashing: {path}", "trashedFiles")
        path = os.path.normpath(path)
        allowedDirs = [
            os.path.normpath(os.path.join(self._scriptDir, "saved")),
            os.path.normpath(os.path.join(self._scriptDir, "external")),
        ]

        #   Check if the file is inside the allowed directories
        if safe:
            if not any(os.path.commonpath([dir, path]) == dir for dir in allowedDirs):
                self.qtHelper.Throw(
                    f"Refused to trash {path} because it's outside the allowed directories\n Please report this ",
                    date=True,
                    logger=self.General.logger,
                )
                return

        #   Check type
        if type == "file" and not os.path.isfile(path):
            self.debuggy(f"Refused to trash {path}: not a file", "trashedFiles")
            return
        if type == "folder" and not os.path.isdir(path):
            self.debuggy(f"Refused to trash {path}: not a folder", "trashedFiles")
            return
        if type == "any" and not os.path.exists(path):
            self.debuggy(f"Path does not exist: {path}", "trashedFiles")
            return

        if os.path.exists(path):
            try:
                send2trash(path)
                self.debuggy(f"Trashed: {path}", "trashedFiles")
            except Exception as e:
                self.debuggy(f"Failed to trash {path}: {str(e)}", "trashedFiles")
        else:
            self.debuggy(f"Path does not exist: {path}", "trashedFiles")

    def _getExtractors(self, withGeneral=True) -> list[ExtractorEntry]:
        """Get all extractors, this list is updated whenever one is added, removed etc
        Useful for making operations on all extractors

        Args:
            withGeneral (bool, optional): Also include General tab. Defaults to True.

        Returns:
            list[ExtractorEntry]: array of extractors with args 'ext' for the extractor object and
            'enabled' to tell if the extractor is enabled in it's settings
        """
        extractors = list(self.extractors)

        if withGeneral:
            extractors.insert(0, ExtractorEntry(self.General))

        return extractors

    def debuggy(self, string: str, classe: object | str, noFormat=False):
        """Call debugmanager only if the debug option is on

        Args:
            string (str): message
            classe (object | str): Name of the filename, if class it gets the class' name
            noFormat (bool, optional): Don't add date and format new lines correctly. Defaults to False
        """
        if self.debug:
            if isinstance(classe, str):
                value = classe
            else:
                value = classe.__class__.__name__

            self.debugManager.debug(f"{string}", value, noFormat)

    #   Window state changes
    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.isMinimized():
                if not self.General.config.settings["showtaskbar"]:
                    self.General.logger.debug("Window state: Qt.WindowType.Tool")
                    self.setWindowFlags(Qt.WindowType.Tool)
                    self.hide()
            elif not self.isMinimized():
                self.General.logger.debug("Window state: Qt.WindowType.Window")
                self.setWindowFlags(Qt.WindowType.Window)
                self.show()
        super().changeEvent(event)

    def closeEvent(self, event):
        for entry in self._getExtractors(False):
            ext = entry.ext

            if not ext.galleryRunner.running:
                continue

            reply = QMessageBox.question(
                self,
                f"{ext.fullName} is still running",
                f"\n{ext.fullName} is still running\nshut down anyways?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        try:
            self.General.logger.info(f"[{datetime.now()}] NA2000 tries to shut down...")
            self.loadingBar.terminate()
            self.extractorsManager.stopProcedure()
            self.hide()
            self.tray.stop()
            self.threadTimeCounter.stop()
            self.dataHelper.stop()
            self.crashHelper.stop()
            self.extractorsManager.savelogs()
            self.debugManager.closeAll()

            self.safeTrash(self.debugManager.debugDPath, "folder")
            self.safeTrash(self._tempDPath, "folder")
            self.safeTrash(self.exceptionFPath, "file")
            event.accept()
            sys.exit(0)

        except Exception as e:
            self.varHelper.exception(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            reply = QMessageBox.question(
                self,
                "Error shutting down",
                # type: ignore
                f"Exception {e}@{exc_tb.tb_lineno} \nStill exit? Changed settings might be lost",  # type: ignore
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
            else:
                event.accept()
                self.crashHelper.stop()
                self.extractorsManager.saveConfigs()

    #   Execute a function on the main thread
    #   Asks for a callable element in input and wraps it into a lambda function
    #   Emits the functions through threadHelper's signal
    def _inv(self, func: Callable[[], Any], *args):
        if func is None:
            self.cmd.error(f"ERROR: Tried to invoke None as a function (args={args})")
            return

        self.debuggy(f"{func}", "invoked")
        self.threadHelper.callFunction.emit(lambda: func(*args))

    def tray_showWindow(self):
        #   Force if it's tool
        if self.windowFlags() & Qt.WindowType.Tool:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.Tool)

        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)
        self.activateWindow()
        self.raise_()

    def _hideWinConsole(self):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        self.winConsole = False

    def _showWinConsole(self):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        self.winConsole = True

    def toggleWinConsole(self):
        if self.winConsole:
            QtHelper._hideWinConsole(self)
        else:
            QtHelper._showWinConsole(self)

    def tabSwitched(self, index):
        for entry in self._getExtractors():
            extractor = entry.ext
            tab = extractor.ui.tabWidget
            tab.setCurrentIndex(index)


class ThreadHelper(QObject):
    #   Signal to execute a function from the main thread
    callFunction = Signal(object)

    def __init__(self):
        super().__init__()
        self.callFunction.connect(self.execute_function, Qt.ConnectionType.QueuedConnection)

    @Slot(object)
    def execute_function(self, func):
        func()


if __name__ == "__main__":
    multiprocessing.freeze_support()

    def isRunning() -> bool:
        scriptPath = pathManager.getScriptDir()
        scriptPath = os.path.normpath(scriptPath).lower().replace(" ", "")
        scriptPath = hashlib.md5(scriptPath.encode()).hexdigest()
        mutexName = f"NA2000_{scriptPath}"
        logger.debug(f"[{datetime.now()}] Mutex: {mutexName}")
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutexName)
        return ctypes.windll.kernel32.GetLastError() == 183

    try:
        pathManager = PathManager(__file__)
        logger = CmdLogger(logDPath=pathManager.getExternalRes("saved/logs/")).getLogger()

        if isRunning():
            msg = "Naughty archiver 2000 is already running in the background"
            logger.warning(f"[{datetime.now()}] {msg} ")
            ctypes.windll.user32.MessageBoxW(0, msg, "Error", 0x10)
            sys.exit(1)

        mainPid = os.getpid()

        app = QApplication(sys.argv)
        crashHelper = CrashHelper(int(mainPid), "NA2000", os.path.join(pathManager.getScriptDir(), "saved", "logs"), logger)

        window = MainApp(logger, crashHelper, pathManager)
        app.exec()

    except Exception as e:
        #   If an early exception happens this will catch it and provide verbose information
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.warning(f"[{datetime.now()}] This program is borked: {e}")
        logger.warning(f"[{datetime.now()}] Exception type: {type(e).__name__}")  # type: ignore
        logger.warning(f"[{datetime.now()}] Line number: {exc_tb.tb_lineno}")  # type: ignore
        traceback.print_exc()

        try:
            crashHelper._handleCrash(crashHelper.title, crashHelper.logPath, list(crashHelper.pidList), crashHelper._log)

            crashHelper.stop()
            logger.warning(f"[{datetime.now()}] Killed registered gallery-dl processes")
        except Exception as e:
            subprocess.run(f"taskkill /F /IM gallery-dl.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.warning(f"[{datetime.now()}] Killed every gallery-dl process: {e}")

        print("Check saved/debug/ with the --debug flag")
        input("Check saved/logs/fault.log with the --debug flag")
        print("Check saved/logs/cmd.txt for full console output")
        sys.exit(1)
