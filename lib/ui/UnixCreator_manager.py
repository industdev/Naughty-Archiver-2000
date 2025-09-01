from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from na2000 import MainApp

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFileDialog, QApplication
from PySide6.QtGui import QKeySequence, QShortcut
from datetime import datetime
from lib.VarHelper import VarHelper

import os

from lib.ui.UnixCreator import Ui_UnixCreator


class UnixCreator(QWidget):
    def __init__(self, main: "MainApp"):
        super().__init__(None)

        self.main = main

        self.ui = Ui_UnixCreator()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("UNIX timestamp creator")
        self.resize(480, 130)
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
        self.ui.btn_copy.clicked.connect(self.copyTimestamp)
        self.ui.btn_folder.clicked.connect(self.selectFolder)

    def updateTimestamp(self):
        try:
            day = int(self.ui.cfg_day.text()) if self.ui.cfg_day.text() else 1
            month = int(self.ui.cfg_month.text()) if self.ui.cfg_month.text() else 1
            year = int(self.ui.cfg_year.text()) if self.ui.cfg_year.text() else 1970

            #   Create datetime object
            date_obj = datetime(year, month, day)
            timestamp = int(date_obj.timestamp())

            self.ui.lbl_unix.setText(f"UNIX: {timestamp}")

        except (ValueError, OverflowError):
            self.ui.lbl_unix.setText("UNIX: Invalid Date")

    def copyTimestamp(self):
        try:
            label_text = self.ui.lbl_unix.text()
            if label_text.startswith("UNIX: ") and not "Invalid" in label_text:
                timestamp = label_text.replace("UNIX: ", "")

                clipboard = QApplication.clipboard()
                clipboard.setText(timestamp)

                self.main.General.logger.debug(f"Copied timestamp: {timestamp}")

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
                self.ui.lbl_unix.setText("UNIX: No files found")
                return

            latestDate = datetime.fromtimestamp(timestamp)

            #   Update the line edits with the latest date
            self.ui.cfg_day.setText(str(latestDate.day))
            self.ui.cfg_month.setText(str(latestDate.month))
            self.ui.cfg_year.setText(str(latestDate.year))

            self.ui.lbl_unix.setText(f"UNIX: {int(timestamp)}")

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.General.logger.debug(f"Error selecting folder: {e}")
            self.ui.lbl_unix.setText("UNIX: Error reading folder")

    def getTimestampFromFolder(self, folder):  # Add your extensions
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

            with os.scandir(folder) as entries:
                for entry in entries:
                    if not (entry.is_file() and entry.name.lower().endswith(exts)):
                        continue
                    self.loading.increase(1)
                    filesFound = True
                    try:
                        maxTimestamp = entry.stat().st_mtime
                        if maxTimestamp > timestamp:
                            timestamp = maxTimestamp
                    except OSError:
                        continue
        except FileNotFoundError:
            return 0
        except Exception as e:
            self.main.varHelper.exception(e)
            return 0
        finally:
            self.loading.terminate()

        return maxTimestamp if filesFound else 0
