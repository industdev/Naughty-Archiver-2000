import re
from typing import TYPE_CHECKING

from lib.Enums import ExtractorState, MessageType

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QListWidget, QWidget, QListWidgetItem
from PySide6.QtCore import Qt
from lib.ui.ExtractorUrlCreator_ui import Ui_URLManager
from lib.VarHelper import VarHelper
import time


class ExtractorUrlCreator(QWidget):
    def __init__(self, main: "MainApp", extractor: "Extractor"):
        super().__init__(None)
        try:
            start = time.perf_counter()
            self.main = main
            self.inv = main._inv
            self.extractor = extractor

            self.ui = Ui_URLManager()
            self.ui.setupUi(self)
            self.setupUi()
            self.setWindowTitle("URL Manager")
            self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)

            settings = extractor.settings.getExtractorUrls()
            self.urls = settings[0]
            self.urlsAliases = settings[1]

            self.userList = None
            self.normalizedUrlPatterns = self.buildNormalizedUrlPatterns()
            self.jobOverride = []

            self.argumentChanged()

        except Exception as e:
            raise Exception(f"Failed to load URLManager: {e}")
        finally:
            self.main.cmd.debug(f" :{__name__}::__init__ ->{(time.perf_counter() - start) * 1000:.6f}ms")

    def updateUi(self):
        self.userList = self.extractor.getUserList()

        self.ui.cfgui_combo.clear()

        for user in self.userList:
            name = user["UserHandle"]
            self.ui.cfgui_combo.addItem(name)

    def setupUi(self):
        self.main.qtHelper.setIcon(self, "inetcpl_1315.ico")
        self.main.qtHelper.setIcon(self.ui.btn_insert, "ieframe_42025.ico", size=(16, 16))
        self.main.qtHelper.setIcon(self.ui.btn_start, "imageres_116.ico", size=(16, 16))
        self.main.qtHelper.setIcon(self.ui.btn_removeselected, "cryptui_3419.ico", size=(16, 16))
        self.main.qtHelper.setIcon(self.ui.btn_import, "certmgr_444.ico", size=(16, 16))
        self.main.qtHelper.setIcon(self.ui.btn_importingDone, "imageres_5341.ico", size=(16, 16))

        self.ui.importWidget.hide()
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)

        self.ui.cfgui_arg1.textChanged.connect(self.argumentChanged)
        self.ui.cfgui_arg2.textChanged.connect(self.argumentChanged)
        self.ui.extractorUrls.itemSelectionChanged.connect(self._updateButtonState)
        self.ui.btn_insert.clicked.connect(self._insertSelectedUrl)
        self.ui.btn_removeselected.clicked.connect(self._removeSelectedUrls)
        self.ui.btn_start.clicked.connect(self.startOverride)
        self.ui.btn_import.clicked.connect(lambda: self.showImportForm(True))
        self.ui.btn_importingDone.clicked.connect(lambda: self.importUrlsFromList())

    def buildNormalizedUrlPatterns(self):
        """
        Convert self.urls into regex patterns that can match user URLs.
        - Replace aliases with a group that matches any alias in self.urlsAliases
        - Replace %s with ([^/]+) to match any non-slash segment
        - Return compiled regex objects
        """
        patterns = []
        aliasGroup = "|".join(re.escape(alias) for alias in self.urlsAliases)

        for template in self.urls:
            matched = False
            for alias in self.urlsAliases:
                if template.startswith(alias):
                    # Replace alias with group of all aliases
                    normalized = re.sub(rf"^{re.escape(alias)}", f"(?:{aliasGroup})", template, count=1)
                    matched = True
                    break

            if not matched:
                self.main.debuggy(f"buildNormalizedUrlPatterns -> skipped (no alias): {template}", self)
                continue

            # Replace %s placeholders with "any segment" regex
            normalized = normalized.replace("%s", "([^/]+)")

            # Compile into regex
            regexPattern = f"^{normalized}$"
            compiled = re.compile(regexPattern)
            patterns.append(compiled)

        self.main.debuggy(f"buildNormalizedUrlPatterns -> built {len(patterns)} patterns", self)
        return patterns

    def showImportForm(self, show):
        self.main.debuggy(f"showImportForm -> {show}", self)
        if show:
            self.ui.runWidget.hide()
            self.ui.importWidget.show()
        else:
            self.ui.importWidget.hide()
            self.ui.runWidget.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def addChosenUrl(self, url: str, appendArgs: str = "", user: str = "") -> bool:
        """
        Add a URL with arguments and user to both the job list and UI display.
        Returns True if successful, False otherwise.
        """
        try:
            # Use current user if not specified
            if not user:
                user = str(self.ui.cfgui_combo.currentText())

            # Use current append args if not specified
            if not appendArgs:
                appendArgs = self.ui.cfgui_argumets.text().strip().rstrip()

            if not user:
                self.main.qtHelper.Throw("Please select a user first", type=MessageType.INFO, parent=self)
                return False

            # Clean up the URL
            url = url.strip().rstrip()
            appendArgs = appendArgs.strip().rstrip()

            # Create the job
            self.insertJob(url, appendArgs, user)

            # Add to UI display
            base = f"{url} {appendArgs}".strip().rstrip()
            fullUrl = f'"{base}" ({user})'
            self.ui.chosenUrls.addItem(fullUrl)

            self.extractor.logger.debug(f"addChosenUrl -> Added {url} with args '{appendArgs}' for user {user}")
            return True

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(message=f"Failed to add URL: {e}", parent=self)
            return False

    def importUrlsFromList(self):
        self.showImportForm(False)

        textContent = self.ui.ImportedList.toPlainText().strip()
        if not textContent:
            self.main.debuggy("importUrlsFromList -> empty input", self)
            return

        importedUrls = [line.strip() for line in textContent.split("\n") if line.strip()]
        if not importedUrls:
            self.main.debuggy("importUrlsFromList -> no URLs found", self)
            return

        user = str(self.ui.cfgui_combo.currentText())
        appendArgs = self.ui.cfgui_argumets.text().strip().rstrip()
        if not user:
            self.main.qtHelper.Throw("Please select a user first", type=MessageType.INFO, parent=self)
            return

        validUrls = []
        invalidUrls = []

        for url in importedUrls:
            cleanedUrl = re.sub(r"^https?://", "", url)
            if cleanedUrl.startswith("www."):
                cleanedUrl = cleanedUrl[4:]

            self.main.debuggy(f"importUrlsFromList -> {url=}, {cleanedUrl=}", self)

            #   Verify alias presence
            if not any(cleanedUrl.startswith(alias) for alias in self.urlsAliases):
                self.main.debuggy(f"importUrlsFromList -> rejected (no alias): {cleanedUrl}", self)
                invalidUrls.append(url)
                continue

            #   Try each normalized pattern
            matched = False
            for pattern in self.normalizedUrlPatterns:
                if pattern.match(cleanedUrl):
                    self.main.debuggy(f"importUrlsFromList -> matched {pattern.pattern=}, {cleanedUrl=}", self)
                    if self.addChosenUrl(url, appendArgs, user):
                        validUrls.append(url)
                    else:
                        invalidUrls.append(url)
                    matched = True
                    break

            if not matched:
                self.main.debuggy(f"importUrlsFromList -> no pattern matched url={cleanedUrl}", self)
                invalidUrls.append(url)

        if invalidUrls:
            self.main.qtHelper.Throw(
                "The following URLs were not added because they don't match any valid template:\n" + "\n".join(invalidUrls),
                type=MessageType.INFO,
                parent=self,
            )

        self.ui.ImportedList.clear()
        self.main.debuggy("importUrlsFromList -> cleared ImportedList", self)

    def argumentChanged(self):
        self._updateExtractorUrls()
        self._updateButtonState()

    def _updateExtractorUrls(self):
        self.ui.extractorUrls.clear()

        arg1 = self.ui.cfgui_arg1.text().strip().rstrip()
        arg2 = self.ui.cfgui_arg2.text().strip().rstrip()

        display_arg1 = arg1 if arg1 else "?"
        display_arg2 = arg2 if arg2 else "?"

        # Process each URL template
        for template in self.urls:
            try:
                # Count the number of %s placeholders
                count = template.count("%s")

                if count == 1:
                    formatted_url = template % display_arg1
                elif count == 2:
                    formatted_url = template % (display_arg1, display_arg2)
                else:
                    formatted_url = template

                item = QListWidgetItem(formatted_url)
                item.setData(Qt.ItemDataRole.UserRole, template)
                self.ui.extractorUrls.addItem(item)

            except (TypeError, ValueError) as e:
                item = QListWidgetItem(f"[Error formatting: {template}]")
                item.setData(Qt.ItemDataRole.UserRole, template)
                self.ui.extractorUrls.addItem(item)

    def _updateButtonState(self):
        validArg = bool(self.ui.cfgui_arg1.text().strip().rstrip())
        urlSelected = bool(self.ui.extractorUrls.currentItem())
        self.ui.btn_insert.setEnabled(validArg and urlSelected)

    def _insertSelectedUrl(self):
        currentItem = self.ui.extractorUrls.currentItem()
        if not currentItem:
            return

        template = currentItem.data(Qt.ItemDataRole.UserRole)

        arg1 = self.ui.cfgui_arg1.text().strip().rstrip()
        arg2 = self.ui.cfgui_arg2.text().strip().rstrip()
        user = str(self.ui.cfgui_combo.currentText())
        appendArgs = self.ui.cfgui_argumets.text().strip().rstrip()

        if not arg1:
            return

        try:
            count = template.count("%s")

            if count == 1:
                url = template % arg1
            elif count == 2:
                url = template % (arg1, arg2)
            else:
                url = template

            if not user:
                return

            url = url.strip().rstrip()
            base = f"{url} {appendArgs}".strip().rstrip()
            fullUrl = f'"{base}" ({user})'

            self.extractor.logger.debug(f"insertSelectedUrl {url}, {appendArgs}, {user}")
            self.insertJob(url, appendArgs, user)
            self.ui.chosenUrls.addItem(fullUrl)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(message=f"Failed to insert the url: {e}", parent=self)

    def _removeSelectedUrls(self):
        selectedItems = self.ui.chosenUrls.selectedItems()

        if not selectedItems:
            return

        #   Get the row indices of selected items before removal
        removeRows = []
        for item in selectedItems:
            row = self.ui.chosenUrls.row(item)
            removeRows.append(row)

        removeRows.sort(reverse=True)
        for i, row in enumerate(removeRows):
            self.ui.chosenUrls.takeItem(row)
            self.extractor.logger.debug(f"_removeSelectedUrls -> Removed job {self.jobOverride[i].get('url', '')}")
            self.jobOverride.pop(i)

    def updateUrls(self, new_urls):
        self.urls = new_urls
        self._updateExtractorUrls()
        self._updateButtonState()

    def getChosenUrls(self):
        urls = []
        for i in range(self.ui.chosenUrls.count()):
            urls.append(self.ui.chosenUrls.item(i).text())
        return urls

    def clearChosenUrls(self):
        self.ui.chosenUrls.clear()

    def insertJob(self, url: str, appendArgs: str, user: str) -> None:
        userData = VarHelper.returnDictFromMatchedKeyInDictArray(user, "UserHandle", self.userList)
        if not userData:
            self.main.qtHelper.Throw(message=f"{user} was not found in the user table", parent=self)
            raise Exception(f"{user} was not found in the user table")

        job = self.extractor.settings.getJobs(
            userData,
            self.extractor.config.settings,
            self.main.General.config.settings,
            self.extractor.runner.getBaseConf(userData),
            self.extractor.runner.deepUpdate,
            self.main,
        )[1]

        job["url"] = f"{appendArgs} {url}".strip().rstrip()
        job["type"] = f"{appendArgs} {url}".strip().rstrip()
        job["userData"] = userData
        self.jobOverride.append(job)

        self.extractor.logger.debug(f"insertJob -> Created job {job['url']}")

    def startOverride(self):
        self.extractor.logger.debug(f"startOverride")
        if self.ui.cfg_quickExtraction.isChecked():
            self.main.debuggy(f"quickExtraction is checked, {self.extractor.settings.galleryName}", self)
            self.extractor.runner.makeJobsQuick(self.jobOverride, [self.extractor.settings.galleryName])

        if self.extractor.loopRunning:
            self.main.qtHelper.Throw(
                f"{self.extractor.name} is running, force stop it to run the custom job", type=MessageType.INFO, parent=self
            )
            return

        if self.main.debug:
            self.main.debuggy("Start extraction", self)
            self.main.debuggy(VarHelper.prettyJson(self.jobOverride), self, noFormat=True)
            string = "\n".join(f"Added {entry['url']}" for entry in self.jobOverride)
            self.main.debuggy(string, self, noFormat=True)

        self.extractor.startExtraction(self.jobOverride, [ExtractorState.CUSTOM_URLS_EXTRACTION, ExtractorState.ANY_URLS_EXTRACTION])
        self.close()
