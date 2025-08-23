from typing import TYPE_CHECKING

from lib.Enums import ExtractorState, MessageType

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtCore import Qt
from lib.ui.urlManager_ui import Ui_URLManager
from lib.VarHelper import VarHelper
import time


class URLManager(QWidget):
    def __init__(self, main: "MainApp", extractor: "Extractor"):
        super().__init__(None)
        try:
            start = time.perf_counter()
            self.main = main
            self.inv = main._inv
            self.extractor = extractor

            self.ui = Ui_URLManager()
            self.ui.setupUi(self)
            self.setWindowTitle("URL Manager")
            self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)

            self.urls = extractor.settings.getExtractorUrls()
            self.userList = None
            self.jobOverride = []

            self.connectSignals()
            self.argumentChanged()

            self.main.qtHelper.setIcon(self, "inetcpl_1315.ico")
            self.main.qtHelper.setIcon(self.ui.btn_insert, "ieframe_42025.ico", size=(16, 16))
            self.main.qtHelper.setIcon(self.ui.btn_start, "imageres_116.ico", size=(16, 16))
            self.main.qtHelper.setIcon(self.ui.btn_removeselected, "cryptui_3419.ico", size=(16, 16))
            QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)

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

    def connectSignals(self):
        self.ui.cfgui_arg1.textChanged.connect(self.argumentChanged)
        self.ui.cfgui_arg2.textChanged.connect(self.argumentChanged)
        self.ui.extractorUrls.itemSelectionChanged.connect(self._updateButtonState)
        self.ui.btn_insert.clicked.connect(self._insertSelectedUrl)
        self.ui.btn_removeselected.clicked.connect(self._removeSelectedUrls)
        self.ui.btn_start.clicked.connect(self.startOverride)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

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
        current_item = self.ui.extractorUrls.currentItem()
        if not current_item:
            return

        template = current_item.data(Qt.ItemDataRole.UserRole)

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

            self.extractor.logger.debug(f"urlManager_settings::insertSelectedUrl {url}, {appendArgs}, {user}")
            self.updateJobOverride(url, appendArgs, user)
            self.ui.chosenUrls.addItem(fullUrl)

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(message=f"Failed to insert the url: {e}")

    def _removeSelectedUrls(self):
        selected_items = self.ui.chosenUrls.selectedItems()

        if not selected_items:
            return

        #   Get the row indices of selected items before removal
        removeRows = []
        for item in selected_items:
            row = self.ui.chosenUrls.row(item)
            removeRows.append(row)

        removeRows.sort(reverse=True)
        for i, row in enumerate(removeRows):
            self.ui.chosenUrls.takeItem(row)
            self.extractor.logger.debug(f"urlManager_settings::_removeSelectedUrls -> Removed job {self.jobOverride[i].get('url', '')}")
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

    def addChosenUrl(self, url):
        self.ui.chosenUrls.addItem(url)

    def updateJobOverride(self, url: str, appendArgs: str, user: str) -> None:
        userData = VarHelper.returnDictFromMatchedKeyInDictArray(user, "UserHandle", self.userList)
        if not userData:
            self.main.qtHelper.Throw(message=f"{user} was not found in the user table")
            raise Exception(f"{user} was not found in the user table")

        job = self.extractor.settings.getJobs(
            userData,
            self.extractor.config.settings,
            self.main.General.config.settings,
            self.extractor.logic.getBaseConf(userData),
            self.extractor.logic.deepUpdate,
            self.main,
        )[1]

        job["url"] = f"{appendArgs} {url}".strip().rstrip()
        job["type"] = f"{appendArgs} {url}".strip().rstrip()
        job["userData"] = userData
        self.jobOverride.append(job)

        self.extractor.logger.debug(f"urlManager_settings::updateJobOverride -> Created job {job['url']}")

    def startOverride(self):
        self.extractor.logger.debug(f"urlManager_settings::startOverride")
        if self.extractor.loopRunning:
            self.main.qtHelper.Throw(f"{self.extractor.name} is running, force stop it to run the custom job", type=MessageType.INFO)
            return

        if self.main.debug:
            self.main.debuggy("Start extraction", self)
            self.main.debuggy(VarHelper.prettyJson(self.jobOverride), self, noFormat=True)
            string = "\n".join(entry["url"] for entry in self.jobOverride)
            self.main.debuggy(string, self, noFormat=True)

        self.extractor.startExtraction(self.jobOverride, [ExtractorState.CUSTOM_URLS_EXTRACTION, ExtractorState.ANY_URLS_EXTRACTION])
        self.close()
