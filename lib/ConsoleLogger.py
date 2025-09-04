from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, QObject, Qt

from lib.Enums import LogLevel

if TYPE_CHECKING:
    from na2000 import MainApp

from PySide6.QtWidgets import QApplication, QTextEdit
from PySide6.QtGui import QTextCursor
from datetime import datetime
import os
from PySide6.QtGui import QTextCursor, QTextBlockFormat
import time


class ConsoleLogger:
    def __init__(self, main: "MainApp", textbox: QTextEdit, logPath: str, extractorName: str, currentConfiguration: dict):
        start = time.perf_counter()
        self.main = main
        self.textbox = textbox
        self.textbox.wheelEvent = self.customWheelEvent
        self.logDPath = logPath
        self.extractorName = extractorName
        self.logFPath = os.path.join(self.logDPath, f"{datetime.now().strftime('%Y-%m-%d')}_{self.extractorName}.txt")
        self.logEntries = []
        self.loading = main.loadingBar

        self.enabledLevels = {
            LogLevel.WHITE: currentConfiguration["consoleshowinfo"],
            LogLevel.YELLOW: currentConfiguration["consoleshowalerts"],
            LogLevel.RED: currentConfiguration["consoleshowerrors"],
            LogLevel.OTHER: currentConfiguration["consoleshowothers"],
            LogLevel.GREY: currentConfiguration["consoleshowdebug"],
            LogLevel.GREEN: currentConfiguration["consoleshowsuccess"],
        }
        self._setFixedLineHeight()
        self.main.cmd.debug(f" :{__name__}::__init__ ->{(time.perf_counter() - start) * 1000:.6f}ms")

    def customWheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            return
        QTextEdit.wheelEvent(self.textbox, event)

    def log(self, message, msgType: str | LogLevel = LogLevel.WHITE):
        if not isinstance(msgType, LogLevel):
            msgType = msgType.split(".")[-1]
            msgType = LogLevel.__members__.get(msgType, LogLevel.OTHER)

        color = msgType.color
        num = msgType.num

        timestamp = datetime.now().strftime("%m-%d/%H:%M:%S")
        logEntry = f"[{num}][{timestamp}]: {message}"
        maxLogNum = self.main.General.config.settings["maxlogentries"]
        self.trim(maxLogNum)

        self.logEntries.append((logEntry, msgType, color))
        self.appendLog(logEntry)

        if msgType in self.enabledLevels and self.enabledLevels[msgType]:
            self._addToTextbox(logEntry, color)

    def _addToTextbox(self, logEntry, color):
        vScrollbar = self.textbox.verticalScrollBar()
        hScrollbar = self.textbox.horizontalScrollBar()
        atBottom = vScrollbar.value() >= (vScrollbar.maximum() - 2)
        hPosition = hScrollbar.value()

        cursor = self.textbox.textCursor()
        hasSelection = cursor.hasSelection()
        if hasSelection:
            selectionStart = cursor.selectionStart()
            selectionEnd = cursor.selectionEnd()
            cursor.clearSelection()
            self.textbox.setTextCursor(cursor)

        self.textbox.setTextColor(color)
        self.textbox.append(logEntry)

        if hasSelection:
            cursor = self.textbox.textCursor()
            cursor.setPosition(selectionStart)
            cursor.setPosition(selectionEnd, QTextCursor.MoveMode.KeepAnchor)
            self.textbox.setTextCursor(cursor)

        hScrollbar.setValue(hPosition)
        if atBottom:
            vScrollbar.setValue(vScrollbar.maximum())

    def trim(self, limit):
        doc = self.textbox.document()
        blockCount = doc.blockCount()
        if blockCount <= limit:
            return

        vScrollbar = self.textbox.verticalScrollBar()
        hScrollbar = self.textbox.horizontalScrollBar()
        atBottom = vScrollbar.value() >= (vScrollbar.maximum() - 2)
        hPosition = hScrollbar.value()

        cursor = self.textbox.textCursor()
        hasSelection = cursor.hasSelection()
        if hasSelection:
            selectionStart = cursor.selectionStart()
            selectionEnd = cursor.selectionEnd()

        if len(self.logEntries) > limit:
            self.logEntries = self.logEntries[-limit:]

        cursor = QTextCursor(doc)
        cursor.movePosition(QTextCursor.MoveOperation.Start)

        for _ in range(blockCount - limit):
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock, QTextCursor.MoveMode.KeepAnchor)

        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.endEditBlock()

        if hasSelection:
            removedChars = cursor.position()
            newSelectionStart = max(0, selectionStart - removedChars)
            newSelectionEnd = max(0, selectionEnd - removedChars)
            if newSelectionStart < newSelectionEnd:
                cursor = self.textbox.textCursor()
                cursor.setPosition(newSelectionStart)
                cursor.setPosition(newSelectionEnd, QTextCursor.MoveMode.KeepAnchor)
                self.textbox.setTextCursor(cursor)

        hScrollbar.setValue(hPosition)
        if atBottom:
            vScrollbar.setValue(vScrollbar.maximum())

    def info(self, message: str):
        self.log(message, LogLevel.WHITE)

    def alert(self, message: str):
        self.log(message, LogLevel.YELLOW)

    def warning(self, message: str):
        self.alert(message)

    def error(self, message: str):
        self.log(message, LogLevel.RED)

    def other(self, message: str):
        self.log(message, LogLevel.OTHER)

    def debug(self, message: str):
        self.log(message, LogLevel.GREY)

    def success(self, message: str):
        self.log(message, LogLevel.GREEN)

    def appendLog(self, text: str):
        try:
            if not os.path.exists(self.logDPath):
                os.makedirs(self.logDPath)

            with open(self.logFPath, "a", encoding="utf-8") as logFile:
                logFile.write(f"{text}\n")
            return True
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"[{datetime.now()}] Error saving log: {str(e)}")

    def saveLog(self):
        try:
            if not os.path.exists(self.logDPath):
                os.makedirs(self.logDPath)

            full_log = "\n".join([entry[0] for entry in self.logEntries])
            file_exists = os.path.isfile(self.logFPath)

            with open(self.logFPath, "a", encoding="utf-8") as logFile:
                if file_exists:
                    logFile.write(f"\n?Log append at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                logFile.write(full_log)
            return True
        except Exception as e:
            self.log(f"Error saving log: {str(e)}", LogLevel.RED)
            return False

    def clear(self):
        self.textbox.clear()
        self.logEntries = []

    def setLevelVisibility(self, levelName: LogLevel, value: bool):
        if levelName in self.enabledLevels:
            self.enabledLevels[levelName] = value
            self._refreshDisplay()

    def _refreshDisplay(self):
        self.textbox.setUpdatesEnabled(False)

        #   -   -   Scrollbar
        vScrollbar = self.textbox.verticalScrollBar()
        hScrollbar = self.textbox.horizontalScrollBar()
        atBottom = vScrollbar.value() >= (vScrollbar.maximum() - 2)
        hPosition = hScrollbar.value()
        #   -   -   Scrollbar

        cursor = self.textbox.textCursor()
        hasSelection = cursor.hasSelection()
        if hasSelection:
            selectionStart = cursor.selectionStart()
            selectionEnd = cursor.selectionEnd()

        self.textbox.clear()
        self._setFixedLineHeight()

        if len(self.logEntries) > 500:
            self.debug(f"Filtering {len(self.logEntries)} entries")

        self.loading.start(len(self.logEntries), "Filtering output", 100, minimum=500)
        for i, (entry, level, color) in enumerate(self.logEntries, 1):
            if level in self.enabledLevels and self.enabledLevels[level]:
                self.textbox.setTextColor(color)
                self.textbox.append(entry)
            self.loading.increase(1)
            if i % 1000 == 0:
                QApplication.processEvents()
        self.loading.terminate()

        #   -   -   Scrollbar
        if hasSelection:
            docLength = self.textbox.document().characterCount()
            if selectionStart < docLength and selectionEnd <= docLength:
                cursor = self.textbox.textCursor()
                cursor.setPosition(selectionStart)
                cursor.setPosition(selectionEnd, QTextCursor.MoveMode.KeepAnchor)
                self.textbox.setTextCursor(cursor)

        hScrollbar.setValue(hPosition)
        if atBottom:
            vScrollbar.setValue(vScrollbar.maximum())
        else:
            vScrollbar.setValue(min(vScrollbar.value(), vScrollbar.maximum()))
        #   -   -   Scrollbar

        self.textbox.setUpdatesEnabled(True)

    def _setFixedLineHeight(self):
        cursor = self.textbox.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)

        format = QTextBlockFormat()
        format.setLineHeight(12, 2)
        cursor.setBlockFormat(format)

        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.textbox.setTextCursor(cursor)

    def _showLevels(self, enabledLevels):
        self.enabledLevels = {
            LogLevel.WHITE: enabledLevels[0],
            LogLevel.YELLOW: enabledLevels[1],
            LogLevel.RED: enabledLevels[2],
            LogLevel.OTHER: enabledLevels[3],
            LogLevel.GREY: enabledLevels[4],
            LogLevel.GREEN: enabledLevels[5],
        }
        self._refreshDisplay()
