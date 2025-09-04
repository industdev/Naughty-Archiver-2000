from typing import TYPE_CHECKING, Literal

from lib.ConfigManager import Config
from lib.Enums import MessageType, Table, Validation

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor

from PySide6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QHeaderView,
    QAbstractItemView,
    QCheckBox,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QAbstractItemView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QKeySequence, QShortcut, QFont
from lib.VarHelper import VarHelper
from lib.ui.UserTable_ui import Ui_UserTable

from datetime import datetime
import time
import sys
import os
import json


class UserTable(QWidget):
    def __init__(self, main: "MainApp", extractor: "Extractor"):
        try:
            start = time.perf_counter()
            super().__init__(None)
            self.main = main
            self.inv = main._inv

            self.ui = Ui_UserTable()
            self.ui.setupUi(self)
            self.setWindowTitle(f"{extractor.name} users")

            self.table = self.ui.cfgui_tableWidget
            self.addtable = self.ui.cfgui_addtable

            self.saveDir = extractor.usersFPath
            self.logger = extractor.logger
            self.extractor = extractor
            self.save = True
            self.config = Config(main, {"users": []}, self.saveDir, f"{self.extractor.name}Users", self)
            self.list = self.config.settings["users"]  # Always points to self.config.settings["users"]

            self.ui.combo_insertPlace.setCurrentIndex(self.main.General.config.settings["comboboxIndex"])
            self.ui.btn_moveUp.clicked.connect(self.moveCheckedRowsUp)
            self.ui.btn_moveDown.clicked.connect(self.moveCheckedRowsDown)
            self.ui.btn_removeUser.clicked.connect(self.removeCheckedRows)
            self.ui.btn_insertUser.clicked.connect(self.insertUser)
            self.ui.btn_duplicateUser.clicked.connect(self.duplicateSelectedRows)
            self.ui.btn_exportList_2.clicked.connect(self.exportTable)
            self.ui.btn_importList_2.clicked.connect(self.importTable)
            self.ui.btn_saveClose.clicked.connect(self.saveClose)
            self.ui.btn_discardClose.clicked.connect(self.discardClose)

            # self.main.qtHelper.setIcon(self.ui.combo_insertPlace, 'imageres_5312.ico')
            self.main.qtHelper.setIcon(self.ui.btn_removeUser, "aclui_126.ico")
            self.main.qtHelper.setIcon(self.ui.btn_insertUser, "dsuiext_4121.ico")
            self.main.qtHelper.setIcon(self.ui.btn_duplicateUser, "aclui_127.ico")
            self.main.qtHelper.setIcon(self.ui.btn_exportList_2, "FXSRESM_5034.ico")
            self.main.qtHelper.setIcon(self.ui.btn_importList_2, "FXSRESM_5035.ico")
            self.main.qtHelper.setIcon(self.ui.btn_saveClose, "cryptui_3421.ico")
            self.main.qtHelper.setIcon(self.ui.btn_discardClose, "cryptui_3422.ico")
            self.main.qtHelper.setIcon(self, "explorer_261.ico")

            self.extractor = extractor

            self.tableTemplate = extractor.tableTemplate
            self.comboTemplate = extractor.comboTemplate

            self.addtableTemplate = []
            for row in self.tableTemplate:
                if row[0] == Table.SHOW:
                    self.addtableTemplate.append(row)

            self.stylesheetQPushbutton = """
                QPushButton {
                    background-color: #F0F0F0;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;  /* Lighter on hover */
                }
                QPushButton:pressed {
                    background-color: #D0D0D0;  /* Darker when pressed */
                }
            """

            self.stylesheetAddTable = """
                QTableWidget {
                    gridline-color: #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                }
                QTableWidget::item:selected {
                    background-color: #ededed;
                    color: black;

                }
                QPushButton {
                    min-width: 0;
                    padding: 0;
                    margin: 0;
                }
            """
            self.stylesheetTable = """
                QTableWidget {
                    gridline-color: #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                }
                QTableWidget::item:selected {
                    background-color: #ededed;
                    color: black;
                }
            """
            self.setupTable()
            self.setupAddTable()
            self.setupShortcuts()
            self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")
        except Exception as e:
            raise Exception(f"Failed to load the users table: {e}")

    def saveClose(self):
        try:
            comboboxIndex = self.ui.combo_insertPlace.currentIndex()
            self.main.General.config.settings["comboboxIndex"] = comboboxIndex
            self.main.General.logger.other(f"Saved General.comboboxIndex with value {comboboxIndex}")

            self.save = True
            self.close()
        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Table: Error during the save procedure: {e}")

    def discardClose(self):
        self.save = False
        self.close()

    def closeEvent(self, event):
        if self.save:
            self.saveTable()

        self.save = True

        event.ignore()
        self.hide()

    def setupShortcuts(self):
        """
        Sets up keyboard shortcuts for user table management actions.
        """
        #   General shortcuts
        QShortcut(QKeySequence("Ctrl+A"), self).activated.connect(self.selectAll)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.unselectAll)

        #   Move rows
        QShortcut(QKeySequence("Ctrl+Up"), self).activated.connect(self.moveCheckedRowsUp)
        QShortcut(QKeySequence("Ctrl+Down"), self).activated.connect(self.moveCheckedRowsDown)

        #   Modify users
        QShortcut(QKeySequence("Del"), self).activated.connect(self.removeCheckedRows)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.insertUser)
        QShortcut(QKeySequence("Ctrl+Shift+D"), self).activated.connect(self.duplicateSelectedRows)

        #   Import/export
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(self.exportTable)
        QShortcut(QKeySequence("Ctrl+I"), self).activated.connect(self.importTable)

        #   Save or discard
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.saveClose)
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.discardClose)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.saveClose)

    def setupAddTable(self):
        self.addtable.setStyleSheet(self.stylesheetAddTable)

        #   Define columns
        headers = []
        for row in self.addtableTemplate:
            value = row[2]
            if value is None:
                value = ""
            headers.append(str(value))

        self.addtable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.addtable.setColumnCount(len(headers))
        self.addtable.setHorizontalHeaderLabels(headers)
        self.addtable.setSortingEnabled(False)
        self.addtable.insertRow(0)

        for column in range(len(self.addtableTemplate)):
            widgetType = self.addtableTemplate[column][1]

            #   widgetType check
            if widgetType == Table.CHECKBOX:
                self._insertCheckbox(self.addtable, 0, column, 0)
            elif widgetType == Table.COMBO:
                self._insertCombobox(self.addtable, 0, column, 0)
            elif widgetType == Table.DESTINATION:
                self._insertDestinationBrowser(self.addtable, 0, column)
            elif widgetType == Table.AUTOTIMESTAMP:
                self._insertAutoTimestampButton(self.addtable, 0, column)
            elif widgetType == Table.SQLDELETER:
                self._insertSqlDeleteButton(self.addtable, 0, column)
            elif widgetType == Table.TEXTBOX:
                self._insertText(self.addtable, 0, column, "", True)
            else:
                raise Exception(f"Unknown Widget Type {widgetType}")

        self.addtable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.addtable.horizontalHeader().setStretchLastSection(True)
        self.addtable.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

    def setupTable(self):
        self.table.setRowCount(0)
        self.table.verticalHeader().setDefaultSectionSize(19)
        self.table.setStyleSheet(self.stylesheetTable)

        #   Define columns
        headers = []
        for row in self.tableTemplate:
            value = row[2]
            if value is None:
                value = ""
            headers.append(str(value))

        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.list))
        self.table.setSortingEnabled(False)

        #   For each user (row)
        for row, user in enumerate(self.list):
            #   For each column defined in the custom table
            for column in range(len(self.tableTemplate)):
                widgetType = self.tableTemplate[column][1]
                jsonKeyName = self.tableTemplate[column][3]
                defaultValue = self.tableTemplate[column][4]

                if jsonKeyName == None:
                    jsonValue = False
                else:
                    try:
                        jsonValue = user[f"{jsonKeyName}"]
                    except KeyError:
                        user[jsonKeyName] = defaultValue
                        jsonValue = user[jsonKeyName]

                #   widgetType check
                if widgetType == Table.CHECKBOX:
                    #   Insert skip checkbox that changes the background of the row
                    if column == 1:
                        self._insertCheckbox(self.table, row, column, jsonValue, faintRowStyle=True)
                    else:
                        self._insertCheckbox(self.table, row, column, jsonValue)

                elif widgetType == Table.COMBO:
                    self._insertCombobox(self.table, row, column, jsonValue)
                elif widgetType == Table.DESTINATION:
                    self._insertDestinationBrowser(self.table, row, column)
                elif widgetType == Table.AUTOTIMESTAMP:
                    self._insertAutoTimestampButton(self.table, row, column)
                elif widgetType == Table.SQLDELETER:
                    self._insertSqlDeleteButton(self.table, row, column)
                elif widgetType == Table.TEXTBOX:
                    self._insertText(self.table, row, column, str(jsonValue), True)
                else:
                    raise Exception(f"Unknown Widget Type {widgetType}")

        self._refreshAllRowStyles()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)

    def _refreshAllRowStyles(self):
        for row in range(self.table.rowCount()):
            skip = False
            widget = self.table.cellWidget(row, 1)
            cb = widget.findChild(QCheckBox)
            if cb:
                skip = cb.isChecked()

            self._updateRowStyle(self.table, row, skip)

    def insertUser(self):
        data = {}
        for column in range(len(self.addtableTemplate)):
            widgetType = self.addtableTemplate[column][1]
            jsonKeyName = self.addtableTemplate[column][3]

            if widgetType == Table.CHECKBOX:
                data[f"{jsonKeyName}"] = bool(self.addtable.cellWidget(0, column).findChild(QCheckBox).isChecked())  # type: ignore
            elif widgetType == Table.COMBO:
                data[f"{jsonKeyName}"] = int(self.addtable.cellWidget(0, column).currentIndex())  # type: ignore
            elif widgetType == Table.TEXTBOX:
                data[f"{jsonKeyName}"] = str(self.addtable.item(0, column).text())  # type: ignore
            elif widgetType in [Table.DESTINATION, Table.AUTOTIMESTAMP, Table.SQLDELETER]:
                pass
            else:
                raise Exception(f"Unknown Widget Type {widgetType}")

        for column in range(len(self.tableTemplate)):
            jsonKeyName = self.tableTemplate[column][3]
            isOnAddtable = self.tableTemplate[column][0]
            defaultValue = self.tableTemplate[column][4]
            if isOnAddtable == Table.HIDE:
                data[f"{jsonKeyName}"] = defaultValue
            else:
                continue

        index = self._getComboIndex()
        self.insertRowFromData(data, index)

    def _getComboIndex(self):
        #   Top,    Middle,     Bottom

        if self.ui.combo_insertPlace.currentIndex() == 0:
            index = 0
        elif self.ui.combo_insertPlace.currentIndex() == 1:
            index = self.ui.cfgui_tableWidget.rowCount() / 2
        else:
            index = self.ui.cfgui_tableWidget.rowCount()
        return index

    def getCheckedRows(self):
        return [
            row
            for row in range(self.table.rowCount())
            if self.table.cellWidget(row, 0).findChild(QCheckBox).isChecked()  # type: ignore
        ]

    def _saveRowData(self, row):
        data = {}

        for column in range(len(self.tableTemplate)):
            widgetType = self.tableTemplate[column][1]
            jsonKeyName = self.tableTemplate[column][3]

            if widgetType == Table.CHECKBOX:
                data[f"{jsonKeyName}"] = bool(self.table.cellWidget(row, column).findChild(QCheckBox).isChecked())  # type: ignore
            elif widgetType == Table.COMBO:
                data[f"{jsonKeyName}"] = int(self.table.cellWidget(row, column).currentIndex())  # type: ignore
            elif widgetType == Table.TEXTBOX:
                data[f"{jsonKeyName}"] = str(self.table.item(row, column).text())  # type: ignore

        return data

    def insertRowFromData(self, data, row):
        try:
            self.table.insertRow(row)
            self.main.debuggy(f"insertRowFromData -> {data=}, {row=}", self)

            #   For each column defined in the custom table
            for column in range(len(self.tableTemplate)):
                widgetType = self.tableTemplate[column][1]
                jsonKeyName = self.tableTemplate[column][3]
                self.main.debuggy(f" :{widgetType=}, {jsonKeyName=}", self)

                if jsonKeyName == None:
                    jsonValue = False
                else:
                    jsonValue = data[f"{jsonKeyName}"]

                #   widgetType check
                if widgetType == Table.CHECKBOX:
                    #   Insert skip checkbox that changes the background of the row
                    if column == 1:
                        self._insertCheckbox(self.table, row, column, jsonValue, faintRowStyle=True, update=True)
                    else:
                        self._insertCheckbox(self.table, row, column, jsonValue)
                elif widgetType == Table.COMBO:
                    self._insertCombobox(self.table, row, column, jsonValue)
                elif widgetType == Table.DESTINATION:
                    self._insertDestinationBrowser(self.table, row, column)
                elif widgetType == Table.AUTOTIMESTAMP:
                    self._insertAutoTimestampButton(self.table, row, column)
                elif widgetType == Table.TEXTBOX:
                    self._insertText(self.table, row, column, str(jsonValue), True)
                elif widgetType == Table.SQLDELETER:
                    self._insertSqlDeleteButton(self.table, row, column)
                else:
                    raise Exception(f"Unknown Widget Type {widgetType}")

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Table: There was an error inserting the row from data: {e}")

    def duplicateSelectedRows(self):
        rows = self.getCheckedRows()
        for row in reversed(rows):
            data = self._saveRowData(row)
            self.insertRowFromData(data, row)

    def updateRowFromData(self, data, row):
        try:
            self.main.debuggy(f"updateRowFromData -> {data=}, {row=}", self)
            for column in range(len(self.tableTemplate)):
                widgetType = self.tableTemplate[column][1]
                jsonKeyName = self.tableTemplate[column][3]
                self.main.debuggy(f" :{widgetType=}, {jsonKeyName=}", self)

                if widgetType == Table.CHECKBOX:
                    self._updateCheckbox(self.table, row, column, bool(data[f"{jsonKeyName}"]))
                elif widgetType == Table.COMBO:
                    self._updateCombobox(self.table, row, column, int(data[f"{jsonKeyName}"]))
                elif widgetType == Table.TEXTBOX:
                    self._updateText(self.table, row, column, str(data[f"{jsonKeyName}"]))
                elif widgetType in [Table.DESTINATION, Table.AUTOTIMESTAMP, Table.SQLDELETER]:
                    pass
                else:
                    raise Exception(f"Unknown Widget Type {widgetType}")

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Table: There was an error updating the row from data: {e}")

    def _moveRowUp(self, row):
        if row <= 0:
            return

        #   Save row data
        current_data = self._saveRowData(row)
        above_data = self._saveRowData(row - 1)
        current_checked = self.table.cellWidget(row, 0).findChild(QCheckBox).isChecked()  # type: ignore
        above_checked = self.table.cellWidget(row - 1, 0).findChild(QCheckBox).isChecked()  # type: ignore

        #   Swap data
        self.updateRowFromData(current_data, row - 1)
        self.updateRowFromData(above_data, row)
        self.table.cellWidget(row - 1, 0).findChild(QCheckBox).setChecked(current_checked)  # type: ignore
        self.table.cellWidget(row, 0).findChild(QCheckBox).setChecked(above_checked)  # type: ignore

    def _moveRowDown(self, row):
        if row >= self.table.rowCount() - 1:
            return

        current_data = self._saveRowData(row)
        below_data = self._saveRowData(row + 1)

        current_checked = self.table.cellWidget(row, 0).findChild(QCheckBox).isChecked()  # type: ignore
        below_checked = self.table.cellWidget(row + 1, 0).findChild(QCheckBox).isChecked()  # type: ignore

        self.updateRowFromData(current_data, row + 1)
        self.updateRowFromData(below_data, row)

        self.table.cellWidget(row + 1, 0).findChild(QCheckBox).setChecked(current_checked)  # type: ignore
        self.table.cellWidget(row, 0).findChild(QCheckBox).setChecked(below_checked)  # type: ignore

    def moveCheckedRowsUp(self):
        rows = self.getCheckedRows()
        if not rows:
            return

        for row in rows:
            self._moveRowUp(row)

    def moveCheckedRowsDown(self):
        rows = self.getCheckedRows()
        if not rows:
            return

        for row in reversed(rows):
            self._moveRowDown(row)

    def unselectAll(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(False)

    def selectAll(self):
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(True)

    def removeCheckedRows(self):
        rows = self.getCheckedRows()
        if not rows:
            return

        for row in reversed(rows):
            self.table.removeRow(row)

    def _insertCheckbox(self, table, row, column, checked, faintRowStyle=False, update=False):
        try:
            checkbox = QCheckBox()
            checkbox.setChecked(checked)

            container = QWidget()
            layout = QHBoxLayout(container)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row, column, container)

            if not faintRowStyle:
                return

            def onClick(state):
                targetRow = self.getWidgetRow(table, column, checkbox)
                if targetRow is not None:
                    self._updateRowStyle(table, targetRow, bool(state))

            checkbox.stateChanged.connect(onClick)

            #   Update style immediately if prompted
            if update:
                self._updateRowStyle(table, row, checked)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to insert checkbox: {e}")

    def _updateRowStyle(self, table, row, checked):
        try:
            font = QFont("Courier New")
            font.setStyleStrategy(QFont.StyleStrategy.NoAntialias)

            if checked:
                text = QColor(150, 150, 150)
                background = QColor(245, 245, 245)
            else:
                text = QColor(0, 0, 0)
                background = QColor(255, 255, 255)

            for col in range(table.columnCount()):
                #   Cell
                item = table.item(row, col)
                if item:
                    item.setForeground(QBrush(text))
                    item.setBackground(QBrush(background))
                    item.setFont(font)

                #   Widget
                widget = table.cellWidget(row, col)
                if not widget:
                    continue

                widget.setAutoFillBackground(True)
                pal = widget.palette()
                pal.setColor(widget.backgroundRole(), background)
                widget.setPalette(pal)

                #   Apply font rules
                if not isinstance(widget, QPushButton):
                    widget.setFont(font)

                if checked:
                    if col in [0, 1]:
                        widget.setEnabled(True)
                    else:
                        widget.setEnabled(False)
                else:
                    widget.setEnabled(True)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.cmd.error(f"[{datetime.now()}] Error updating row style: {e}")

    def _updateCheckbox(self, table, row, column, checked=False):
        #   Sortvalue
        #   sortvalue = table.item(row, column)
        #   sortvalue.setText(str(checked))

        #   Checkbox
        container = table.cellWidget(row, column)
        checkbox = container.findChild(QCheckBox)
        checkbox.setChecked(checked)
        return checkbox

    def _insertCombobox(self, table, row, column, value=0):
        try:
            #   Sortvalue
            #   sortvalue = QTableWidgetItem(str(self.comboTemplate[value]))
            #   sortvalue.setForeground(QBrush(QColor(0, 0, 0, 0)))
            #   sortvalue.setFlags(sortvalue.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEditable)
            #   table.setItem(row, column, sortvalue)

            #   Combobox
            combo_box = QComboBox()

            combo_box.addItems(self.comboTemplate)
            combo_box.setCurrentIndex(value)
            table.setCellWidget(row, column, combo_box)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to insert combobox: {e}")

        return combo_box

    def _updateCombobox(self, table, row, column, value=0):
        #   Sortvalue
        #   sortvalue = table.item(row, column)
        #   sortvalue.setText(str(self.comboTemplate[value]))

        #   Combobox
        comboBox = table.cellWidget(row, column)
        comboBox.setCurrentIndex(value)

        return comboBox

    def _insertText(self, table: QTableWidget, row: int, column: int, value: str, editable=False, short=False):
        try:
            item = QTableWidgetItem(str(value))

            if not editable:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            if short:
                #   todo
                item.setToolTip(value)
                table.setItem(row, column, item)
            else:
                table.setItem(row, column, item)

            return item
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to insert text: {e}")

    def _updateText(self, table: QTableWidget, row: int, column: int, value: str):
        text = table.item(row, column)
        text.setText(value)  # type: ignore

        return text

    def _insertDestinationBrowser(self, table: QTableWidget, row: int, column: int):
        try:
            button = QPushButton("...")
            button.setFixedWidth(30)
            button.setStyleSheet(self.stylesheetQPushbutton)

            #   Closure to remember row/column and update the cell before the button
            def onBrowse(self):
                targetRow = self.getWidgetRow(table, column, button)
                if targetRow is None:
                    return
                targetColumn = column - 1
                targetItem = table.item(targetRow, targetColumn)

                path = targetItem.text() if targetItem and targetItem.text() else ""
                self.logger.debug(f"Table: _insertDestinationBrowser::onBrowse was clicked on row {row}")

                folderPath = QFileDialog.getExistingDirectory(None, "Select Folder", path)
                if folderPath and targetItem:
                    targetItem.setText(folderPath)

            button.clicked.connect(lambda: onBrowse(self))
            table.setCellWidget(row, column, button)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to insert destination browser button: {e}")

    def _insertAutoTimestampButton(self, table, row, column):
        try:
            button = QPushButton("Auto")
            button.setMinimumWidth(60)
            button.setStyleSheet(self.stylesheetQPushbutton)

            def onClick(self):
                #   Get the path from column 5
                targetRow = self.getWidgetRow(table, column, button)
                if targetRow is None:
                    return
                targetColumn = column
                targetItem = table.item(targetRow, targetColumn - 1)
                pathItem = table.item(targetRow, 4)

                path = pathItem.text()

                #   If default build complete string
                if path == "default":
                    nameItem = table.item(targetRow, 3)
                    if not nameItem.text():
                        return
                    name = nameItem.text()
                    default = self.extractor.config.settings["defaultpath"]
                    path = f"{default}/{name}"

                self.logger.debug(f"Table: _insertAutoTimestampButton::onBrowse was clicked on row {targetRow}")
                timestamp = int(self.extractor.main.General.unixCreator.getTimestampFromFolder(path))

                targetItem.setText(str(int(timestamp)) if timestamp else "0")

            button.clicked.connect(lambda: onClick(self))
            table.setCellWidget(row, column, button)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to insert auto timestamp button: {e}")

    def _insertSqlDeleteButton(self, table, row, column):
        try:
            button = QPushButton("Delete SQL")
            button.setMinimumWidth(70)
            button.setStyleSheet(self.stylesheetQPushbutton)

            def onClick(self):
                #   Get the path from column 5
                targetRow = self.getWidgetRow(table, column, button)
                if targetRow is None:
                    return

                path = table.item(targetRow, 4).text()
                username = table.item(targetRow, 3).text()

                #   Determine the directory to search in
                if path == "default":
                    default = self.extractor.config.settings["defaultpath"]
                    searchDPath = os.path.join(default, username)
                else:
                    searchDPath = path

                #   Look for SQL files in the directory
                try:
                    if os.path.exists(searchDPath) and os.path.isdir(searchDPath):
                        sqlFiles = [f for f in os.listdir(searchDPath) if f.lower().endswith(".sql")]

                        if len(sqlFiles) == 1:
                            sqlFPath = os.path.join(searchDPath, sqlFiles[0])
                            self.logger.debug(f"Found single SQL file: {sqlFiles[0]}")
                        elif len(sqlFiles) > 1:
                            sqlFPath = os.path.join(searchDPath, f"{username}.sql")
                            self.logger.debug(f"Multiple SQL files found ({len(sqlFiles)}), using username fallback: {username}.sql")
                        else:
                            self.logger.debug(f"No SQL files found in directory: {searchDPath}")
                            return
                    else:
                        sqlFPath = os.path.join(searchDPath, f"{username}.sql")
                        self.logger.debug(f"Directory doesn't exist, using username fallback: {username}.sql")

                except Exception as e:
                    self.logger.error(f"Error reading directory {searchDPath}: {e}")
                    sqlFPath = os.path.join(searchDPath, f"{username}.sql")

                self.logger.debug(f"Table: _insertSqlDeleteButton::onClick was clicked on row {targetRow}")
                self.logger.info(f"Table: Deleting {sqlFPath}")
                self.main.safeTrash(sqlFPath, "file", safe=False)

            button.clicked.connect(lambda: onClick(self))
            table.setCellWidget(row, column, button)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to insert SQL delete button: {e}")

    def getTableData(self) -> dict | Literal[False]:
        try:
            fullTable = []
            #   Check if there's any duplicate users
            usersSeen = set()
            for row in range(self.table.rowCount()):
                username = self.table.item(row, 3).text()  # type: ignore
                if username in usersSeen:
                    self.main.qtHelper.Throw(f"Duplicate user found: {username}", title="Duplicate User", type=MessageType.WARNING)
                    return False
                usersSeen.add(username)
            usersSeen.clear()

            #   Check if rows are valid
            for row in range(self.table.rowCount()):
                data = self._saveRowData(row)
                if not self.isRowValid(data, row):
                    return False

                fullTable.append(data)

            fullTable = {"users": fullTable}
            return fullTable
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Failed to get table data: {e}")

    def saveTable(self):
        try:
            fullTable = self.getTableData()
            if not fullTable:
                return

            self.config.saveConfig(overwrite=fullTable, forced=True)

            self.inv(lambda: self.logger.info("Table: Saved user table"))
            return True

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"There was an error saving the table:\n{self.main.varHelper.exception(e)}", logger=self.logger)
            return False

    def isRowValid(self, data, row):
        for column in range(len(self.tableTemplate)):
            #   Show on Addtable? > Widget type > Header Title > Json KEY name > default > check
            jsonKeyName = self.tableTemplate[column][3]
            HeaderTitle = self.tableTemplate[column][2]

            checkType = self.tableTemplate[column][5]

            if checkType == None:
                continue

            index = self.table.model().index(row, 0)

            if checkType == Validation.INTEGER:
                if not VarHelper.isValidNumber(data[f"{jsonKeyName}"]):
                    self.main.qtHelper.Throw(f"Invalid integer on row {row + 1} for {HeaderTitle}", title="Invalid Integer")
                    self.table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
                    return False
            elif checkType == Validation.DIR_PATH:
                if not VarHelper.isValidDPath(data[f"{jsonKeyName}"], True, False):
                    self.main.qtHelper.Throw(f"Invalid path on row {row + 1} for {HeaderTitle}", title="Invalid Path")
                    self.table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
                    return False

            elif checkType == Validation.BOOLEAN:
                if not VarHelper.isValidBoolean(data[f"{jsonKeyName}"]):
                    self.main.qtHelper.Throw(f"Invalid boolean on row {row + 1} for {HeaderTitle}", title="Invalid Boolean")
                    self.table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
                    return False
            elif checkType == Validation.EMPTY:
                if VarHelper.isEmpty(data[f"{jsonKeyName}"]):
                    self.main.qtHelper.Throw(f"Row {row + 1} for {HeaderTitle} can't be empty")
                    self.table.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
                    return False
        return True

    def importTable(self):
        self.extractor.logger.debug("userTable::importTable")

        fullTable = []
        window = QWidget()

        try:
            importPath, _ = QFileDialog.getOpenFileName(
                parent=window,
                caption="Select a JSON file",
                filter="JSON Files (*.json);;All Files (*)",
            )

            if not importPath:
                self.logger.info("Table: No file was selected for import")
                return

            with open(importPath, "r", encoding="utf-8") as f:
                fullTable = json.load(f)

            for user in fullTable:
                index = self._getComboIndex()
                self.insertRowFromData(user, index)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Table: There was an error importing the table: {e}")
            self.logger.error(f"Table: Make sure it's compatible with the extractor")

    def exportTable(self):
        self.extractor.logger.debug("userTable::exportTable")

        defaultFilename = f"{self.extractor.name}Users.json"

        exportPath, _ = QFileDialog.getSaveFileName(
            self.main,
            "Export Users Table",  #    Dialog title
            defaultFilename,  #     Default file name
            "JSON Files (*.json);;All Files (*)",
        )

        if not exportPath:
            self.inv(lambda: self.logger.debug(f"Table: Export cancelled by user"))
            return False

        #   Add .json extension
        if not exportPath.lower().endswith(".json"):
            exportPath += ".json"

        try:
            fullTable = self.getTableData()
            if not fullTable:
                return

            with open(exportPath, "w", encoding="utf-8") as f:
                json.dump(fullTable, f, indent=4)

            self.inv(lambda: self.logger.info(f"Table: Successfully exported {len(fullTable)} users to {exportPath}"))
            return True

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"Failed to export users table: {str(e)}", logger=self.extractor.logger)
            return False

    def setUserKey(self, username, keyname, value):
        try:
            for i, user in enumerate(self.list):
                if user.get("UserHandle") == username:
                    self.main.debuggy(f"Updating {username}'s {keyname} key to '{value}' at index {i} where ({self.list[i]=} and )", self)
                    self.inv(lambda: self.logger.debug(f"Updating {username}'s {keyname} key to '{str(value)[:12]}'..."))
                    user[keyname] = value
                    self.inv(lambda u=user, i=i: self.updateRowFromData(u, i))
                    return
            self.inv(lambda: self.logger.alert(f"{username} not found in list"))
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda: self.logger.error(f"Something went wrong updating {username}'s {keyname} key: {e}"))

    def getWidgetRow(self, table: QTableWidget, column: int, sender: QWidget) -> int | None:
        try:
            """Return the current row of a button in the given column of a QTableWidget"""
            for row in range(table.rowCount()):
                widget = table.cellWidget(row, column)
                if widget:
                    #   Check if the widget is inside a container
                    if widget == sender or sender in widget.findChildren(QWidget):
                        return row
            return None
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"Failed to get row from widget: {e}")
            return None
