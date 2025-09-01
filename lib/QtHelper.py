from datetime import datetime
from typing import TYPE_CHECKING

from lib.Enums import MessageType

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.ConsoleLogger import ConsoleLogger

from PySide6.QtWidgets import QMessageBox, QFileDialog, QPushButton, QTabWidget, QToolButton, QLabel, QWidget
import ctypes
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
import os
import time

from PySide6.QtCore import QObject


class QtHelper(QObject):
    def __init__(self, main: "MainApp"):
        super().__init__()
        start = time.perf_counter()
        self.main = main
        self.inv = main._inv
        self.iconsDPath = main._iconsPath

        main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def Throw(
        self,
        message: str,
        logger: "ConsoleLogger" = None,  # type: ignore
        title: str | None = None,
        type: MessageType = MessageType.CRITICAL,
        parent=None,
        date=False,
    ):
        #   Log message if logger is given
        self.main.debuggy("Throw BOX:", self)
        self.main.debuggy(f"Message: {message}", self)
        self.main.debuggy(f"logger: {logger}", self)
        self.main.debuggy(f"title: {title}", self)
        self.main.debuggy(f"type: {type}", self)
        self.main.debuggy(f"date: {date}", self)

        if logger:
            logMessage = message.replace("\n", " ").replace("\r", " ")

            if date:
                logMessage = f"[{datetime.now()}] {logMessage} "

            logger.log(logMessage, type.logLevel)

        def func():
            dialogParent = parent if parent else self.main
            windowTitle = title if title else type.name.capitalize()

            #   Create custom message box
            msgBox = QMessageBox(dialogParent)
            msgBox.setWindowTitle(windowTitle)
            msgBox.setText(message)

            if type == MessageType.CRITICAL:
                msgBox.setIcon(QMessageBox.Icon.Critical)
            elif type == MessageType.WARNING:
                msgBox.setIcon(QMessageBox.Icon.Warning)
            else:
                msgBox.setIcon(QMessageBox.Icon.Information)

            msgBox.setWindowFlags(msgBox.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)

            msgBox.show()
            msgBox.activateWindow()
            msgBox.raise_()
            msgBox.exec_()

        self.main.threadHelper.callFunction.emit(func)

    @staticmethod
    def browseFolder(editWidget, parent, current=""):
        folder = QFileDialog.getExistingDirectory(parent, "Select Destination Folder", current, QFileDialog.Option.ShowDirsOnly)
        if folder:
            editWidget.setText(folder)
            editWidget.editingFinished.emit()

    @staticmethod
    def _hideWinConsole(window):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        window.winConsole = False

    @staticmethod
    def _showWinConsole(window):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        window.winConsole = True

    @staticmethod
    def removeExtractorTabByName(tab_name, tab):
        try:
            widget = tab
            #   Search through all tabs
            for index in range(widget.count()):
                if widget.tabText(index) == tab_name:
                    widget.removeTab(index)
                    return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def removeCurrentExtractorTab(tab):
        index = tab.currentIndex()
        if index != -1:
            tab.removeTab(index)

    def setIcon(self, widget, name, size: tuple[int, int] = (24, 24), index=None):
        self.main.debuggy(f"QtHelper::setIcon -> {name} {size}", self)
        path = os.path.join(self.iconsDPath, name)

        if not os.path.exists(path):
            self.main.cmd.error(f"[{datetime.now()}] QtHelper::setIcon -> Icon not found at {path}")
            return

        icon = QIcon(path)
        qsize = QSize(size[0], size[1])

        if isinstance(widget, QPushButton):
            widget.setIcon(icon)
            widget.setIconSize(qsize)
        elif isinstance(widget, QToolButton):
            widget.setIcon(icon)
            widget.setIconSize(qsize)
        elif isinstance(widget, QTabWidget):
            if widget.count() == 0:
                raise ValueError("QTabWidget has no tabs to add an icon to.")
            target_index = index if index is not None else widget.count() - 1
            widget.setTabIcon(target_index, icon)
        elif isinstance(widget, QWidget):
            widget.setWindowIcon(icon)
        else:
            raise ValueError(f"Unsupported widget type {type(widget)}. Expected QPushButton, QToolButton, QLabel, QAction, or QTabWidget.")
