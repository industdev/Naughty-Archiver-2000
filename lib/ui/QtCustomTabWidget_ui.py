# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CustomTabWidgetDFJNnN.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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
    QAbstractScrollArea,
    QApplication,
    QFrame,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(696, 407)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout_6 = QHBoxLayout(self.widget)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.cfg_list = QListWidget(self.widget)
        self.cfg_list.setObjectName("cfg_list")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfg_list.sizePolicy().hasHeightForWidth())
        self.cfg_list.setSizePolicy(sizePolicy)
        self.cfg_list.setMinimumSize(QSize(128, 0))
        self.cfg_list.setFrameShape(QFrame.Shape.NoFrame)
        self.cfg_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cfg_list.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.cfg_list.setAutoScrollMargin(16)
        self.cfg_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cfg_list.setProperty("showDropIndicator", False)

        self.horizontalLayout_6.addWidget(self.cfg_list)

        self.btn_showHideList = QPushButton(self.widget)
        self.btn_showHideList.setObjectName("btn_showHideList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_showHideList.sizePolicy().hasHeightForWidth())
        self.btn_showHideList.setSizePolicy(sizePolicy1)
        self.btn_showHideList.setMaximumSize(QSize(24, 16777215))
        self.btn_showHideList.setChecked(False)
        self.btn_showHideList.setFlat(True)

        self.horizontalLayout_6.addWidget(self.btn_showHideList)

        self.line_3 = QFrame(self.widget)
        self.line_3.setObjectName("line_3")
        palette = QPalette()
        brush = QBrush(QColor(217, 217, 217, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        self.line_3.setPalette(palette)
        self.line_3.setFrameShadow(QFrame.Shadow.Plain)
        self.line_3.setLineWidth(0)
        self.line_3.setFrameShape(QFrame.Shape.VLine)

        self.horizontalLayout_6.addWidget(self.line_3)

        self.cfg_windows = QStackedWidget(self.widget)
        self.cfg_windows.setObjectName("cfg_windows")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.horizontalLayout_8 = QHBoxLayout(self.page)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.cfg_windows.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.cfg_windows.addWidget(self.page_2)

        self.horizontalLayout_6.addWidget(self.cfg_windows)

        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)

        self.cfg_windows.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.btn_showHideList.setText(QCoreApplication.translate("Form", "<", None))

    # retranslateUi
