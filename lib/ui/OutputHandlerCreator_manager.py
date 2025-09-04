from datetime import datetime
import json
import os
import re
from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QBrush, QKeySequence, QShortcut

from lib.VarHelper import VarHelper

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.ui.GeneralTab import General

from lib.Enums import EventNames, ExtractorState, Handlers, HandlersActions, LogLevel, MessageType, QColor
from lib.ui.OutputHandlerCreator_ui import Ui_Creator
from PySide6.QtWidgets import QWidget

import time
from PySide6.QtWidgets import QWidget, QListWidgetItem


class OutputHandlerCreator(QWidget):
    def __init__(self, main: "MainApp", general: "General") -> None:
        super().__init__(None)
        start = time.perf_counter()
        self.main = main
        self.inv = main._inv
        self.unlockDefaultEntries = False
        self.general = general

        self.ui = Ui_Creator()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Output Handler Creator")

        self.patternTemplate: dict[str, Any] = {
            Handlers.MATCH.name: "Match Me",
            Handlers.LINE_LEVEL.name: "WHITE",
            "VERSION": self.main.versionInt,
        }
        self.defaultPatterns = {}

        self.hiddenPatterns: list[dict[str, Any]] = [
            {
                Handlers.MATCH.name: r"rem Naughty Archiver, please",
                Handlers.LINE_LEVEL.name: LogLevel.GREY.name,
                Handlers.EVENT.name: EventNames.CONVERT_TO_GIF.name,
            },
            {Handlers.MATCH.name: r"warning", Handlers.LINE_LEVEL.name: LogLevel.YELLOW.name},
            {Handlers.MATCH.name: r" 503 ", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
            {Handlers.MATCH.name: r"\[debug\]", Handlers.LINE_LEVEL.name: LogLevel.GREY.name},
            {Handlers.MATCH.name: r"\[info\]", Handlers.LINE_LEVEL.name: LogLevel.WHITE.name},
            {Handlers.MATCH.name: r"\[error\]", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
            {Handlers.MATCH.name: r"timeout", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
        ]

        self.colors = {
            "RED": QColor(255, 205, 205),
            "YELLOW": QColor(255, 243, 205),
            "WHITE": QColor(255, 255, 255),
            "GREY": QColor(227, 227, 227),
            "OTHER": QColor(205, 255, 234),
            "GREEN": QColor(225, 255, 205),
            "MASK": QColor(100, 100, 100),
        }

        self.currentIndex = -1
        self.isModified = False
        self.inhibitBox = False

        #   Initialize Data
        self.patterns = []
        self.loadJson()

        #   Initialize UI
        self.setupConnections()
        self.populateComboBoxes()
        self.loadData()
        self.updateGroupBoxStates()
        self.main.cmd.debug(f" :{__name__}::__init__ ->{(time.perf_counter() - start) * 1000:.6f}ms")

    def closeEvent(self, event):
        # Save current entry if modified before saving all patterns
        if self.isModified and self.currentIndex >= 0:
            self.saveCurrentEntry()

        self.saveJson()
        self.main.extractorsManager.setOutputHandlerReloadingFlag()
        event.ignore()
        self.hide()

    def saveJson(self):
        with open(self.main.userOutputPatternsFPath, "w", encoding="utf-8") as f:
            json.dump(self.patterns, f, indent=4)
            os.fsync(f.fileno())
        self.main.debuggy(f"outputHandlerCreator_manager::saveJson -> {self.main.userOutputPatternsFPath}", self)
        self.main.debuggy(VarHelper.prettyJson(self.getCompiledPatterns(None)), "GalleryOutputHandler", noFormat=True)

    def getCompiledPatterns(self, extractor=None) -> list[tuple[re.Pattern[str], dict[str, Any]]]:
        if extractor:
            patterns = extractor.settings.getOutputHandlingCases()
            self.main.debuggy(f"Compiling {extractor.name} output handling patterns", extractor)
        else:
            patterns = self.patterns.copy()
            patterns.extend(self.hiddenPatterns)
            self.main.debuggy("Compiling output handling patterns", self)

        #   Create the tuple with the compiled pattern and the config dict
        compiled = []
        for config in patterns:
            cTuple = (re.compile(config[Handlers.MATCH.name]), config)
            if extractor:
                self.main.debuggy(f"-> {cTuple}", extractor)
            else:
                self.main.debuggy(f"-> {cTuple}", self)
            compiled.append(cTuple)
        return compiled

    def loadData(self):
        self.ui.listWidget.clear()
        self.currentIndex = -1

        #   Add entries to list widget
        for i, entry in enumerate(self.patterns):
            displayText = entry.get(Handlers.MATCH.name)
            _level = entry.get(Handlers.LINE_LEVEL.name)
            _mask = entry.get(Handlers.MASK.name)
            _isProtected = entry.get("DEFAULT")
            self.addListWidgetEntry(displayText, _level, _mask, _isProtected)

        #   Select first item if available
        if len(self.patterns) > 0:
            self.ui.listWidget.setCurrentRow(0)
            self.currentIndex = 0
            self.loadEntry(0)

        self.isModified = False
        self.updateGroupBoxStates()

    def initializeEmptyState(self):
        self.ui.listWidget.clear()
        self.currentIndex = -1
        self.isModified = False
        self.updateGroupBoxStates()
        self.blockSignals(True)
        self.ui.cfg_key.clear()
        self.ui.cfg_messageOnAction.clear()
        self.ui.cfg_messageOnLine.clear()
        self.ui.cfg_lineLevel.setCurrentIndex(0)
        self.ui.cfg_action.setCurrentIndex(0)
        self.ui.cfg_runEvent.setCurrentIndex(0)
        self.ui.cfg_mask.setCurrentIndex(0)
        self.ui.cfg_inhibitBox.setChecked(False)
        self.ui.cfg_actionNeverReset.setChecked(False)
        self.ui.cfg_actionAfterLinesSeen.setValue(2)
        self.ui.cfg_actionResetAt.setValue(1)
        self.blockSignals(False)

    def updateToNewVersion(self):
        defaultEntry = self.defaultPatterns[0]
        currentDefaultVersion = defaultEntry.get("VERSION", [0, 0, 0])
        if isinstance(currentDefaultVersion, str):
            currentDefaultVersion = [1, 2, 1]

        currentAppVersion = self.main.versionInt

        #   Rebuild default patterns if version is off
        if self.main.compareVer(currentDefaultVersion, currentAppVersion) >= 0:
            return

        for pattern in self.defaultPatterns:
            pattern["VERSION"] = self.main.versionInt
            pattern["DEFAULT"] = True

        with open(self.main.defaultOutputPatternsFPath, "w", encoding="utf-8") as f:
            json.dump(self.defaultPatterns, f, indent=4)
            os.fsync(f.fileno())

        #   Strip defaults from old list
        userEntries = [e for e in self.patterns if not e.get("DEFAULT", False)]

        #   Walk through old list, insert user entries in same positions
        merged = []
        userIndex = 0
        for entry in self.patterns:
            if entry.get("DEFAULT", False):
                continue
            merged.append(userEntries[userIndex])
            userIndex += 1

        #   Now interleave defaults around the preserved users
        merged = []
        userPositions = [i for i, e in enumerate(self.patterns) if not e.get("DEFAULT", False)]
        defaults = iter(self.defaultPatterns)
        for i in range(len(self.patterns)):
            if i in userPositions:
                merged.append(userEntries.pop(0))
            else:
                try:
                    merged.append(next(defaults))
                except StopIteration:
                    pass
        #   Append leftover defaults
        merged.extend(list(defaults))
        self.main.cmd.info(f"[{datetime.now()}] Updated output handler entries to new version")
        self.patterns = merged

    def loadJson(self):
        try:
            #   Load normally
            with open(self.main.userOutputPatternsFPath, "r", encoding="utf-8") as f:
                self.patterns = json.load(f)
                self.main.debuggy(f"outputHandlerCreator_manager::loadJson -> {self.main.userOutputPatternsFPath}", self)

            with open(self.main.defaultOutputPatternsFPath, "r", encoding="utf-8") as f:
                self.defaultPatterns = json.load(f)
                self.main.debuggy(f"outputHandlerCreator_manager::loadJson -> {self.main.defaultOutputPatternsFPath}", self)

            self.updateToNewVersion()

        except FileNotFoundError:
            #   First time, load default
            self.main.cmd.info(
                f"[{datetime.now()}] outputHandlerCreator_manager::loadJson -> File not found, loading default: {self.main.defaultOutputPatternsFPath}"
            )
            with open(self.main.defaultOutputPatternsFPath, "r", encoding="utf-8") as f:
                self.main.debuggy(f"Loaded default {self.main.defaultOutputPatternsFPath}", self)
                self.patterns = json.load(f)
            self.saveJson()
        except Exception as e:
            #   Fatal, close program
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"Error loading critical file: {e}, the program will quit")
            time.sleep(1)
            self.main.close()

    def setupConnections(self):
        #   Text boxes
        self.ui.cfg_key.textChanged.connect(self.onKeyChanged)
        self.ui.cfg_messageOnAction.textChanged.connect(lambda: self.markModified())
        self.ui.cfg_messageOnLine.textChanged.connect(lambda: self.markModified())

        #   Combo boxes
        self.ui.cfg_lineLevel.currentTextChanged.connect(lambda: self.markModified())
        self.ui.cfg_action.currentTextChanged.connect(lambda: self.markModified())
        self.ui.cfg_runEvent.currentTextChanged.connect(lambda: self.markModified())
        self.ui.cfg_mask.currentTextChanged.connect(lambda: self.markModified())

        #   Check boxes
        self.ui.cfg_inhibitBox.toggled.connect(lambda: self.markModified())

        #   Spin boxes
        self.ui.cfg_actionAfterLinesSeen.setRange(1, 20)
        self.ui.cfg_actionResetAt.setRange(1, 2000)

        self.ui.cfg_actionAfterLinesSeen.valueChanged.connect(lambda: self.markModified())
        self.ui.cfg_actionResetAt.valueChanged.connect(lambda: self.markModified())
        self.ui.cfg_actionNeverReset.toggled.connect(self.onNeverResetChanged)

        #   List widget
        self.ui.listWidget.currentRowChanged.connect(self.onEntrySelected)

        #   Buttons
        self.ui.btn_removeSelected.clicked.connect(self.removeSelectedEntry)
        self.ui.btn_newEntry.clicked.connect(self.addNewEntry)
        self.ui.btn_moveUp.clicked.connect(self.moveEntryUp)
        self.ui.btn_moveDown.clicked.connect(self.moveEntryDown)
        self.ui.btn_duplicateSelected.clicked.connect(self.duplicateSelectedEntry)

        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.saveCurrentEntry)
        self.main.qtHelper.setIcon(self, "FXSRESM_2101.ico")
        self.main.qtHelper.setIcon(self.ui.btn_removeSelected, "cryptui_3419.ico", size=(16, 16))
        self.main.qtHelper.setIcon(self.ui.btn_duplicateSelected, "imageres_5322.ico", size=(16, 16))
        self.main.qtHelper.setIcon(self.ui.btn_newEntry, "certmgr_444.ico", size=(16, 16))

    def populateComboBoxes(self):
        #   Line Level combo - store enum name as string, display description
        self.ui.cfg_lineLevel.clear()
        for level in LogLevel:
            enum_name = f"{level.name}"
            self.ui.cfg_lineLevel.addItem(level.string, enum_name)

        #   Action combo
        self.ui.cfg_action.clear()
        self.ui.cfg_action.addItem("Do nothing")
        for action in HandlersActions:
            enum_name = f"{action.name}"
            self.ui.cfg_action.addItem(action.desc, enum_name)

        #   Run Event combo
        self.ui.cfg_runEvent.clear()
        self.ui.cfg_runEvent.addItem("Nothing", None)
        for event in EventNames.comboBoxEvents():
            enum_name = f"{event.name}"
            self.ui.cfg_runEvent.addItem(event.name, enum_name)

        #   Mask combo - store enum name as string, display description
        self.ui.cfg_mask.clear()
        self.ui.cfg_mask.addItem("is running", None)
        for state in ExtractorState:
            if state == ExtractorState.IDLE:
                continue
            enum_name = f"{state.name}"
            self.ui.cfg_mask.addItem(state.desc, enum_name)

    def isCurrentEntryDefault(self) -> bool:
        """Check if the currently selected entry is a default entry"""
        if self.currentIndex < 0 or self.currentIndex >= len(self.patterns):
            return False
        return self.patterns[self.currentIndex].get("DEFAULT", False)

    def updateGroupBoxStates(self):
        hasEntries = len(self.patterns) > 0

        #   Basic enable/disable based on whether there are entries
        self.ui.leftSide.setEnabled(hasEntries)

        #   Check if current entry is default and not unlocked
        isDefaultAndLocked = hasEntries and self.isCurrentEntryDefault() and not self.unlockDefaultEntries

        #   Enable/disable the specific groupboxes based on default entry status
        self.ui.box_entry.setEnabled(hasEntries and not isDefaultAndLocked)
        self.ui.box_action.setEnabled(hasEntries and not isDefaultAndLocked)
        self.ui.box_mask.setEnabled(hasEntries and not isDefaultAndLocked)
        self.ui.box_event.setEnabled(hasEntries and not isDefaultAndLocked)
        self.ui.box_box.setEnabled(hasEntries and not isDefaultAndLocked)

    def markModified(self):
        # Only mark as modified if we're allowed to edit this entry
        if not self.isCurrentEntryDefault() or self.unlockDefaultEntries:
            self.isModified = True

    def onKeyChanged(self):
        self.markModified()

    def onNeverResetChanged(self, checked):
        self.ui.cfg_actionResetAt.setEnabled(not checked)
        self.markModified()

    def onEntrySelected(self, row):
        if row == -1:
            self.currentIndex = -1
            self.updateGroupBoxStates()
            return

        #   Save current entry if modified
        if self.isModified and self.currentIndex >= 0:
            self.saveCurrentEntry()

        #   Load selected entry - assign currentIndex to the actual row position
        if 0 <= row < len(self.patterns):
            self.currentIndex = row
            self.loadEntry(row)
            self.isModified = False
            self.updateGroupBoxStates()

    def createEntryFromTemplate(self):
        return self.patternTemplate.copy()

    def saveCurrentEntry(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.patterns):
            return

        #   Check if this is a default entry and we're not allowed to edit it
        if self.isCurrentEntryDefault() and not self.unlockDefaultEntries:
            return

        config = {}

        #   Preserve DEFAULT key if it existed in the original entry
        originalEntry = self.patterns[self.currentIndex]
        if originalEntry.get("DEFAULT", False):
            config["DEFAULT"] = True

        #   Key
        matchText = self.ui.cfg_key.text()
        config[Handlers.MATCH.name] = matchText

        #   Text fields
        messageOnAction = self.ui.cfg_messageOnAction.toPlainText().strip()
        if messageOnAction:
            config[Handlers.MESSAGE_ON_ACTION.name] = messageOnAction

        messageOnLine = self.ui.cfg_messageOnLine.toPlainText().strip()
        if messageOnLine:
            config[Handlers.MESSAGE_ON_LINE.name] = messageOnLine

        #   Line Level
        lineLevelData = self.ui.cfg_lineLevel.currentData()
        if lineLevelData:
            config[Handlers.LINE_LEVEL.name] = lineLevelData

        #   Inhibit box
        config[Handlers.INHIBIT_BOX.name] = self.ui.cfg_inhibitBox.isChecked()

        #   Action
        actionData = self.ui.cfg_action.currentData()
        if actionData:
            actionValue = [actionData, self.ui.cfg_actionAfterLinesSeen.value()]
            config[Handlers.ACTION.name] = actionValue

        #   Reset At
        if not self.ui.cfg_actionNeverReset.isChecked():
            config[Handlers.RESET_AT.name] = self.ui.cfg_actionResetAt.value()

        #   Event
        eventData = self.ui.cfg_runEvent.currentData()
        if eventData:
            config[Handlers.EVENT.name] = eventData

        #   Mask
        maskData = self.ui.cfg_mask.currentData()
        if maskData:
            config[Handlers.MASK.name] = maskData

        #   Version
        config["VERSION"] = self.main.versionInt

        self.patterns[self.currentIndex] = config

        #   Update list widget item text to match key
        item = self.ui.listWidget.item(self.currentIndex)
        if item and matchText:
            if maskData:
                color = self.colors.get("MASK")
                item.setForeground(QBrush(color))

            color = self.colors.get(lineLevelData.upper())
            item.setBackground(QBrush(color))

            item.setText(matchText)

        self.isModified = False

    def loadEntry(self, index):
        if index < 0 or index >= len(self.patterns):
            return

        config = self.patterns[index]

        #   Block signals to prevent marking as modified during loading
        self.blockSignals(True)

        self.ui.cfg_key.setText(config.get(Handlers.MATCH.name, ""))
        self.ui.cfg_messageOnAction.setPlainText(config.get(Handlers.MESSAGE_ON_ACTION.name, ""))
        self.ui.cfg_messageOnLine.setPlainText(config.get(Handlers.MESSAGE_ON_LINE.name, ""))
        self.ui.cfg_inhibitBox.setChecked(config.get(Handlers.INHIBIT_BOX.name, False))

        #   Load line level
        lineLevel = config.get(Handlers.LINE_LEVEL.name, "WHITE")
        for i in range(self.ui.cfg_lineLevel.count()):
            if self.ui.cfg_lineLevel.itemData(i) == lineLevel:
                self.ui.cfg_lineLevel.setCurrentIndex(i)
                break

        #   Load action
        action = config.get(Handlers.ACTION.name)
        if action:
            actionEnumName = action[0]
            for i in range(self.ui.cfg_action.count()):
                if self.ui.cfg_action.itemData(i) == actionEnumName:
                    self.ui.cfg_action.setCurrentIndex(i)
                    self.ui.cfg_actionAfterLinesSeen.setValue(action[1])
                    break
        else:
            self.ui.cfg_action.setCurrentIndex(0)  # "Do nothing"

        #   Load reset at
        resetAt = config.get(Handlers.RESET_AT.name)
        if resetAt is None:
            self.ui.cfg_actionNeverReset.setChecked(True)
            self.ui.cfg_actionResetAt.setEnabled(False)
        else:
            self.ui.cfg_actionNeverReset.setChecked(False)
            self.ui.cfg_actionResetAt.setEnabled(True)
            self.ui.cfg_actionResetAt.setValue(resetAt)

        #   Load event
        event = config.get(Handlers.EVENT.name)
        if event:
            for i in range(self.ui.cfg_runEvent.count()):
                data = self.ui.cfg_runEvent.itemData(i)
                if data == event:
                    self.ui.cfg_runEvent.setCurrentIndex(i)
                    break
        else:
            self.ui.cfg_runEvent.setCurrentIndex(0)  # "None"

        #   Load mask
        mask = config.get(Handlers.MASK.name)
        if mask:
            for i in range(self.ui.cfg_mask.count()):
                data = self.ui.cfg_mask.itemData(i)
                if data == mask:
                    self.ui.cfg_mask.setCurrentIndex(i)
                    break
        else:
            self.ui.cfg_mask.setCurrentIndex(0)  # "is running

        self.blockSignals(False)

    def loadTemplate(self):
        self.blockSignals(True)

        self.ui.cfg_key.setText(self.patternTemplate.get(Handlers.MATCH.name))
        self.ui.cfg_messageOnAction.setPlainText("")
        self.ui.cfg_messageOnLine.setPlainText("")

        templateLineLevel = self.patternTemplate.get(Handlers.LINE_LEVEL.name, "WHITE")
        for i in range(self.ui.cfg_lineLevel.count()):
            if self.ui.cfg_lineLevel.itemData(i) == templateLineLevel:
                self.ui.cfg_lineLevel.setCurrentIndex(i)
                break

        self.ui.cfg_inhibitBox.setChecked(self.patternTemplate.get(Handlers.INHIBIT_BOX.name, False))

        templateAction = self.patternTemplate.get(Handlers.ACTION.name)
        if templateAction:
            for i in range(self.ui.cfg_action.count()):
                if self.ui.cfg_action.itemData(i) == templateAction[0]:
                    self.ui.cfg_action.setCurrentIndex(i)
                    break

            self.ui.cfg_actionAfterLinesSeen.setValue(templateAction[1])

        #   Set defaults for event and mask
        self.ui.cfg_runEvent.setCurrentIndex(0)
        self.ui.cfg_mask.setCurrentIndex(0)

        self.blockSignals(False)

    def blockSignals(self, block):
        widgets = [
            self.ui.cfg_key,
            self.ui.cfg_messageOnAction,
            self.ui.cfg_messageOnLine,
            self.ui.cfg_lineLevel,
            self.ui.cfg_action,
            self.ui.cfg_runEvent,
            self.ui.cfg_mask,
            self.ui.cfg_inhibitBox,
            self.ui.cfg_actionNeverReset,
            self.ui.cfg_actionAfterLinesSeen,
            self.ui.cfg_actionResetAt,
        ]
        for widget in widgets:
            widget.blockSignals(block)

    def addNewEntry(self):
        if self.isModified and self.currentIndex >= 0:
            self.saveCurrentEntry()

        #   Create new entry from template
        newEntry = self.createEntryFromTemplate()

        current = self.ui.listWidget.currentRow()
        if current < 0:
            insertIndex = len(self.patterns)
        else:
            insertIndex = current

        self.patterns.insert(insertIndex, newEntry)

        #   Add to list widget
        _level = newEntry.get(Handlers.LINE_LEVEL.name, "WHITE")
        _mask = newEntry.get(Handlers.MASK.name)
        self.addListWidgetEntry("Match Me", _level, _mask, False, index=insertIndex)

        self.ui.listWidget.setCurrentRow(insertIndex)

        #   Assign currentIndex to the actual position where the item was inserted
        self.currentIndex = insertIndex
        self.loadTemplate()
        self.isModified = False
        self.updateGroupBoxStates()

    def duplicateSelectedEntry(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.patterns):
            return

        #   Save current entry if modified
        if self.isModified:
            self.saveCurrentEntry()

        #   Create duplicate
        duplicateEntry = self.patterns[self.currentIndex].copy()

        # Remove DEFAULT key from duplicated entry since it's now a user entry
        if "DEFAULT" in duplicateEntry:
            del duplicateEntry["DEFAULT"]

        if Handlers.MATCH.name in duplicateEntry:
            originalMatch = duplicateEntry[Handlers.MATCH.name]
            duplicateEntry[Handlers.MATCH.name] = f"{originalMatch} - Copy"

        self.patterns.append(duplicateEntry)

        #   Add to list widget
        displayText = duplicateEntry.get(Handlers.MATCH.name, "New Entry")
        _level = duplicateEntry.get(Handlers.LINE_LEVEL.name)
        _mask = duplicateEntry.get(Handlers.MASK.name)
        self.addListWidgetEntry(displayText, _level, _mask, False)

        #   Set currentIndex to the actual position of the new item
        newIndex = len(self.patterns) - 1
        self.ui.listWidget.setCurrentRow(newIndex)
        self.currentIndex = newIndex
        self.loadEntry(newIndex)
        self.isModified = False

    def removeSelectedEntry(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.patterns):
            return

        if self.patterns[self.currentIndex].get("DEFAULT") and not self.inhibitBox:
            self.main.qtHelper.Throw(
                "You are removing a default entry, it will get overwritten the next program update \nIf you want to replace the default entries for every update create an issue on github",
                type=MessageType.INFO,
            )
            self.inhibitBox = True

        del self.patterns[self.currentIndex]
        self.ui.listWidget.takeItem(self.currentIndex)

        #   Update current index to match actual positions
        if len(self.patterns) == 0:
            self.currentIndex = -1
        else:
            # If we removed the last item, move to previous
            if self.currentIndex >= len(self.patterns):
                self.currentIndex = len(self.patterns) - 1
            # currentIndex now points to the correct position

            self.ui.listWidget.setCurrentRow(self.currentIndex)
            self.loadEntry(self.currentIndex)

        self.isModified = False
        self.updateGroupBoxStates()

    def moveEntryUp(self):
        currentIndex = self.ui.listWidget.currentRow()
        if currentIndex <= 0:
            return

        if self.isModified:
            self.saveCurrentEntry()

        # Swap in patterns array
        self.patterns[currentIndex], self.patterns[currentIndex - 1] = (
            self.patterns[currentIndex - 1],
            self.patterns[currentIndex],
        )

        # Move in list widget
        item = self.ui.listWidget.takeItem(currentIndex)
        self.ui.listWidget.insertItem(currentIndex - 1, item)
        self.ui.listWidget.setCurrentRow(currentIndex - 1)

        # Update currentIndex to the new actual position
        self.currentIndex = currentIndex - 1

    def moveEntryDown(self):
        currentIndex = self.ui.listWidget.currentRow()
        if currentIndex < 0 or currentIndex >= len(self.patterns) - 1:
            return

        if self.isModified:
            self.saveCurrentEntry()

        # Swap in patterns array
        self.patterns[currentIndex], self.patterns[currentIndex + 1] = (
            self.patterns[currentIndex + 1],
            self.patterns[currentIndex],
        )

        # Move in list widget
        item = self.ui.listWidget.takeItem(currentIndex)
        self.ui.listWidget.insertItem(currentIndex + 1, item)
        self.ui.listWidget.setCurrentRow(currentIndex + 1)

        # Update currentIndex to the new actual position
        self.currentIndex = currentIndex + 1

    def getJsonOutput(self):
        #   Save current entry if modified
        if self.isModified and self.currentIndex >= 0:
            self.saveCurrentEntry()

        return self.patterns.copy()

    def loadJsonData(self, data):
        self.patterns = data.copy() if isinstance(data, list) else []

        self.ui.listWidget.clear()

        #   Add entries to list widget
        for entry in self.patterns:
            displayText = entry.get(Handlers.MATCH.name, "Entry")
            _level = entry.get(Handlers.LINE_LEVEL.name)
            _mask = entry.get(Handlers.MASK.name)
            _protected = entry.get("DEFAULT")
            self.addListWidgetEntry(displayText, _level, _mask, _protected)

        #   Select first item if available
        if len(self.patterns) > 0:
            self.ui.listWidget.setCurrentRow(0)
            self.currentIndex = 0  # Set to actual position of first item
        else:
            self.currentIndex = -1

        self.isModified = False
        self.updateGroupBoxStates()

    def addListWidgetEntry(self, text: str, levelValue: str, mask, isProtected: bool, index=None):
        if isProtected:
            string = f"(Protected) {text}"
        else:
            string = text

        item = QListWidgetItem(string)

        if mask:
            color = self.colors.get("MASK")
            item.setForeground(QBrush(color))

        color = self.colors.get(levelValue.upper())
        item.setBackground(QBrush(color))

        if index is None:
            self.ui.listWidget.addItem(item)
        else:
            self.ui.listWidget.insertItem(index, item)
