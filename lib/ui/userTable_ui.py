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
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Ui_UserTable(object):
    def setupUi(self, UserTable):
        if not UserTable.objectName():
            UserTable.setObjectName("UserTable")
        UserTable.resize(667, 397)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        UserTable.setPalette(palette)
        self.verticalLayout = QVBoxLayout(UserTable)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.cfgui_tableWidget = QTableWidget(UserTable)
        self.cfgui_tableWidget.setObjectName("cfgui_tableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgui_tableWidget.sizePolicy().hasHeightForWidth())
        self.cfgui_tableWidget.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies(["Courier New"])
        font.setStyleStrategy(QFont.NoAntialias)
        self.cfgui_tableWidget.setFont(font)
        self.cfgui_tableWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.cfgui_tableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.AnyKeyPressed
            | QAbstractItemView.EditTrigger.CurrentChanged
            | QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.cfgui_tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.cfgui_tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cfgui_tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cfgui_tableWidget.setSortingEnabled(True)
        self.cfgui_tableWidget.horizontalHeader().setVisible(True)
        self.cfgui_tableWidget.horizontalHeader().setMinimumSectionSize(0)
        self.cfgui_tableWidget.horizontalHeader().setHighlightSections(True)
        self.cfgui_tableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.cfgui_tableWidget.verticalHeader().setDefaultSectionSize(27)

        self.verticalLayout.addWidget(self.cfgui_tableWidget)

        self.line = QFrame(UserTable)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.widget = QWidget(UserTable)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 0, 2, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.widget_2)

        self.cfgui_addtable = QTableWidget(self.widget)
        self.cfgui_addtable.setObjectName("cfgui_addtable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cfgui_addtable.sizePolicy().hasHeightForWidth())
        self.cfgui_addtable.setSizePolicy(sizePolicy1)
        self.cfgui_addtable.setMinimumSize(QSize(640, 0))
        self.cfgui_addtable.setMaximumSize(QSize(16777215, 80))
        font1 = QFont()
        font1.setFamilies(["Courier New"])
        font1.setPointSize(9)
        self.cfgui_addtable.setFont(font1)
        self.cfgui_addtable.setFrameShadow(QFrame.Shadow.Plain)
        self.cfgui_addtable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cfgui_addtable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.cfgui_addtable.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.cfgui_addtable.setDragDropOverwriteMode(False)
        self.cfgui_addtable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.cfgui_addtable.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cfgui_addtable.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cfgui_addtable.setGridStyle(Qt.PenStyle.SolidLine)
        self.cfgui_addtable.setWordWrap(False)
        self.cfgui_addtable.setCornerButtonEnabled(False)
        self.cfgui_addtable.horizontalHeader().setVisible(True)
        self.cfgui_addtable.horizontalHeader().setMinimumSectionSize(0)
        self.cfgui_addtable.horizontalHeader().setHighlightSections(False)
        self.cfgui_addtable.horizontalHeader().setStretchLastSection(True)
        self.cfgui_addtable.verticalHeader().setVisible(False)
        self.cfgui_addtable.verticalHeader().setMinimumSectionSize(16)
        self.cfgui_addtable.verticalHeader().setDefaultSectionSize(16)
        self.cfgui_addtable.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.cfgui_addtable)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.widget_3.setMinimumSize(QSize(0, 48))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 2, 0, 2)
        self.exportimport = QWidget(self.widget_3)
        self.exportimport.setObjectName("exportimport")
        self.horizontalLayout_5 = QHBoxLayout(self.exportimport)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_saveClose = QPushButton(self.exportimport)
        self.btn_saveClose.setObjectName("btn_saveClose")
        self.btn_saveClose.setMinimumSize(QSize(44, 44))

        self.horizontalLayout_5.addWidget(self.btn_saveClose)

        self.btn_discardClose = QPushButton(self.exportimport)
        self.btn_discardClose.setObjectName("btn_discardClose")
        self.btn_discardClose.setMinimumSize(QSize(44, 44))

        self.horizontalLayout_5.addWidget(self.btn_discardClose)

        self.horizontalLayout_2.addWidget(self.exportimport)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_importList_2 = QPushButton(self.widget_5)
        self.btn_importList_2.setObjectName("btn_importList_2")
        self.btn_importList_2.setMinimumSize(QSize(0, 44))

        self.horizontalLayout_4.addWidget(self.btn_importList_2)

        self.btn_exportList_2 = QPushButton(self.widget_5)
        self.btn_exportList_2.setObjectName("btn_exportList_2")
        self.btn_exportList_2.setMinimumSize(QSize(0, 44))

        self.horizontalLayout_4.addWidget(self.btn_exportList_2)

        self.horizontalLayout_2.addWidget(self.widget_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_duplicateUser = QPushButton(self.widget_3)
        self.btn_duplicateUser.setObjectName("btn_duplicateUser")
        self.btn_duplicateUser.setMinimumSize(QSize(90, 44))

        self.horizontalLayout_2.addWidget(self.btn_duplicateUser)

        self.btn_removeUser = QPushButton(self.widget_3)
        self.btn_removeUser.setObjectName("btn_removeUser")
        self.btn_removeUser.setMinimumSize(QSize(90, 44))

        self.horizontalLayout_2.addWidget(self.btn_removeUser)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName("widget_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy2)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_moveUp = QPushButton(self.widget_4)
        self.btn_moveUp.setObjectName("btn_moveUp")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_moveUp.sizePolicy().hasHeightForWidth())
        self.btn_moveUp.setSizePolicy(sizePolicy3)
        self.btn_moveUp.setMinimumSize(QSize(24, 44))
        self.btn_moveUp.setMaximumSize(QSize(16, 16777215))
        self.btn_moveUp.setAutoRepeat(True)
        self.btn_moveUp.setAutoRepeatDelay(240)
        self.btn_moveUp.setAutoRepeatInterval(80)

        self.horizontalLayout_3.addWidget(self.btn_moveUp)

        self.btn_moveDown = QPushButton(self.widget_4)
        self.btn_moveDown.setObjectName("btn_moveDown")
        sizePolicy3.setHeightForWidth(self.btn_moveDown.sizePolicy().hasHeightForWidth())
        self.btn_moveDown.setSizePolicy(sizePolicy3)
        self.btn_moveDown.setMinimumSize(QSize(24, 44))
        self.btn_moveDown.setMaximumSize(QSize(16, 16777215))
        self.btn_moveDown.setAutoRepeat(True)
        self.btn_moveDown.setAutoRepeatDelay(240)
        self.btn_moveDown.setAutoRepeatInterval(80)

        self.horizontalLayout_3.addWidget(self.btn_moveDown)

        self.horizontalLayout_2.addWidget(self.widget_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.combo_insertPlace = QComboBox(self.widget_3)
        self.combo_insertPlace.addItem("")
        self.combo_insertPlace.addItem("")
        self.combo_insertPlace.addItem("")
        self.combo_insertPlace.setObjectName("combo_insertPlace")
        self.combo_insertPlace.setMinimumSize(QSize(0, 42))

        self.horizontalLayout_2.addWidget(self.combo_insertPlace)

        self.btn_insertUser = QPushButton(self.widget_3)
        self.btn_insertUser.setObjectName("btn_insertUser")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_insertUser.sizePolicy().hasHeightForWidth())
        self.btn_insertUser.setSizePolicy(sizePolicy4)
        self.btn_insertUser.setMinimumSize(QSize(64, 44))
        self.btn_insertUser.setMaximumSize(QSize(48, 16777215))

        self.horizontalLayout_2.addWidget(self.btn_insertUser)

        self.verticalLayout_3.addWidget(self.widget_3)

        self.verticalLayout.addWidget(self.widget)

        QWidget.setTabOrder(self.btn_removeUser, self.btn_insertUser)
        QWidget.setTabOrder(self.btn_insertUser, self.btn_duplicateUser)

        self.retranslateUi(UserTable)

        QMetaObject.connectSlotsByName(UserTable)

    # setupUi

    def retranslateUi(self, UserTable):
        UserTable.setWindowTitle(QCoreApplication.translate("UserTable", "Form", None))
        # if QT_CONFIG(tooltip)
        self.btn_saveClose.setToolTip(QCoreApplication.translate("UserTable", "Save changes made and close", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_saveClose.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_discardClose.setToolTip(QCoreApplication.translate("UserTable", "Discard changes made and close", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_discardClose.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_importList_2.setToolTip(QCoreApplication.translate("UserTable", "Import users from file", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_importList_2.setText(QCoreApplication.translate("UserTable", "Import", None))
        # if QT_CONFIG(tooltip)
        self.btn_exportList_2.setToolTip(QCoreApplication.translate("UserTable", "Export users to file", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_exportList_2.setText(QCoreApplication.translate("UserTable", "Export", None))
        # if QT_CONFIG(tooltip)
        self.btn_duplicateUser.setToolTip(QCoreApplication.translate("UserTable", "Duplicates selected users", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_duplicateUser.setText(QCoreApplication.translate("UserTable", "Duplicate", None))
        # if QT_CONFIG(tooltip)
        self.btn_removeUser.setToolTip(QCoreApplication.translate("UserTable", "Removes selected users", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_removeUser.setText(QCoreApplication.translate("UserTable", "Remove", None))
        # if QT_CONFIG(tooltip)
        self.btn_moveUp.setToolTip(QCoreApplication.translate("UserTable", "Move selected users up", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_moveUp.setText(QCoreApplication.translate("UserTable", "\u2191", None))
        # if QT_CONFIG(tooltip)
        self.btn_moveDown.setToolTip(QCoreApplication.translate("UserTable", "Move selected users down", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_moveDown.setText(QCoreApplication.translate("UserTable", "\u2193", None))
        self.combo_insertPlace.setItemText(0, QCoreApplication.translate("UserTable", "Top", None))
        self.combo_insertPlace.setItemText(1, QCoreApplication.translate("UserTable", "Middle", None))
        self.combo_insertPlace.setItemText(2, QCoreApplication.translate("UserTable", "Bottom", None))

        # if QT_CONFIG(tooltip)
        self.combo_insertPlace.setToolTip(QCoreApplication.translate("UserTable", "Position at which to insert the user", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.btn_insertUser.setToolTip(QCoreApplication.translate("UserTable", "Insert the user in the table", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_insertUser.setText(QCoreApplication.translate("UserTable", "Insert", None))

    # retranslateUi
