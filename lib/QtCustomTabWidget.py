from PySide6.QtWidgets import QWidget, QListWidgetItem
from PySide6.QtCore import Signal

from lib.ui.QtCustomTabWidget_ui import Ui_Form
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp


class QtCustomTabWidget(QWidget):
    currentChanged = Signal(int)

    def __init__(self, main: "MainApp", parent=None):
        super().__init__(parent)
        self.main = main

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.connectSignals()
        self.ui.cfg_list.clear()

        #   Remove all pages before
        pages = self.ui.cfg_windows.count()
        for i in range(pages):
            widget = self.ui.cfg_windows.widget(0)
            self.ui.cfg_windows.removeWidget(widget)

        self.ui.btn_showHideList.setText("")
        self.main.qtHelper.setIcon(self.ui.btn_showHideList, "comdlg32_578_l.ico")

    def connectSignals(self):
        self.ui.cfg_list.currentRowChanged.connect(self.onListSelectionChanged)
        self.ui.btn_showHideList.clicked.connect(self.toggleListVisibility)

    def addTab(self, widget, tabName):
        self.main.debuggy(
            f"Adding tab '{tabName}' - Before: List count: {self.ui.cfg_list.count()}, Stack count: {self.ui.cfg_windows.count()}", self
        )

        self.ui.cfg_windows.addWidget(widget)
        item = QListWidgetItem(tabName)
        self.ui.cfg_list.addItem(item)

        self.main.debuggy(
            f"After adding tab '{tabName}' - List count: {self.ui.cfg_list.count()}, Stack count: {self.ui.cfg_windows.count()}", self
        )

        # If this is the first tab, select it
        if self.ui.cfg_list.count() == 1:
            self.main.debuggy("Setting first tab as current (row 0)", self)
            self.ui.cfg_list.setCurrentRow(0)
            self.main.debuggy(
                f"After setting current row - List current: {self.ui.cfg_list.currentRow()}, Stack current: {self.ui.cfg_windows.currentIndex()}",
                self,
            )

    def removeTab(self, index):
        """Remove a tab at the specified index"""
        self.main.debuggy(f"Removing tab at index {index}", self)
        if 0 <= index < self.ui.cfg_windows.count():
            widget = self.ui.cfg_windows.widget(index)
            self.ui.cfg_windows.removeWidget(widget)

            item = self.ui.cfg_list.takeItem(index)
            if item:
                del item

    def currentIndex(self):
        """Get the current tab index"""
        current = self.ui.cfg_list.currentRow()
        self.main.debuggy(f"currentIndex() called - returning {current}", self)
        return current

    def setCurrentIndex(self, index):
        """Set the current tab by index"""
        self.main.debuggy(f"setCurrentIndex({index}) called - List count: {self.ui.cfg_list.count()}", self)
        if 0 <= index < self.ui.cfg_list.count():
            self.ui.cfg_list.setCurrentRow(index)
            self.main.debuggy(f"Set current row to {index} - Actual current row: {self.ui.cfg_list.currentRow()}", self)

    def onListSelectionChanged(self, currentRow):
        """Handle list widget selection changes"""
        self.main.debuggy(f"onListSelectionChanged called with currentRow: {currentRow}", self)
        self.main.debuggy(f"Stack widget current index before change: {self.ui.cfg_windows.currentIndex()}", self)

        if currentRow >= 0:
            self.ui.cfg_windows.setCurrentIndex(currentRow)
            self.main.debuggy(f"Stack widget current index after change: {self.ui.cfg_windows.currentIndex()}", self)
            self.currentChanged.emit(currentRow)
            self.main.debuggy(f"Emitted currentChanged signal with index: {currentRow}", self)

    def toggleListVisibility(self):
        """Toggle the visibility of the list widget"""
        if self.ui.cfg_list.isVisible():
            self.main.qtHelper.setIcon(self.ui.btn_showHideList, "comdlg32_578_r.ico")
            self.ui.cfg_list.hide()
        else:
            self.main.qtHelper.setIcon(self.ui.btn_showHideList, "comdlg32_578_l.ico")
            self.ui.cfg_list.show()

    def setTabIcon(self, index, icon):
        if 0 <= index < self.ui.cfg_list.count():
            item = self.ui.cfg_list.item(index)
            if item:
                item.setIcon(icon)
