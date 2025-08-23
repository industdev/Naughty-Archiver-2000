import sys
import time
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt, QTimer, QEventLoop
from PySide6.QtGui import QGuiApplication


class LoadingBar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._max = 0
        self._current = 0
        self._displayed_value = -1  # Track displayed value to avoid unnecessary updates

        # Timer for UI updates
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._updateUI)
        self._interval_ms = 100  # Default update interval

        # Setup UI
        self._setup()

        # Non-modal to avoid blocking
        self.setModal(False)
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )

    def start(self, maxSize: int, message="Please wait...", interval_ms: int = 100) -> None:
        """Initialize and show the loading bar."""
        self._max = maxSize
        self._current = 0
        self._displayed_value = -1  # Reset displayed value tracking
        self._startTime = time.perf_counter()
        self._interval_ms = max(50, interval_ms)  # Minimum 50ms

        self.setWindowTitle(message)
        self._progressBar.setMaximum(self._max)
        self._progressBar.setValue(0)

        # Ensure proper window display
        self._force_show()

        # Start timer for UI updates
        self._update_timer.start(self._interval_ms)

    def _force_show(self):
        """Ensure the window is properly shown and visible."""
        self.show()
        self.raise_()
        self.activateWindow()

        # Force immediate display with minimal event processing
        QApplication.processEvents(QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)

    def increase(self, amount: int = 1):
        """Increase progress - FAST operation with no UI updates."""
        self._current = min(self._current + amount, self._max)

    def setValue(self, value):
        """Set progress to a specific value."""
        self._current = max(0, min(value, self._max))

    def forceUpdate(self):
        """Force an immediate UI update."""
        self._updateUI()

    def terminate(self):
        """Close the loading bar."""
        self._update_timer.stop()
        self._current = self._max
        self._updateUI()  # Final update
        self.accept()

    def isComplete(self):
        """Check if progress is complete."""
        return self._current >= self._max

    def getElapsedTime(self):
        """Get elapsed time since loading bar was shown."""
        if self._startTime:
            return time.perf_counter() - self._startTime
        return 0

    def _setup(self):
        """Internal setup of the dialog UI."""
        self.setFixedSize(400, 60)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(15, 15, 15, 15)

        self._progressBar = QProgressBar()
        self._progressBar.setMinimum(0)
        self._progressBar.setMaximum(100)
        self._progressBar.setValue(0)
        self._progressBar.setTextVisible(True)

        layout.addWidget(self._progressBar)
        self.setLayout(layout)

    def _updateUI(self):
        """Update the progress bar UI - called ONLY by timer."""
        # Only update if value has changed
        if self._displayed_value != self._current:
            self._displayed_value = self._current
            self._progressBar.setValue(self._current)

    # Prevent ESC key from closing
    def reject(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)
