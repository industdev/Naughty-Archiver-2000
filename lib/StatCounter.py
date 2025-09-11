from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
from PySide6.QtGui import QMovie
from lib.ConfigManager import ConfigManager
import threading
import os


class StatCounter:
    def __init__(self, main, statisticsUi):
        self.main = main
        self.inv = self.main._inv

        self.statsUi = statisticsUi

        self.statsUi.lbl_totAmount.setText("Violated users: ")
        self.statsUi.lbl_totSize.setText("Times opened: ")
        self.statsUi.lbl_totMetadataSize.setText("Metadata size: ")
        self.statsUi.lbl_totMediaSize.setText("Media size: ")
        self.statsUi.lbl_totMetadataAmount.setText("Metadata extracted: ")
        self.statsUi.lbl_totMediaAmount.setText("Media extracted: ")
        self.statsUi.lbl_totApiCalls.setText("Api calls: ")
        self.statsUi.lbl_totExtractorsRuns.setText("Extractors runs: ")
        self.statsUi.lbl_totExtractorsRuntime.setText("Extractors ran for: ")

        template = {
            "totAmount": 0,
            "totSize": 0,
            "totMediaAmount": 0,
            "totMediaSize": 0,
            "totMetadataAmount": 0,
            "totMetadataSize": 0,
            "totApiCalls": 0,
            "totExtractorsRuntime": 0,
            "totExtractorsRuns": 0,
            "since": None,
        }
        config = os.path.join(self.main._extConfigDPath, "Stats.json")
        self.config = ConfigManager(main, template, config, "Stats", self)

        self.secret = self.statsUi.image

        if not self.main.General.config.settings["supersecretoption"]:
            self.updateDrawing = self.null

        self.updateDrawing(0)
        self.S_COUNTER = threading.Lock()

    def increase(self, amount, type, save=True):
        if self.main.General.config.settings["nostatsupdate"]:
            return

        with self.S_COUNTER:
            self.config.settings[f"{type}"] += amount
            value = self.config.settings[f"{type}"]

            labelText = getattr(self.statsUi, f"lbl_{type}")
            labelPulse = getattr(self.statsUi, f"d_{type}")

            # Format
            if type in ("totMediaSize", "totMetadataSize"):
                valueFormat = "toSize"
            elif type == "totExtractorsRuntime":
                valueFormat = "toTime"
            else:
                valueFormat = None

            self.inv(lambda p=labelPulse: StatCounter.flash(p, "#00FF00"))
            self.inv(lambda l=labelText, v=value, f=valueFormat: self.setLabel(l, v, f))
            if save:
                self.config.saveConfig()

    def setLabel(self, label: QLabel, value, valueFormat=None):
        text = label.text()
        base = text.split(":")[0]

        if valueFormat == "toSize":
            value = self.toSize(value)

        if valueFormat == "toTime":
            value = self.toTime(value)

        label.setText(f"{base}: {value}")

    @staticmethod
    def flash(label: QLabel, new: str, duration: int = 200):
        label.setStyleSheet(f"color: {new};")
        QTimer.singleShot(duration, lambda: label.setStyleSheet(f"color: #000000;"))

    @staticmethod
    def toSize(bytes):
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = float(bytes)
        uIndex = 0

        while size >= 1000 and uIndex < len(units) - 1:
            size /= 1000
            uIndex += 1

        if uIndex == 0:
            return f"{int(size)} {units[uIndex]}"
        return f"{size:.2f} {units[uIndex]}"

    @staticmethod
    def toTime(seconds):
        if seconds < 60:
            return f"{seconds} sec"

        time_units = [("day", 86400), ("hr", 3600), ("min", 60), ("s", 1)]

        parts = []
        for name, count in time_units:
            value = seconds // count
            if value:
                parts.append(f"{value} {name}{'s' if value > 1 and name != 'hr' and name != 's' else ''}")
                seconds %= count

        return " ".join(parts)

    def updateDrawing(self, value):
        try:
            self.secret.show()
            filename = f"{value}"
            path = f"{self.main._animPath}/{filename}"
            movie = QMovie(path)
            self.secret.setMovie(movie)
            movie.start()
        except Exception as e:
            self.main.cmd.info(f"Drawing: {e}")

    def null(self, value):
        pass
