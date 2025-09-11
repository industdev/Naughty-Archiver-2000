from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp

from PySide6.QtWidgets import QWidget
from lib.ui.Statistics_ui import Ui_Form
from lib.StatCounter import StatCounter
import time


class StatisticsTab(QWidget):
    def __init__(self, main: "MainApp"):
        start = time.perf_counter()

        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.counter = StatCounter(main, self.ui)

        #   Ui overrides
        self.setObjectName("TabStatistics")
        self.setAutoFillBackground(True)

        main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")
