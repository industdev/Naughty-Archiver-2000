from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from na2000 import MainApp

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFileDialog, QApplication
from PySide6.QtGui import QKeySequence, QShortcut
from datetime import datetime

import os

from lib.ui.UnixCreator_ui import Ui_UnixCreator


class UnixCreator(QWidget):
    def __init__(self, main: "MainApp"):
        super().__init__(None)

        self.main = main
        self.manualTimestampUpdate = False

        self.ui = Ui_UnixCreator()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("UNIX timestamp creator")
        self.resize(480, 140)
        self.setFixedSize(self.size())

        self.initializeWidget()
        self.connectSignals()

        self.loading = self.main.loadingBar
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)
        self.ui.btn_folder.setToolTip(
            "Find the timestamp of the latest file created in a folder. This indicates when the last file got extracte\n It only take in consideration files with the following extensions:\n .png, .jpg, .mp4, .mov, .jpeg, .gif, .wepb, .html, .zip, .mkv"
        )
        self.main.qtHelper.setIcon(self, "ieframe_20783.ico")
        self.main.qtHelper.setIcon(self.ui.btn_folder, "ieframe_20784.ico")
        self.main.qtHelper.setIcon(self.ui.btn_copy, "dsquery_153.ico")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def initializeWidget(self):
        current_date = datetime.now()

        self.ui.cfg_day.setText(str(current_date.day))
        self.ui.cfg_month.setText(str(current_date.month))
        self.ui.cfg_year.setText(str(current_date.year))

        self.updateTimestamp()

    def connectSignals(self):
        self.ui.cfg_day.textChanged.connect(self.updateTimestamp)
        self.ui.cfg_month.textChanged.connect(self.updateTimestamp)
        self.ui.cfg_year.textChanged.connect(self.updateTimestamp)
        self.ui.cfg_result.textChanged.connect(self.updateDateFromTimestamp)
        self.ui.btn_copy.clicked.connect(self.copyTimestamp)
        self.ui.btn_folder.clicked.connect(self.selectFolder)

    def updateTimestamp(self):
        if self.manualTimestampUpdate:
            return

        try:
            day = int(self.ui.cfg_day.text()) if self.ui.cfg_day.text() else 1
            month = int(self.ui.cfg_month.text()) if self.ui.cfg_month.text() else 1
            year = int(self.ui.cfg_year.text()) if self.ui.cfg_year.text() else 1970

            #   Create datetime object
            date_obj = datetime(year, month, day)
            timestamp = int(date_obj.timestamp())

            self.ui.cfg_result.setText(str(timestamp))

        except (ValueError, OverflowError):
            self.ui.cfg_result.setText("Invalid Date")

    def updateDateFromTimestamp(self):
        if self.manualTimestampUpdate:
            return

        try:
            timestamp_text = self.ui.cfg_result.text().strip()

            #   Skip if empty or invalid
            if not timestamp_text or timestamp_text == "Invalid Date":
                return

            timestamp = int(timestamp_text)

            #   Convert timestamp to datetime
            date_obj = datetime.fromtimestamp(timestamp)

            self.manualTimestampUpdate = True

            self.ui.cfg_day.setText(str(date_obj.day))
            self.ui.cfg_month.setText(str(date_obj.month))
            self.ui.cfg_year.setText(str(date_obj.year))

        except (ValueError, OverflowError, OSError) as e:
            #   Don't update anything if timestamp is invalid
            pass
        finally:
            self.manualTimestampUpdate = False

    def copyTimestamp(self):
        try:
            timestamp_text = self.ui.cfg_result.text().strip()

            if timestamp_text and timestamp_text != "Invalid Date":
                clipboard = QApplication.clipboard()
                clipboard.setText(timestamp_text)

                self.main.General.logger.debug(f"Copied timestamp: {timestamp_text}")

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.General.logger.debug(f"Error copying timestamp: {e}")

    def selectFolder(self):
        try:
            folderPath = QFileDialog.getExistingDirectory(
                self, "Select Folder", "", QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
            )

            if not folderPath:
                return

            timestamp = self.getTimestampFromFolder(folderPath)
            if not timestamp:
                self.ui.cfg_result.setText("No files found")
                return

            latestDate = datetime.fromtimestamp(timestamp)

            #   Update the line edits with the latest date
            self.ui.cfg_day.setText(str(latestDate.day))
            self.ui.cfg_month.setText(str(latestDate.month))
            self.ui.cfg_year.setText(str(latestDate.year))

            self.ui.cfg_result.setText(str(int(timestamp)))

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.General.logger.debug(f"Error selecting folder: {e}")
            self.ui.cfg_result.setText("Error reading folder")

    def getTimestampFromFolder(self, folder):
        try:
            timestamp = 0
            maxTimestamp = 0
            filesFound = False
            items = 0
            exts = (".png", ".jpg", ".mp4", ".mov", ".jpeg", ".gif", ".wepb", ".html", ".zip", ".mkv")

            with os.scandir(folder) as entries:
                #   Count files with allowed extensions
                items = sum(1 for entry in entries if entry.is_file() and entry.name.lower().endswith(exts))

            self.loading.start(items, f"Searching for timestamp...", 200, "files", 40)
            self.main.debuggy(f"Searching for timestamp in {folder}", self)

            with os.scandir(folder) as entries:
                for entry in entries:
                    try:
                        if not (entry.is_file() and entry.name.lower().endswith(exts)):
                            self.main.debuggy(f"Skipping {entry.name} ({entry.stat().st_mtime})", self)
                            continue
                        self.main.debuggy(f"Considering {entry.name} ({entry.stat().st_mtime})", self)
                        self.loading.increase(1)
                        filesFound = True
                        timestamp = entry.stat().st_mtime
                        if maxTimestamp < timestamp:
                            maxTimestamp = timestamp
                    except OSError:
                        self.main.debuggy(f"OSError on {entry.name}", self)
                        continue
        except FileNotFoundError:
            return 0
        except Exception as e:
            self.main.varHelper.exception(e)
            return 0
        finally:
            self.loading.terminate()

        self.main.debuggy(f"Decided on {maxTimestamp if filesFound else 0}", self)
        return maxTimestamp if filesFound else 0
