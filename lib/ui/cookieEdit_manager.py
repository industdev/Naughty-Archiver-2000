from typing import TYPE_CHECKING

from lib.Enums import SpecialWidgets

if TYPE_CHECKING:
    from lib.Extractor import Extractor

from PySide6.QtWidgets import QTextEdit, QWidget
from PySide6.QtCore import Qt
from lib.ui.cookieEdit_ui import Ui_Form
import os
import subprocess
from PySide6.QtGui import QKeySequence, QShortcut


class CookieEdit(QWidget):
    def __init__(self, filesPath: str, galleryFPath: str, extractor: "Extractor"):
        super().__init__(None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(f"{extractor.name} cookies")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)

        self.ui.btn_add.clicked.connect(self.addFile)
        self.ui.btn_remove.clicked.connect(self.removeFile)
        self.ui.btn_saveSelection.clicked.connect(self.saveSelection)
        self.ui.cb_fileDropdown.currentIndexChanged.connect(self.loadFile)

        #   cookiesTextBox
        settings = extractor.settings.getCookiesSettings()
        self.cookiesTextBoxType = settings[0]
        self.cookiesTextBoxText = settings[1]
        self.cookiesShowPixivOauthButton = settings[2]
        self.setupTextBoxes(self.cookiesTextBoxType, self.cookiesTextBoxText)

        #   cookiesShowPixivOauthButton
        if self.cookiesShowPixivOauthButton:
            self.ui.btn_oauth.clicked.connect(self.runOauth)
        else:
            self.ui.btn_oauth.setVisible(False)
            self.ui.btn_oauth.deleteLater()
        self.galleryFPath = galleryFPath
        self.currentSelectedFullPath = "None!"
        self.filesPath = filesPath
        self.extractor = extractor
        self.updateComboBox()
        self.updateTextboxStates()

        extractor.main.qtHelper.setIcon(self, "dsuiext_4110.ico")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def setupTextBoxes(self, cookiesTextBoxType, cookiesTextBoxText):
        self.ui.textEdit1.setPlaceholderText(cookiesTextBoxText[0])

        #   Configure based on text box type
        if cookiesTextBoxType == 0:
            if hasattr(self.ui, "textEdit2"):
                self.ui.textEdit2.deleteLater()

            if hasattr(self.ui, "textEdit2_line"):
                self.ui.textEdit2_line.deleteLater()

            #   Set custom focusOutEvent handler
            self.ui.textEdit1.focusOutEvent = lambda event: self._focusOutEvent(event, self.ui.textEdit1)  # type: ignore

        else:
            if cookiesTextBoxText[1]:
                self.ui.textEdit2.setPlaceholderText(cookiesTextBoxText[1])

            if cookiesTextBoxType == 1:
                self.ui.textEdit2.setMaximumHeight(32)

            #   Set custom focusOutEvent handlers for both text edits
            self.ui.textEdit1.focusOutEvent = lambda event: self._focusOutEvent(event, self.ui.textEdit1)  # type: ignore
            self.ui.textEdit2.focusOutEvent = lambda event: self._focusOutEvent(event, self.ui.textEdit2)  # type: ignore

    def updateTextboxStates(self):
        hasFile = bool(self.ui.cb_fileDropdown.currentText())

        self.ui.textEdit1.setEnabled(hasFile)
        if hasattr(self.ui, "textEdit2") and self.ui.textEdit2:
            self.ui.textEdit2.setEnabled(hasFile)

        #   Also disable the save selection button if no file is selected
        self.ui.btn_saveSelection.setEnabled(hasFile)
        self.ui.btn_remove.setEnabled(hasFile)

    def runOauth(self):
        str = "Copy the token to the smaller textbox! "
        command = f'start cmd /c "{self.galleryFPath}" oauth:pixiv ^& echo {str} ^& pause'
        subprocess.Popen(command, shell=True)

    def saveSelection(self):
        text = self.ui.cb_fileDropdown.currentText()
        if text == "":
            return

        override = os.path.join(self.filesPath, text)

        self.extractor.main.configurator.updateConfigByWidget(
            self.extractor.config.settings,
            "cookiespath",
            override,
            self.extractor,
            SpecialWidgets.EXT_COOKIESLABEL,
            self.extractor.ui.label_2,
        )

        text = self.extractor.config._pathToCookiesFilename(override)
        self.extractor.ui.label_2.setText(text)
        self.close()

    def updateComboBox(self):
        self.ui.cb_fileDropdown.clear()

        if not os.path.exists(self.filesPath):
            os.makedirs(self.filesPath)
            return

        #   Get all files from the directory that don't end with _token
        files = [f for f in os.listdir(self.filesPath) if os.path.isfile(os.path.join(self.filesPath, f)) and not f.endswith("_token")]

        if files:
            self.ui.cb_fileDropdown.addItems(files)

    def loadFile(self):
        currentFile = self.ui.cb_fileDropdown.currentText()
        self.updateTextboxStates()

        #   No file selected
        if not currentFile:
            self.ui.textEdit1.clear()
            if hasattr(self.ui, "textEdit2") and self.ui.textEdit2:
                self.ui.textEdit2.clear()
            return

        #   Load cookie file
        cookieFilePath = os.path.join(self.filesPath, currentFile)
        if os.path.exists(cookieFilePath):
            try:
                with open(cookieFilePath, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.ui.textEdit1.setPlainText(content)
            except Exception as e:
                self.ui.textEdit1.setPlainText(f"Error loading cookie file: {str(e)}")
        else:
            self.ui.textEdit1.setPlainText(f"Error: File '{currentFile}' not found.")

        #   Load token file if second text box exists
        if hasattr(self.ui, "textEdit2") and self.ui.textEdit2:
            tokenFilePath = os.path.join(self.filesPath, f"{currentFile}_token")
            if os.path.exists(tokenFilePath):
                try:
                    with open(tokenFilePath, "r", encoding="utf-8") as file:
                        content = file.read()
                        self.ui.textEdit2.setPlainText(content)
                except Exception as e:
                    self.ui.textEdit2.setPlainText(f"Error loading token file: {str(e)}")
            else:
                self.ui.textEdit2.clear()

    def _focusOutEvent(self, event, edit):
        currentFile = self.ui.cb_fileDropdown.currentText()

        #   No file selected
        if not currentFile:
            # Call the original method via the QTextEdit class
            QTextEdit.focusOutEvent(edit, event)
            return

        #   Determine which file to save based on which text edit lost focus
        if edit == self.ui.textEdit1:
            cookieFilePath = os.path.join(self.filesPath, currentFile)
            try:
                with open(cookieFilePath, "w", encoding="utf-8") as cookiefile:
                    content = self.ui.textEdit1.toPlainText()
                    cookiefile.write(content)
            except Exception as e:
                self.extractor.logger.error(f"Error saving A cookie file: {str(e)}")
        elif hasattr(self.ui, "textEdit2") and edit == self.ui.textEdit2:
            tokenFilePath = os.path.join(self.filesPath, f"{currentFile}_token")
            try:
                with open(tokenFilePath, "w", encoding="utf-8") as tokenfile:
                    content = self.ui.textEdit2.toPlainText()
                    tokenfile.write(content)
            except Exception as e:
                self.extractor.logger.error(f"Error saving B cookie file: {str(e)}")

        #   Call the original method via the QTextEdit class
        QTextEdit.focusOutEvent(edit, event)

    def _Refresh(self):
        currentFile = self.ui.cb_fileDropdown.currentText()
        self.updateComboBox()

        #   Reselect file
        index = self.ui.cb_fileDropdown.findText(currentFile)
        if index >= 0:
            self.ui.cb_fileDropdown.setCurrentIndex(index)

        #   Update textbox states after refresh
        self.updateTextboxStates()

    def addFile(self):
        filename = self.ui.txt_fileName.toPlainText().strip()

        if not filename or len(filename) > 128:
            filename = "Cookies"
            return

        if not os.path.exists(self.filesPath):
            os.makedirs(self.filesPath)

        cookieFilePath = os.path.join(self.filesPath, filename)
        tokenFilePath = os.path.join(self.filesPath, f"{filename}_token")

        try:
            if not os.path.exists(cookieFilePath):
                with open(cookieFilePath, "w", encoding="utf-8") as file:
                    file.write("")

            if hasattr(self.ui, "textEdit2") and self.ui.textEdit2:
                if not os.path.exists(tokenFilePath):
                    with open(tokenFilePath, "w", encoding="utf-8") as file:
                        file.write("")

            self._Refresh()

            index = self.ui.cb_fileDropdown.findText(filename)
            if index >= 0:
                self.ui.cb_fileDropdown.setCurrentIndex(index)

            self.ui.txt_fileName.clear()

        except Exception as e:
            self.extractor.logger.error(f"Error creating files: {str(e)}")

    def removeFile(self):
        selected = self.ui.cb_fileDropdown.currentText()

        if not selected:
            self.extractor.logger.info(f"No cookie file selected to remove")
            return

        cookieFilePath = os.path.join(self.filesPath, selected)
        tokenFilePath = os.path.join(self.filesPath, f"{selected}_token")

        try:
            if os.path.exists(cookieFilePath):
                os.remove(cookieFilePath)

            if os.path.exists(tokenFilePath):
                os.remove(tokenFilePath)

            self.loadFile()
            self._Refresh()

        except Exception as e:
            self.extractor.logger.error(f"Error removing files: {str(e)}")
