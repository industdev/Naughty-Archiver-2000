from PySide6.QtCore import QObject, QTimer, QEvent, Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter


class QtLabelScroller(QObject):
    def __init__(self, extractor, label: QLabel, speed: int = 50, step: int = 2):
        super().__init__(label)
        self.label = label
        self.step = step
        self.speed = speed
        self.offset = 0
        self.isError = False
        self.isRunning = False
        self.pendingAction = None

        label.installEventFilter(self)

        #   Timers
        self.scrollTimer = QTimer(self)
        self.scrollTimer.timeout.connect(self.updateOffset)

        self.devilTimer = QTimer(self)
        self.devilTimer.timeout.connect(self.updateDevil)

        self.errorRecoveryTimer = QTimer(self)
        self.errorRecoveryTimer.setSingleShot(True)
        self.errorRecoveryTimer.timeout.connect(self.recoverFromError)

        #   Devil
        self.runningDevil = [
            "( ・∀・)Ψ ",
            "( ・∀・) Ψ",
            " Ψ(・∀・ )",
            "Ψ (・∀・ )",
        ]
        self.idleDevil = "( ∨ω∨ )Zzz"
        self.badDevil = "(/・A・)!"

        self.devilIndex = 0

        #   Text
        self.originalText = label.text()
        self.modifiedText = ""

        extractorName = extractor.name
        self.currentUser = ""
        self.userListLength = "0"
        self.currentDevil = self.idleDevil

        self.runningLabelFormat = extractorName + " extractor - {userListLength} users - Archiving {currentUser} - {devil} | "
        self.idleLabelFormat = extractorName + " extractor - {userListLength} users - {devil}"
        self.errorLabelFormat = extractorName + " extractor - {devil} ~ Ayay!!! "
        self.updateLabelText()

        font = self.label.font()
        font.setFamily("Courier New")
        font.setStyleStrategy(font.StyleStrategy.NoAntialias)
        self.label.setFont(font)
        self.label.update()

    def setUserListLength(self, userCount):
        self.userListLength = str(userCount)
        self.updateLabelText()

    def setCurrentUser(self, userName):
        self.currentUser = userName
        self.updateLabelText()

    def updateLabelText(self):
        if self.isError:
            label = self.errorLabelFormat
        elif self.isRunning:
            label = self.runningLabelFormat
        else:
            label = self.idleLabelFormat

        label = label.replace("{userListLength}", self.userListLength)
        label = label.replace("{currentUser}", self.currentUser)
        label = label.replace("{devil}", self.currentDevil)

        self.modifiedText = label

    def updateDevil(self):
        """Update the devil animation when running"""
        if not self.isError and self.isRunning:
            self.devilIndex = (self.devilIndex + 1) % len(self.runningDevil)
            self.currentDevil = self.runningDevil[self.devilIndex]
            self.updateDisplay()

    def updateOffset(self):
        """Update scrolling offset"""
        if not self.isRunning or self.isError:
            return

        #   Update the modified text
        self.updateLabelText()

        #   Calculate the width of one complete cycle
        cycle_width = self.label.fontMetrics().horizontalAdvance(self.modifiedText)

        if cycle_width <= 0:
            return

        self.offset = (self.offset + self.step) % cycle_width
        self.label.update()

    def updateDisplay(self):
        """Update the display text without changing offset"""
        self.updateLabelText()
        self.label.update()

    def eventFilter(self, obj, event):
        """Custom paint event to handle scrolling text"""
        if obj is self.label and event.type() == QEvent.Type.Paint:
            painter = QPainter(self.label)
            rect = self.label.rect()
            painter.setClipRect(rect)

            # Set text color based on error state
            if self.isError:
                painter.setPen(Qt.GlobalColor.red)
            else:
                painter.setPen(self.label.palette().color(self.label.foregroundRole()))

            single_unit = self.modifiedText
            single_width = self.label.fontMetrics().horizontalAdvance(single_unit)

            if single_width <= 0:
                return True

            font_metrics = self.label.fontMetrics()
            text_height = font_metrics.height()
            y_pos = (rect.height() + text_height) // 2 - font_metrics.descent()

            #   No wrapping when errored or idle
            if not self.isRunning or self.isError:
                text_width = self.label.fontMetrics().horizontalAdvance(single_unit)
                x_pos = (rect.width() - text_width) // 2
                painter.drawText(x_pos, y_pos, single_unit)
            else:
                # Scrolling behavior
                x_pos = -self.offset
                label_width = rect.width()

                # Draw multiple copies to ensure continuous scrolling
                while x_pos < label_width + single_width:
                    painter.drawText(x_pos, y_pos, single_unit)
                    x_pos += single_width

            return True
        return super().eventFilter(obj, event)

    def start(self):
        """Start the scrolling animation and switch to running devil"""
        self.isError = False
        self.pendingAction = None
        self.updateDisplay()

        # Set running state
        self.isRunning = True
        self.devilIndex = 0
        self.currentDevil = self.runningDevil[self.devilIndex]

        # Start timers
        self.scrollTimer.start(self.speed)
        self.devilTimer.start(600)

        self.updateDisplay()

    def stop(self):
        """Stop the scrolling animation and switch to idle devil"""
        # If in error state, queue the stop action
        if self.isError:
            self.pendingAction = "stop"
            return

        # Clear any pending action
        self.pendingAction = None

        # Set idle state
        self.isRunning = False
        self.currentDevil = self.idleDevil

        # Stop timers
        self.scrollTimer.stop()
        self.devilTimer.stop()

        # Reset offset to show text from beginning when stopped
        self.offset = 0
        self.updateDisplay()

    def setSpeed(self, speed: int):
        """Change the animation speed (timer interval in ms)"""
        self.speed = speed
        if self.scrollTimer.isActive():
            self.scrollTimer.setInterval(speed)

    def setStep(self, step: int):
        """Change the scroll step size"""
        self.step = step

    def errorTrigger(self):
        self.isError = True
        self.currentDevil = self.badDevil

        #   Stop all animations during error
        self.scrollTimer.stop()
        self.devilTimer.stop()

        #   Update immediately
        self.updateDisplay()

        self.errorRecoveryTimer.start(1700)

    def recoverFromError(self):
        self.isError = False

        #   Execute pending action if any
        if self.pendingAction == "start":
            self.pendingAction = None
            self.start()
        elif self.pendingAction == "stop":
            self.pendingAction = None
            self.stop()
        else:
            # No pending action, restore previous state
            if self.isRunning:
                # Resume running state
                self.devilIndex = 0
                self.currentDevil = self.runningDevil[self.devilIndex]
                self.scrollTimer.start(self.speed)
                self.devilTimer.start(600)
            else:
                # Return to idle state
                self.currentDevil = self.idleDevil
                self.offset = 0

            self.updateDisplay()
