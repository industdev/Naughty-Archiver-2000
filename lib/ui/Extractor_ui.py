# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExtractorUiLdDjwz.ui'
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
    QApplication,
    QCheckBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_Extractor(object):
    def setupUi(self, Extractor):
        if not Extractor.objectName():
            Extractor.setObjectName("Extractor")
        Extractor.resize(689, 464)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        Extractor.setPalette(palette)
        self.gridLayout_4 = QGridLayout(Extractor)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(4)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.line_2 = QFrame(Extractor)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.line_2, 1, 0, 1, 1)

        self.tabWidget = QTabWidget(Extractor)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMinimumSize(QSize(480, 300))
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.South)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideLeft)
        self.tabWidget.setDocumentMode(True)
        self.tab1 = QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout_3 = QGridLayout(self.tab1)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(8, 4, 8, 8)
        self.widget_2 = QWidget(self.tab1)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 0)
        self.grpbox_tabconsole = QGroupBox(self.widget_4)
        self.grpbox_tabconsole.setObjectName("grpbox_tabconsole")
        self.grpbox_tabconsole.setMinimumSize(QSize(0, 48))
        font = QFont()
        font.setBold(False)
        font.setStrikeOut(False)
        self.grpbox_tabconsole.setFont(font)
        self.grpbox_tabconsole.setMouseTracking(False)
        self.grpbox_tabconsole.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grpbox_tabconsole.setFlat(True)
        self.horizontalLayout_4 = QHBoxLayout(self.grpbox_tabconsole)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 0, 5, 5)
        self.cfgui_consoleshowWHITE = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowWHITE.setObjectName("cfgui_consoleshowWHITE")

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowWHITE)

        self.cfgui_consoleshowYELLOW = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowYELLOW.setObjectName("cfgui_consoleshowYELLOW")

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowYELLOW)

        self.cfgui_consoleshowRED = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowRED.setObjectName("cfgui_consoleshowRED")

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowRED)

        self.cfgui_consoleshowGREY = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowGREY.setObjectName("cfgui_consoleshowGREY")

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowGREY)

        self.cfgui_consoleshowOTHER = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowOTHER.setObjectName("cfgui_consoleshowOTHER")

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowOTHER)

        self.cfgui_consoleshowGREEN = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowGREEN.setObjectName("cfgui_consoleshowGREEN")
        self.cfgui_consoleshowGREEN.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowGREEN)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_3.addWidget(self.grpbox_tabconsole)

        self.verticalLayout_3.addWidget(self.widget_4)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(128, 0))
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_skipJob = QPushButton(self.widget_3)
        self.btn_skipJob.setObjectName("btn_skipJob")
        self.btn_skipJob.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btn_skipJob)

        self.btn_StopRun = QPushButton(self.widget_3)
        self.btn_StopRun.setObjectName("btn_StopRun")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_StopRun.sizePolicy().hasHeightForWidth())
        self.btn_StopRun.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.btn_StopRun)

        self.btn_customRun = QPushButton(self.widget_3)
        self.btn_customRun.setObjectName("btn_customRun")

        self.horizontalLayout.addWidget(self.btn_customRun)

        self.btn_showUsersTable = QPushButton(self.widget_3)
        self.btn_showUsersTable.setObjectName("btn_showUsersTable")

        self.horizontalLayout.addWidget(self.btn_showUsersTable)

        self.btn_showCookiesTable = QPushButton(self.widget_3)
        self.btn_showCookiesTable.setObjectName("btn_showCookiesTable")

        self.horizontalLayout.addWidget(self.btn_showCookiesTable)

        self.btn_showErrored = QPushButton(self.widget_3)
        self.btn_showErrored.setObjectName("btn_showErrored")

        self.horizontalLayout.addWidget(self.btn_showErrored)

        self.verticalLayout_3.addWidget(self.widget_3)

        self.verticalLayout.addWidget(self.widget_2)

        self.theLogPlace = QTextEdit(self.tab1)
        self.theLogPlace.setObjectName("theLogPlace")
        self.theLogPlace.setMinimumSize(QSize(256, 128))
        self.theLogPlace.setBaseSize(QSize(64, 64))
        palette1 = QPalette()
        brush1 = QBrush(QColor(204, 204, 204, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush1)
        brush2 = QBrush(QColor(12, 12, 12, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush2)
        brush3 = QBrush(QColor(255, 255, 255, 128))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush3)
        # endif
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush3)
        # endif
        brush4 = QBrush(QColor(120, 120, 120, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush4)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush3)
        # endif
        self.theLogPlace.setPalette(palette1)
        font1 = QFont()
        font1.setFamilies(["Courier New"])
        font1.setPointSize(8)
        font1.setStrikeOut(False)
        font1.setStyleStrategy(QFont.NoAntialias)
        self.theLogPlace.setFont(font1)
        self.theLogPlace.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.theLogPlace.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.theLogPlace.setReadOnly(True)

        self.verticalLayout.addWidget(self.theLogPlace)

        self.label_2 = QLabel(self.tab1)
        self.label_2.setObjectName("label_2")
        palette2 = QPalette()
        brush5 = QBrush(QColor(180, 180, 180, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush5)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush5)
        self.label_2.setPalette(palette2)

        self.verticalLayout.addWidget(self.label_2)

        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        self.tabWidget.addTab(self.tab1, icon, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout = QGridLayout(self.tab2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsTab = QVBoxLayout()
        self.settingsTab.setSpacing(0)
        self.settingsTab.setObjectName("settingsTab")
        self.settingsTab.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.tab2)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setFrameShadow(QFrame.Shadow.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 685, 356))
        self.horizontalLayout_2 = QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 7, 11, 0)
        self.grpbox_settings = QGroupBox(self.scrollAreaWidgetContents_2)
        self.grpbox_settings.setObjectName("grpbox_settings")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.grpbox_settings.sizePolicy().hasHeightForWidth())
        self.grpbox_settings.setSizePolicy(sizePolicy2)
        self.grpbox_settings.setMinimumSize(QSize(128, 128))
        palette3 = QPalette()
        brush6 = QBrush(QColor(0, 0, 0, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush6)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush6)
        brush7 = QBrush(QColor(144, 144, 144, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush7)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush6)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush6)
        brush8 = QBrush(QColor(50, 50, 50, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush8)
        brush9 = QBrush(QColor(30, 30, 30, 128))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush9)
        # endif
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush6)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush6)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush7)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush6)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush6)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush8)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush9)
        # endif
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush7)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush6)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush7)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush7)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush7)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush8)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush9)
        # endif
        self.grpbox_settings.setPalette(palette3)
        self.grpbox_settings.setTitle("Extractor Settings")
        self.grpbox_settings.setFlat(True)
        self.grpbox_settings.setCheckable(True)
        self.formLayout = QFormLayout(self.grpbox_settings)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.lbl_twitterdestination = QLabel(self.grpbox_settings)
        self.lbl_twitterdestination.setObjectName("lbl_twitterdestination")
        self.lbl_twitterdestination.setMinimumSize(QSize(128, 0))
        self.lbl_twitterdestination.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter
        )

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_twitterdestination)

        self.widget_5 = QWidget(self.grpbox_settings)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.cfgui_defaultpath = QLineEdit(self.widget_5)
        self.cfgui_defaultpath.setObjectName("cfgui_defaultpath")
        self.cfgui_defaultpath.setMaxLength(256)
        self.cfgui_defaultpath.setReadOnly(False)

        self.horizontalLayout_5.addWidget(self.cfgui_defaultpath)

        self.btn_pathselect = QPushButton(self.widget_5)
        self.btn_pathselect.setObjectName("btn_pathselect")
        self.btn_pathselect.setMinimumSize(QSize(0, 24))
        self.btn_pathselect.setMaximumSize(QSize(48, 16777215))

        self.horizontalLayout_5.addWidget(self.btn_pathselect)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.widget_5)

        self.lbl_sleep = QLabel(self.grpbox_settings)
        self.lbl_sleep.setObjectName("lbl_sleep")
        self.lbl_sleep.setMinimumSize(QSize(128, 0))
        self.lbl_sleep.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_sleep)

        self.cfgui_sleeptime = QLineEdit(self.grpbox_settings)
        self.cfgui_sleeptime.setObjectName("cfgui_sleeptime")
        self.cfgui_sleeptime.setReadOnly(False)
        self.cfgui_sleeptime.setClearButtonEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfgui_sleeptime)

        self.horizontalLayout_2.addWidget(self.grpbox_settings)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.settingsTab.addWidget(self.scrollArea)

        self.line = QFrame(self.tab2)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.settingsTab.addWidget(self.line)

        self.widget_6 = QWidget(self.tab2)
        self.widget_6.setObjectName("widget_6")
        self.widget_6.setMinimumSize(QSize(0, 8))
        self._2 = QHBoxLayout(self.widget_6)
        self._2.setObjectName("_2")
        self._2.setContentsMargins(-1, 2, 2, 4)
        self.label = QLabel(self.widget_6)
        self.label.setObjectName("label")
        palette4 = QPalette()
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush5)
        brush10 = QBrush(QColor(143, 143, 143, 255))
        brush10.setStyle(Qt.BrushStyle.SolidPattern)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush10)
        brush11 = QBrush(QColor(143, 143, 143, 128))
        brush11.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush11)
        # endif
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush5)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush10)
        brush12 = QBrush(QColor(143, 143, 143, 128))
        brush12.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush12)
        # endif
        brush13 = QBrush(QColor(127, 127, 127, 255))
        brush13.setStyle(Qt.BrushStyle.SolidPattern)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush13)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush13)
        brush14 = QBrush(QColor(143, 143, 143, 128))
        brush14.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush14)
        # endif
        self.label.setPalette(palette4)

        self._2.addWidget(self.label)

        self.btn_copyLastCursor = QPushButton(self.widget_6)
        self.btn_copyLastCursor.setObjectName("btn_copyLastCursor")
        self.btn_copyLastCursor.setMaximumSize(QSize(128, 16777215))

        self._2.addWidget(self.btn_copyLastCursor)

        self.btn_deleteExtractor = QPushButton(self.widget_6)
        self.btn_deleteExtractor.setObjectName("btn_deleteExtractor")
        self.btn_deleteExtractor.setMinimumSize(QSize(128, 0))
        self.btn_deleteExtractor.setMaximumSize(QSize(128, 16777215))

        self._2.addWidget(self.btn_deleteExtractor)

        self.settingsTab.addWidget(self.widget_6)

        self.gridLayout.addLayout(self.settingsTab, 0, 0, 1, 1)

        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.tabWidget.addTab(self.tab2, icon1, "")

        self.gridLayout_4.addWidget(self.tabWidget, 3, 0, 1, 1)

        self.labelContainer = QWidget(Extractor)
        self.labelContainer.setObjectName("labelContainer")
        palette5 = QPalette()
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, brush6)
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, brush6)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, brush6)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush6)
        self.labelContainer.setPalette(palette5)
        self.horizontalLayout_6 = QHBoxLayout(self.labelContainer)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 4, 0, 4)
        self.scrollingLabel = QLabel(self.labelContainer)
        self.scrollingLabel.setObjectName("scrollingLabel")
        sizePolicy2.setHeightForWidth(self.scrollingLabel.sizePolicy().hasHeightForWidth())
        self.scrollingLabel.setSizePolicy(sizePolicy2)
        self.scrollingLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollingLabel.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollingLabel.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.scrollingLabel)

        self.gridLayout_4.addWidget(self.labelContainer, 0, 0, 1, 1)

        self.retranslateUi(Extractor)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Extractor)

    # setupUi

    def retranslateUi(self, Extractor):
        Extractor.setWindowTitle(QCoreApplication.translate("Extractor", "Form", None))
        self.grpbox_tabconsole.setTitle(QCoreApplication.translate("Extractor", "Console Settings", None))
        self.cfgui_consoleshowWHITE.setText(QCoreApplication.translate("Extractor", "Infos", None))
        self.cfgui_consoleshowYELLOW.setText(QCoreApplication.translate("Extractor", "Alerts", None))
        self.cfgui_consoleshowRED.setText(QCoreApplication.translate("Extractor", "Errors", None))
        self.cfgui_consoleshowGREY.setText(QCoreApplication.translate("Extractor", "Debug", None))
        self.cfgui_consoleshowOTHER.setText(QCoreApplication.translate("Extractor", "Api", None))
        self.cfgui_consoleshowGREEN.setText(QCoreApplication.translate("Extractor", "Files", None))
        self.btn_skipJob.setText(QCoreApplication.translate("Extractor", "Skip", None))
        self.btn_StopRun.setText(QCoreApplication.translate("Extractor", "Run", None))
        self.btn_customRun.setText(QCoreApplication.translate("Extractor", "Custom run", None))
        self.btn_showUsersTable.setText(QCoreApplication.translate("Extractor", "Users", None))
        self.btn_showCookiesTable.setText(QCoreApplication.translate("Extractor", "Cookies", None))
        self.btn_showErrored.setText(QCoreApplication.translate("Extractor", "Errored", None))
        self.theLogPlace.setDocumentTitle("")
        self.theLogPlace.setPlaceholderText(QCoreApplication.translate("Extractor", "Extractor's logs will be shown here", None))
        self.label_2.setText(QCoreApplication.translate("Extractor", "Current selected cookies: None", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("Extractor", "Console", None))
        self.lbl_twitterdestination.setText(QCoreApplication.translate("Extractor", "Default destination", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_defaultpath.setToolTip(
            QCoreApplication.translate(
                "Extractor",
                "<html><head/><body><p>The extraction path of users with text 'default' as destination will go in (folder is named with the username). </p><p>Useful for archiving many accounts to the same folder</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_defaultpath.setText("")
        self.cfgui_defaultpath.setPlaceholderText(QCoreApplication.translate("Extractor", "Absolute Path", None))
        self.btn_pathselect.setText(QCoreApplication.translate("Extractor", "...", None))
        self.lbl_sleep.setText(QCoreApplication.translate("Extractor", "Sleep", None))
        self.cfgui_sleeptime.setText("")
        self.cfgui_sleeptime.setPlaceholderText(QCoreApplication.translate("Extractor", "Integer (Seconds)", None))
        self.label.setText(QCoreApplication.translate("Extractor", "Settings are applied on extractor restart", None))
        self.btn_copyLastCursor.setText(QCoreApplication.translate("Extractor", "Copy last cursor", None))
        self.btn_deleteExtractor.setText(QCoreApplication.translate("Extractor", "Delete extractor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QCoreApplication.translate("Extractor", "Settings", None))
        self.scrollingLabel.setText(QCoreApplication.translate("Extractor", "Extractor", None))

    # retranslateUi
