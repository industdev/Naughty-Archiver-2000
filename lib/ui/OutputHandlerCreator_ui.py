from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_Creator(object):
    def setupUi(self, Creator):
        if not Creator.objectName():
            Creator.setObjectName("Creator")
        Creator.resize(1140, 628)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        Creator.setPalette(palette)
        self.horizontalLayout = QHBoxLayout(Creator)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.leftSide = QWidget(Creator)
        self.leftSide.setObjectName("leftSide")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftSide.sizePolicy().hasHeightForWidth())
        self.leftSide.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.leftSide)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.box_entry = QGroupBox(self.leftSide)
        self.box_entry.setObjectName("box_entry")
        self.formLayout_4 = QFormLayout(self.box_entry)
        self.formLayout_4.setObjectName("formLayout_4")
        self.formLayout_4.setContentsMargins(-1, 4, -1, -1)
        self.label_11 = QLabel(self.box_entry)
        self.label_11.setObjectName("label_11")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.cfg_key = QLineEdit(self.box_entry)
        self.cfg_key.setObjectName("cfg_key")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfg_key)

        self.verticalLayout_2.addWidget(self.box_entry)

        self.box_box = QGroupBox(self.leftSide)
        self.box_box.setObjectName("box_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.box_box.sizePolicy().hasHeightForWidth())
        self.box_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.box_box)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 4, -1, -1)
        self.widget_10 = QWidget(self.box_box)
        self.widget_10.setObjectName("widget_10")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(self.widget_10)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout = QVBoxLayout(self.widget_7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 4)
        self.label_2 = QLabel(self.widget_7)
        self.label_2.setObjectName("label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.cfg_messageOnLine = QPlainTextEdit(self.widget_7)
        self.cfg_messageOnLine.setObjectName("cfg_messageOnLine")

        self.verticalLayout.addWidget(self.cfg_messageOnLine)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_9.addWidget(self.widget_7)

        self.widget_9 = QWidget(self.widget_10)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_3 = QVBoxLayout(self.widget_9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 4)
        self.label = QLabel(self.widget_9)
        self.label.setObjectName("label")

        self.verticalLayout_3.addWidget(self.label)

        self.cfg_messageOnAction = QPlainTextEdit(self.widget_9)
        self.cfg_messageOnAction.setObjectName("cfg_messageOnAction")

        self.verticalLayout_3.addWidget(self.cfg_messageOnAction)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.horizontalLayout_9.addWidget(self.widget_9)

        self.verticalLayout_4.addWidget(self.widget_10)

        self.widget_11 = QWidget(self.box_box)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_11)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(9, 0, 0, 0)
        self.label_3 = QLabel(self.widget_11)
        self.label_3.setObjectName("label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.label_3)

        self.cfg_lineLevel = QComboBox(self.widget_11)
        self.cfg_lineLevel.setObjectName("cfg_lineLevel")

        self.horizontalLayout_7.addWidget(self.cfg_lineLevel)

        self.cfg_inhibitBox = QCheckBox(self.widget_11)
        self.cfg_inhibitBox.setObjectName("cfg_inhibitBox")

        self.horizontalLayout_7.addWidget(self.cfg_inhibitBox)

        self.verticalLayout_4.addWidget(self.widget_11)

        self.verticalLayout_2.addWidget(self.box_box)

        self.box_action = QGroupBox(self.leftSide)
        self.box_action.setObjectName("box_action")
        self.box_action.setFlat(False)
        self.box_action.setCheckable(False)
        self.gridLayout_3 = QGridLayout(self.box_action)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, 4, -1, 9)
        self.widget_3 = QWidget(self.box_action)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.widget_3)
        self.label_6.setObjectName("label_6")
        self.label_6.setMinimumSize(QSize(128, 0))

        self.horizontalLayout_6.addWidget(self.label_6)

        self.cfg_actionResetAt = QSpinBox(self.widget_3)
        self.cfg_actionResetAt.setObjectName("cfg_actionResetAt")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cfg_actionResetAt.sizePolicy().hasHeightForWidth())
        self.cfg_actionResetAt.setSizePolicy(sizePolicy3)
        self.cfg_actionResetAt.setMinimumSize(QSize(64, 0))
        self.cfg_actionResetAt.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_6.addWidget(self.cfg_actionResetAt)

        self.label_7 = QLabel(self.widget_3)
        self.label_7.setObjectName("label_7")
        self.label_7.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_6.addWidget(self.label_7)

        self.cfg_actionNeverReset = QCheckBox(self.widget_3)
        self.cfg_actionNeverReset.setObjectName("cfg_actionNeverReset")

        self.horizontalLayout_6.addWidget(self.cfg_actionNeverReset)

        self.horizontalSpacer_2 = QSpacerItem(0, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.gridLayout_3.addWidget(self.widget_3, 2, 0, 1, 1)

        self.widget = QWidget(self.box_action)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_3.addWidget(self.widget, 1, 0, 1, 1)

        self.widget_6 = QWidget(self.box_action)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_6)
        self.label_4.setObjectName("label_4")
        self.label_4.setMinimumSize(QSize(128, 0))

        self.horizontalLayout_3.addWidget(self.label_4)

        self.cfg_actionAfterLinesSeen = QSpinBox(self.widget_6)
        self.cfg_actionAfterLinesSeen.setObjectName("cfg_actionAfterLinesSeen")
        sizePolicy3.setHeightForWidth(self.cfg_actionAfterLinesSeen.sizePolicy().hasHeightForWidth())
        self.cfg_actionAfterLinesSeen.setSizePolicy(sizePolicy3)
        self.cfg_actionAfterLinesSeen.setMinimumSize(QSize(64, 0))
        self.cfg_actionAfterLinesSeen.setMaximumSize(QSize(64, 16777215))

        self.horizontalLayout_3.addWidget(self.cfg_actionAfterLinesSeen)

        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.cfg_action = QComboBox(self.widget_6)
        self.cfg_action.setObjectName("cfg_action")
        sizePolicy3.setHeightForWidth(self.cfg_action.sizePolicy().hasHeightForWidth())
        self.cfg_action.setSizePolicy(sizePolicy3)
        self.cfg_action.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_3.addWidget(self.cfg_action)

        self.gridLayout_3.addWidget(self.widget_6, 0, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.box_action)

        self.widget_4 = QWidget(self.leftSide)
        self.widget_4.setObjectName("widget_4")
        sizePolicy1.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy1)
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.box_event = QGroupBox(self.widget_4)
        self.box_event.setObjectName("box_event")
        sizePolicy1.setHeightForWidth(self.box_event.sizePolicy().hasHeightForWidth())
        self.box_event.setSizePolicy(sizePolicy1)
        self.formLayout_3 = QFormLayout(self.box_event)
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout_3.setContentsMargins(-1, 4, -1, -1)
        self.label_8 = QLabel(self.box_event)
        self.label_8.setObjectName("label_8")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.cfg_runEvent = QComboBox(self.box_event)
        self.cfg_runEvent.setObjectName("cfg_runEvent")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfg_runEvent)

        self.horizontalLayout_5.addWidget(self.box_event)

        self.box_mask = QGroupBox(self.widget_4)
        self.box_mask.setObjectName("box_mask")
        sizePolicy1.setHeightForWidth(self.box_mask.sizePolicy().hasHeightForWidth())
        self.box_mask.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.box_mask)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 4, -1, -1)
        self.label_9 = QLabel(self.box_mask)
        self.label_9.setObjectName("label_9")

        self.horizontalLayout_4.addWidget(self.label_9)

        self.cfg_mask = QComboBox(self.box_mask)
        self.cfg_mask.setObjectName("cfg_mask")

        self.horizontalLayout_4.addWidget(self.cfg_mask)

        self.horizontalLayout_5.addWidget(self.box_mask)

        self.verticalLayout_2.addWidget(self.widget_4)

        self.bottomLabel = QLabel(self.leftSide)
        self.bottomLabel.setObjectName("bottomLabel")
        palette1 = QPalette()
        brush1 = QBrush(QColor(193, 193, 193, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        self.bottomLabel.setPalette(palette1)

        self.verticalLayout_2.addWidget(self.bottomLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout.addWidget(self.leftSide)

        self.widget_5 = QWidget(Creator)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_5 = QVBoxLayout(self.widget_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, -1, -1, 0)
        self.listWidget = QListWidget(self.widget_5)
        self.listWidget.setObjectName("listWidget")

        self.verticalLayout_5.addWidget(self.listWidget)

        self.widget_8 = QWidget(self.widget_5)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_8.setSpacing(2)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 2, 0, 0)
        self.btn_removeSelected = QPushButton(self.widget_8)
        self.btn_removeSelected.setObjectName("btn_removeSelected")

        self.horizontalLayout_8.addWidget(self.btn_removeSelected)

        self.btn_duplicateSelected = QPushButton(self.widget_8)
        self.btn_duplicateSelected.setObjectName("btn_duplicateSelected")

        self.horizontalLayout_8.addWidget(self.btn_duplicateSelected)

        self.btn_newEntry = QPushButton(self.widget_8)
        self.btn_newEntry.setObjectName("btn_newEntry")

        self.horizontalLayout_8.addWidget(self.btn_newEntry)

        self.btn_moveUp = QPushButton(self.widget_8)
        self.btn_moveUp.setObjectName("btn_moveUp")
        self.btn_moveUp.setMaximumSize(QSize(20, 16777215))
        self.btn_moveUp.setAutoRepeat(True)
        self.btn_moveUp.setAutoRepeatDelay(250)
        self.btn_moveUp.setAutoRepeatInterval(80)

        self.horizontalLayout_8.addWidget(self.btn_moveUp)

        self.btn_moveDown = QPushButton(self.widget_8)
        self.btn_moveDown.setObjectName("btn_moveDown")
        self.btn_moveDown.setMaximumSize(QSize(20, 16777215))
        self.btn_moveDown.setAutoRepeat(True)
        self.btn_moveDown.setAutoRepeatDelay(250)
        self.btn_moveDown.setAutoRepeatInterval(140)

        self.horizontalLayout_8.addWidget(self.btn_moveDown)

        self.verticalLayout_5.addWidget(self.widget_8)

        self.horizontalLayout.addWidget(self.widget_5)

        self.retranslateUi(Creator)

        QMetaObject.connectSlotsByName(Creator)

    # setupUi

    def retranslateUi(self, Creator):
        Creator.setWindowTitle(QCoreApplication.translate("Creator", "Form", None))
        self.box_entry.setTitle(QCoreApplication.translate("Creator", "Entry", None))
        self.label_11.setText(QCoreApplication.translate("Creator", "Match", None))
        # if QT_CONFIG(tooltip)
        self.cfg_key.setToolTip(
            QCoreApplication.translate(
                "Creator",
                "<html><head/><body><p>Do all the things below if gallery-dl matches this output</p><p>This will be converted into a case-insensitive regex group, so you have to escape everything properly</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_key.setText("")
        self.cfg_key.setPlaceholderText(QCoreApplication.translate("Creator", "String (Regex string of text to match)", None))
        # if QT_CONFIG(tooltip)
        self.box_box.setToolTip(QCoreApplication.translate("Creator", "Define a message box pop-up when the message is seen", None))
        # endif // QT_CONFIG(tooltip)
        self.box_box.setTitle(QCoreApplication.translate("Creator", "Box", None))
        self.label_2.setText(QCoreApplication.translate("Creator", "Message box on Line", None))
        self.cfg_messageOnLine.setPlaceholderText(QCoreApplication.translate("Creator", "String (Message)", None))
        self.label.setText(QCoreApplication.translate("Creator", "Message box on Action", None))
        self.cfg_messageOnAction.setPlainText("")
        self.cfg_messageOnAction.setPlaceholderText(QCoreApplication.translate("Creator", "String (Message)", None))
        self.label_3.setText(QCoreApplication.translate("Creator", "Change log level to", None))
        # if QT_CONFIG(tooltip)
        self.cfg_lineLevel.setToolTip(
            QCoreApplication.translate("Creator", "<html><head/><body><p>Change the level and color of the text</p></body></html>", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.cfg_inhibitBox.setToolTip(
            QCoreApplication.translate(
                "Creator",
                "<html><head/><body><p>Don't throw any box, just log to the screen the contents of the box</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_inhibitBox.setText(QCoreApplication.translate("Creator", "Don't throw message box, just log", None))
        # if QT_CONFIG(tooltip)
        self.box_action.setToolTip(QCoreApplication.translate("Creator", "Define an extractor action when the text is seen", None))
        # endif // QT_CONFIG(tooltip)
        self.box_action.setTitle(QCoreApplication.translate("Creator", "Action", None))
        self.label_6.setText(QCoreApplication.translate("Creator", "Reset the counter every ", None))
        # if QT_CONFIG(tooltip)
        self.cfg_actionResetAt.setToolTip(
            QCoreApplication.translate(
                "Creator", "Forget about how many times it has seen the message after this amount of lines pass", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("Creator", "lines or", None))
        # if QT_CONFIG(tooltip)
        self.cfg_actionNeverReset.setToolTip(
            QCoreApplication.translate("Creator", "Never reset the counter of times it has seen the message", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_actionNeverReset.setText(QCoreApplication.translate("Creator", "Never reset", None))
        self.label_4.setText(QCoreApplication.translate("Creator", "When this text is seen", None))
        # if QT_CONFIG(tooltip)
        self.cfg_actionAfterLinesSeen.setToolTip(
            QCoreApplication.translate(
                "Creator", "If the text is read this amount of times before it gets reset, then run the action", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Creator", "times", None))
        # if QT_CONFIG(tooltip)
        self.cfg_action.setToolTip(QCoreApplication.translate("Creator", "Run this action ", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.box_event.setToolTip(
            QCoreApplication.translate(
                "Creator", "Define an event from those available that the extractor should run, leave it at None if you are unsure", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.box_event.setTitle(QCoreApplication.translate("Creator", "Event", None))
        self.label_8.setText(QCoreApplication.translate("Creator", "Run event", None))
        # if QT_CONFIG(tooltip)
        self.cfg_runEvent.setToolTip(
            QCoreApplication.translate(
                "Creator",
                "<html><head/><body><p>Select an event to run</p><p>Enum.py::EventNames has a list of events for combo boxes, then GalleryOutputHandler.py calls OutputEvent.py's functions</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.box_mask.setToolTip(QCoreApplication.translate("Creator", "Only act if extractor's state matches the mask", None))
        # endif // QT_CONFIG(tooltip)
        self.box_mask.setTitle(QCoreApplication.translate("Creator", "Mask", None))
        self.label_9.setText(QCoreApplication.translate("Creator", "Only consider when extractor", None))
        # if QT_CONFIG(tooltip)
        self.cfg_mask.setToolTip(
            QCoreApplication.translate(
                "Creator",
                "<html><head/><body><p>Don't do any of the above if the current extractor's state/operation doesn't match the following Mask<br/>'is running' always matches</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.bottomLabel.setText(QCoreApplication.translate("Creator", "Settings saved on exit", None))
        self.btn_removeSelected.setText(QCoreApplication.translate("Creator", "Remove", None))
        self.btn_duplicateSelected.setText(QCoreApplication.translate("Creator", "Duplicate", None))
        self.btn_newEntry.setText(QCoreApplication.translate("Creator", "New", None))
        self.btn_moveUp.setText(QCoreApplication.translate("Creator", "\u2191", None))
        self.btn_moveDown.setText(QCoreApplication.translate("Creator", "\u2193", None))

    # retranslateUi
