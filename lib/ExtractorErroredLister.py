from typing import TYPE_CHECKING

from lib.Enums import ExtractorState, MessageType

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor, ExtractorEntry

from PySide6.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QKeySequence, QShortcut

from lib.ui.ExtractorErroredLister_ui import Ui_Form
from lib.VarHelper import VarHelper

import json
import os
import time


class ExtractorErroredLister(QWidget):
    def __init__(self, main: "MainApp", extractor: "Extractor") -> None:
        super().__init__(None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(f"{extractor.name} errored URLs")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)

        self.extractor = extractor
        self.main = main
        self.loading = main.loadingBar

        self.ui.label.setText(f"Loading URLs...")
        self.ui.btn_clear.clicked.connect(self.clear)
        self.ui.btn_retrySelected.clicked.connect(self.retrySelected)

        self.main.qtHelper.setIcon(self.ui.btn_clear, "cryptui_3419.ico")
        self.main.qtHelper.setIcon(self.ui.btn_retrySelected, "cliconfg_127.ico")
        self.main.qtHelper.setIcon(self, "cryptui_3417.ico")

        settings = extractor.settings.getErrorlistSettings()
        self.errorListEnabled = settings[0]
        self.errorListRegex = settings[1]
        self.errorListIdExtractRegex = settings[2]
        self.errorListFullURL = settings[3]

        if not self.errorListEnabled:
            self.extractor.ui.btn_showErrored.setVisible(False)

        self.runnerSettings = [self.extractor.erroredFPath, self.errorListRegex, self.errorListIdExtractRegex, self.errorListFullURL]
        self.setupTable()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def setupTable(self):
        self.main.debuggy(f" :{self.extractor.name}.ErroredLister::setupTable -> {self.extractor.configName}", self)
        self.ui.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        header = self.ui.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        #   Enable word wrapping for text that spans multiple lines
        self.ui.table.setWordWrap(True)

        self.ui.table.setSelectionBehavior(self.ui.table.SelectionBehavior.SelectItems)
        self.ui.table.setSelectionMode(self.ui.table.SelectionMode.ExtendedSelection)

        self.ui.table.setVerticalScrollMode(self.ui.table.ScrollMode.ScrollPerPixel)
        self.ui.table.setHorizontalScrollMode(self.ui.table.ScrollMode.ScrollPerPixel)

        #   Allow manual column resizing by user
        header.setSectionsMovable(False)
        header.setStretchLastSection(False)

    def showEvent(self, event):
        super().showEvent(event)
        self._loadData()
        self.loading.terminate()

    def _loadData(self):
        self.main.debuggy(f"erroredLister_settings::_loadData", self)
        try:
            if not os.path.exists(self.extractor.erroredFPath):
                self.ui.table.setRowCount(0)
                return
            with open(self.extractor.erroredFPath, "r", encoding="utf-8") as file:
                data = json.load(file)

            #   Clear existing table data
            self.ui.table.setRowCount(0)
            self.main.debuggy(f"erroredLister_settings::_loadData -> {len(data)}", self)
            if not data:
                return

            #   Set the number of rows based on array length
            self.ui.table.setRowCount(len(data))
            self.loading.start(len(data), "Loading errored URLs", 200)
            start_time = time.perf_counter()
            for row, item in enumerate(data):
                self.loading.increase(1)

                user = item.get("user", "Unknown")
                url = item.get("url", "Unknown")
                error = item.get("error", "Unknown")
                userItem = QTableWidgetItem(str(user))
                urlItem = QTableWidgetItem(str(url))
                errorItem = QTableWidgetItem(str(error))
                userItem.setData(Qt.ItemDataRole.DisplayRole, str(user))
                urlItem.setData(Qt.ItemDataRole.DisplayRole, str(url))
                errorItem.setData(Qt.ItemDataRole.DisplayRole, str(error))
                self.ui.table.setItem(row, 0, userItem)
                self.ui.table.setItem(row, 1, urlItem)
                self.ui.table.setItem(row, 2, errorItem)
                userItem.setFlags(userItem.flags() & ~Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)
                urlItem.setFlags(urlItem.flags() & ~Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)
                errorItem.setFlags(errorItem.flags() & ~Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable)
            end_time = time.perf_counter()
            t = end_time - start_time

            self.main.debuggy(f"ErroredLister::_loadData table fill took {t * 1000:.4f} ms", self)

            self.ui.table.resizeRowsToContents()
            self.ui.table.resizeColumnsToContents()

        except json.JSONDecodeError as e:
            self.extractor.logger.error(f"Error decoding JSON file: {e}")
            self.ui.table.setRowCount(1)
            self.ui.table.setItem(0, 0, QTableWidgetItem("JSON Error"))
            self.ui.table.setItem(0, 1, QTableWidgetItem(f"Invalid JSON format: {str(e)}"))

        except Exception as e:
            self.main.varHelper.exception(e)
            self.extractor.logger.error(f"Error loading errored data: {e}")
            self.ui.table.setRowCount(1)
            self.ui.table.setItem(0, 0, QTableWidgetItem("Load Error"))
            self.ui.table.setItem(0, 1, QTableWidgetItem(f"Failed to load data: {str(e)}"))
        finally:
            self.ui.label.setText(f" ")

    def clear(self):
        self.main.debuggy(f"erroredLister_settings::clear", self)

        try:
            #   Empty file
            with open(self.extractor.erroredFPath, "w", encoding="utf-8") as file:
                json.dump([], file)

            self._loadData()

            self.extractor.logger.info(f"Cleared errored URLs file: {self.extractor.erroredFPath}")

        except Exception as e:
            self.main.varHelper.exception(e)
            self.extractor.logger.error(f"Error clearing file: {e}")

    def refresh(self):
        self._loadData()

    def retrySelected(self):
        try:
            if self.extractor.loopRunning:
                self.main.qtHelper.Throw(f"{self.extractor.name} is running, force stop it to run the custom job", type=MessageType.INFO)
                return

            #   Get fully selected entries in self.ui.table, from the index on the left side
            selected = set()
            for index in self.ui.table.selectionModel().selectedRows():
                selected.add(index.row())

            #   Collect unique users from selected rows
            check = []
            urls = []

            self.main.debuggy(f"erroredLister_settings::retrySelected -> search selected", self)
            self.main.loadingBar.start(len(selected), "Loading Jobs...", 100, "jobs", 10)
            for row in selected:
                self.main.loadingBar.increase(1)
                user_item = self.ui.table.item(row, 0)
                url_item = self.ui.table.item(row, 1)
                check.append(user_item.text().strip())  # type: ignore
                urls.append(url_item.text().strip())  # type: ignore

            self.main.debuggy(f"erroredLister_settings::retrySelected -> found {len(check)}", self)

            if not check:
                return

            self.main.debuggy(f"erroredLister_settings::retrySelected -> Load external users", self)
            #   Load external users
            ext_users = self.extractor.getUserList()
            ext_userHandles = {user["UserHandle"] for user in ext_users}

            #   Find missing users
            missing = []
            for user in check:
                if user not in ext_userHandles and user not in missing:
                    missing.append(user)

            if missing:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Users Not Found")

                message_text = "The following users were not found in the user list:\n"
                message_text += "".join(f"\n- {user}" for user in missing)
                message_text += "\nPlease create these users in the user table and try again"

                msg.setText(message_text)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return

            #   Compile new job list
            jobs = []
            self.extractor.logger.debug(f"erroredLister_settings::retrySelected -> Creating jobs")
            for row in selected:
                sel_user = self.ui.table.item(row, 0).text().strip()  # type: ignore
                sel_url = self.ui.table.item(row, 1).text().strip()  # type: ignore

                #   Search for sel_user in 'UserHandle' keys for every entry in ext_users and return whole entry (of the user) if found
                ext_user = VarHelper.returnDictFromMatchedKeyInDictArray(sel_user, "UserHandle", ext_users)

                #   Extract complete user data from table
                job = self.extractor.settings.getJobs(
                    ext_user,
                    self.extractor.config.settings,
                    self.extractor.main.General.config.settings,
                    self.extractor.runner.getBaseConf(ext_user),
                    self.extractor.runner.deepUpdate,
                    self.main,
                )[1]

                job["url"] = sel_url
                job["type"] = f"Recovering {sel_url}"
                job["userData"] = ext_user
                jobs.append(job)
                self.main.debuggy(f"erroredLister_settings::retrySelected -> insert {job['url']}", self)

            self.extractor.logger.debug(f"erroredLister_settings::retrySelected -> {len(jobs)} jobs created, starting extraction")

            #   Start extraction
            self.main.debuggy("Start extraction", self)
            self.main.debuggy(VarHelper.prettyJson(jobs), self, noFormat=True)

            self.extractor.startExtraction(jobs, [ExtractorState.ERRORED_URLS_EXTRACTION, ExtractorState.ANY_URLS_EXTRACTION])
            self.close()
        except Exception as e:
            self.main.varHelper.exception(e)
            self.extractor.logger.error(f"Unexpected error while managing errored urls {e}")
        finally:
            self.main.loadingBar.terminate()
