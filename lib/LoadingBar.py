import os
import time
from PySide6.QtCore import QTimer, QObject
import ctypes

from PySide6.QtWidgets import QApplication
from lib.QtHelper import QtHelper


class LoadingBar(QObject):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        #   Progress tracking
        self.current = 0
        self.maximum = 100
        self.minimum = 10
        self.message = "Loading..."

        self.interval = 100  #  Ms
        self.unit_name = "it"

        #   Display settings
        self.charCount = 70
        self.suffixLength = 0
        self.isActive = False
        self.cmdController = CMDButtonController()

        #   Console state tracking
        self.startTime = 0
        self.lastupdate = 0

    def start(self, maximum=100, message="Loading...", interval=30, name="it", minimum=10):
        self.main.debuggy(
            f"Starting loadingbar: {maximum}max, {interval}ms, {minimum}min, skip:{self.main.General.config.settings['skiploadingbars']}",
            self,
        )

        if maximum < minimum:
            self.isActive = False
            return
        self._resizeConsole()
        self.main.setEnabled(False)
        QApplication.processEvents()
        self.cmdController.disableConsoleOperations(self.message)

        if self.main.General.config.settings["skiploadingbars"]:
            return

        QtHelper._showWinConsole(self.main)

        #   Initialize progress tracking
        self.current = 0
        self.maximum = maximum
        self.minimum = minimum
        self.message = message
        self.interval = interval
        self.unit_name = name
        self.isActive = True
        self.startTime = time.time()

        self.timer.start(self.interval)

        print()
        self.update()

    def increase(self, amount=1):
        self.main.debuggy(f"+{amount}", self, True)

        if not self.isActive:
            return

        if self.main.General.config.settings["skiploadingbars"]:
            return

        self.current = min(self.current + amount, self.maximum)

    def terminate(self):
        self.main.debuggy(f"Terminate", self)
        self.main.setEnabled(True)
        QApplication.processEvents()

        if not self.isActive:
            return

        self.timer.stop()
        self.isActive = False

        #   Final update showing completion
        self.current = self.maximum
        self.update()

        #   Add a final newline for clean output
        print()

        self.cmdController.enableConsoleOperations()

        QtHelper._hideWinConsole(self.main)

        self._restoreConsoleSize()

    def update(self):
        self.main.debuggy(f"update", self)
        if not self.isActive:
            return

        messageAndBarWidth = self.charCount

        #   Message capped at 2/3 total
        maxMessageWidth = (2 * messageAndBarWidth) // 3
        msg = self.message[:maxMessageWidth]
        messageWidth = len(msg)
        barWidth = messageAndBarWidth - messageWidth

        percentage = (self.current / self.maximum) * 100 if self.maximum > 0 else 100

        #   Build bar
        filledWidth = int((self.current / self.maximum) * barWidth) if self.maximum > 0 else barWidth
        bar = f" [{'█' * filledWidth}{'░' * (barWidth - filledWidth)}]"

        #   Build suffix
        elapsedTime = time.time() - self.startTime
        speed = f"{(self.current / elapsedTime):.1f}{self.unit_name}/s" if elapsedTime > 0 else f"0.0{self.unit_name}/s"

        if self.current > 0 and self.current < self.maximum and elapsedTime > 0:
            eta = (elapsedTime / self.current) * (self.maximum - self.current)
            etaString = self._format_time(eta)
        else:
            etaString = "00:00"

        elapsedString = self._format_time(elapsedTime)

        #   Core (message + bar only, fixed to charCount)
        ctypes.windll.kernel32.SetConsoleTitleW(msg)
        core = f"{msg}{bar}"
        suffix = f"{percentage:3.0f}% | {speed} | {elapsedString} | ETA:{etaString}"
        self.suffixLength = len(suffix)
        line = f"{core} {suffix}"

        #   Clear remnants of previous longer lines
        paddedLine = line.ljust(messageAndBarWidth + len(suffix))
        print(f"\033[1A\r{paddedLine}", end="", flush=True)

    def _format_time(self, seconds):
        """Format seconds into MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def get_progress(self):
        """
        Get the current progress information

        Returns:
            dict: Dictionary containing current progress information
        """
        if self.maximum > 0:
            percentage = (self.current / self.maximum) * 100
        else:
            percentage = 100

        return {
            "current": self.current,
            "maximum": self.maximum,
            "percentage": percentage,
            "message": self.message,
            "isActive": self.isActive,
            "elapsedTime": time.time() - self.startTime if self.isActive else 0,
        }

    def _resizeConsole(self):
        """Resize console to a compact size suitable for progress display."""
        try:
            os.system(f"mode con lines=2 cols={self.charCount + self.suffixLength + 6}")
        except Exception:
            pass

    def _restoreConsoleSize(self):
        try:
            os.system("mode con lines=25 cols=80")
        except Exception:
            pass


#   Courtesy of Claude Sonnet 4
class CMDButtonController:
    def __init__(self):
        self.hwnd = None
        self.originalStyle = None
        self.originalExStyle = None

        # Windows API constants
        self.GWL_STYLE = -16
        self.GWL_EXSTYLE = -20

        # Window style constants
        self.WS_SYSMENU = 0x00080000  # System menu (includes close button)
        self.WS_MINIMIZEBOX = 0x00020000  # Minimize button
        self.WS_MAXIMIZEBOX = 0x00010000  # Maximize button
        self.WS_THICKFRAME = 0x00040000  # Resizable border

        self.user32 = ctypes.windll.user32  # type: ignore
        self.kernel32 = ctypes.windll.kernel32  # type: ignore
        self._get_console_window()

    def _get_console_window(self):
        """Get the handle of the current console window"""
        self.hwnd = self.kernel32.GetConsoleWindow()
        if not self.hwnd:
            raise Exception("Could not get console window handle")

    def _get_window_style(self):
        """Get current window style"""
        return self.user32.GetWindowLongW(self.hwnd, self.GWL_STYLE)

    def _set_window_style(self, style):
        """Set window style"""
        return self.user32.SetWindowLongW(self.hwnd, self.GWL_STYLE, style)

    def disableConsoleOperations(self, title):
        """Hide the close, minimize, and maximize buttons"""
        if not self.hwnd:
            self._get_console_window()

        self.originalStyle = self._get_window_style()

        new_style = self.originalStyle
        new_style &= ~self.WS_SYSMENU  # Remove close button and system menu
        new_style &= ~self.WS_MINIMIZEBOX  # Remove minimize button
        new_style &= ~self.WS_MAXIMIZEBOX  # Remove maximize button
        new_style &= ~self.WS_THICKFRAME  # Remove resizable frame
        self._set_window_style(new_style)

        ctypes.windll.kernel32.SetConsoleTitleW(title)
        self.user32.SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, 0x0027)  # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER

        return True

    def enableConsoleOperations(self):
        """Restore the original window buttons"""
        if not self.hwnd or self.originalStyle is None:
            return False

        self._set_window_style(self.originalStyle)
        ctypes.windll.kernel32.SetConsoleTitleW("Naughty archiver 2000")
        self.user32.SetWindowPos(self.hwnd, 0, 0, 0, 0, 0, 0x0027)  # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER

        return True
