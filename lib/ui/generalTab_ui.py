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


class Ui_TabGeneral(object):
    def setupUi(self, TabGeneral):
        if not TabGeneral.objectName():
            TabGeneral.setObjectName("TabGeneral")
        TabGeneral.resize(599, 619)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        TabGeneral.setPalette(palette)
        self.gridLayout_4 = QGridLayout(TabGeneral)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(TabGeneral)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMinimumSize(QSize(480, 300))
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.South)
        self.tabWidget.setIconSize(QSize(64, 16))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.tab1 = QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout_3 = QGridLayout(self.tab1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(8, 8, 8, 9)
        self.widget_2 = QWidget(self.tab1)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(128, 0))
        self.verticalLayout = QVBoxLayout(self.widget_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_StopRun = QPushButton(self.widget_3)
        self.btn_StopRun.setObjectName("btn_StopRun")
        self.btn_StopRun.setMinimumSize(QSize(0, 48))

        self.verticalLayout.addWidget(self.btn_StopRun)

        self.horizontalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 4, 0)
        self.grpbox_tabconsole = QGroupBox(self.widget_4)
        self.grpbox_tabconsole.setObjectName("grpbox_tabconsole")
        self.grpbox_tabconsole.setMinimumSize(QSize(0, 48))
        palette1 = QPalette()
        brush1 = QBrush(QColor(144, 144, 144, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush1)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush2)
        brush3 = QBrush(QColor(0, 0, 0, 128))
        brush3.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush3)
        # endif
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush2)
        brush4 = QBrush(QColor(0, 0, 0, 128))
        brush4.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush4)
        # endif
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush5)
        # endif
        self.grpbox_tabconsole.setPalette(palette1)
        font = QFont()
        font.setBold(False)
        font.setStrikeOut(False)
        self.grpbox_tabconsole.setFont(font)
        self.grpbox_tabconsole.setMouseTracking(False)
        self.grpbox_tabconsole.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.grpbox_tabconsole.setFlat(True)
        self.grpbox_tabconsole.setCheckable(False)
        self.horizontalLayout_4 = QHBoxLayout(self.grpbox_tabconsole)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 0, 0, 0)
        self.cfgui_consoleshowWHITE = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowWHITE.setObjectName("cfgui_consoleshowWHITE")
        palette2 = QPalette()
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        brush6 = QBrush(QColor(127, 127, 127, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        self.cfgui_consoleshowWHITE.setPalette(palette2)

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowWHITE)

        self.cfgui_consoleshowYELLOW = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowYELLOW.setObjectName("cfgui_consoleshowYELLOW")
        palette3 = QPalette()
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        self.cfgui_consoleshowYELLOW.setPalette(palette3)

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowYELLOW)

        self.cfgui_consoleshowRED = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowRED.setObjectName("cfgui_consoleshowRED")
        palette4 = QPalette()
        palette4.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette4.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        self.cfgui_consoleshowRED.setPalette(palette4)

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowRED)

        self.cfgui_consoleshowGREY = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowGREY.setObjectName("cfgui_consoleshowGREY")
        palette5 = QPalette()
        palette5.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette5.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette5.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        self.cfgui_consoleshowGREY.setPalette(palette5)

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowGREY)

        self.cfgui_consoleshowOTHER = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowOTHER.setObjectName("cfgui_consoleshowOTHER")
        palette6 = QPalette()
        palette6.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette6.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette6.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        self.cfgui_consoleshowOTHER.setPalette(palette6)

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowOTHER)

        self.cfgui_consoleshowGREEN = QCheckBox(self.grpbox_tabconsole)
        self.cfgui_consoleshowGREEN.setObjectName("cfgui_consoleshowGREEN")
        self.cfgui_consoleshowGREEN.setMaximumSize(QSize(0, 0))
        palette7 = QPalette()
        palette7.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette7.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette7.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush6)
        self.cfgui_consoleshowGREEN.setPalette(palette7)

        self.horizontalLayout_4.addWidget(self.cfgui_consoleshowGREEN)

        self.horizontalLayout_3.addWidget(self.grpbox_tabconsole)

        self.horizontalLayout.addWidget(self.widget_4)

        self.gridLayout_2.addWidget(self.widget_2, 0, 0, 1, 1)

        self.theLogPlace = QTextEdit(self.tab1)
        self.theLogPlace.setObjectName("theLogPlace")
        self.theLogPlace.setMinimumSize(QSize(256, 128))
        self.theLogPlace.setBaseSize(QSize(64, 64))
        palette8 = QPalette()
        brush7 = QBrush(QColor(204, 204, 204, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette8.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush7)
        brush8 = QBrush(QColor(12, 12, 12, 255))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
        palette8.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush8)
        brush9 = QBrush(QColor(255, 255, 255, 128))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush9)
        # endif
        palette8.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush7)
        palette8.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush8)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush9)
        # endif
        brush10 = QBrush(QColor(120, 120, 120, 255))
        brush10.setStyle(Qt.BrushStyle.SolidPattern)
        palette8.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush10)
        palette8.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush9)
        # endif
        self.theLogPlace.setPalette(palette8)
        font1 = QFont()
        font1.setFamilies(["Courier New"])
        font1.setPointSize(8)
        font1.setStrikeOut(False)
        font1.setStyleStrategy(QFont.NoAntialias)
        self.theLogPlace.setFont(font1)
        self.theLogPlace.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.theLogPlace.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.theLogPlace.setReadOnly(True)

        self.gridLayout_2.addWidget(self.theLogPlace, 1, 0, 1, 1)

        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        self.tabWidget.addTab(self.tab1, icon, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout = QGridLayout(self.tab2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutLeft = QVBoxLayout()
        self.verticalLayoutLeft.setSpacing(0)
        self.verticalLayoutLeft.setObjectName("verticalLayoutLeft")
        self.verticalLayoutLeft.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.tab2)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setFrameShadow(QFrame.Shadow.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.settings = QWidget()
        self.settings.setObjectName("settings")
        self.settings.setGeometry(QRect(0, 0, 583, 656))
        self.verticalLayout_3 = QVBoxLayout(self.settings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 6, 12, -1)
        self.grpbox_settings_5 = QGroupBox(self.settings)
        self.grpbox_settings_5.setObjectName("grpbox_settings_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.grpbox_settings_5.sizePolicy().hasHeightForWidth())
        self.grpbox_settings_5.setSizePolicy(sizePolicy1)
        palette9 = QPalette()
        palette9.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette9.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush1)
        brush11 = QBrush(QColor(206, 206, 206, 255))
        brush11.setStyle(Qt.BrushStyle.SolidPattern)
        palette9.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush11)
        palette9.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush2)
        brush12 = QBrush(QColor(206, 206, 206, 128))
        brush12.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush12)
        # endif
        palette9.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        palette9.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush1)
        palette9.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush11)
        palette9.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush2)
        brush13 = QBrush(QColor(206, 206, 206, 128))
        brush13.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush13)
        # endif
        palette9.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette9.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush1)
        palette9.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette9.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        brush14 = QBrush(QColor(206, 206, 206, 128))
        brush14.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush14)
        # endif
        self.grpbox_settings_5.setPalette(palette9)
        self.grpbox_settings_5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.grpbox_settings_5.setTitle("Tools")
        self.grpbox_settings_5.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.grpbox_settings_5.setFlat(True)
        self.formLayout_2 = QFormLayout(self.grpbox_settings_5)
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout_2.setContentsMargins(-1, 6, 6, 6)
        self.lbl_looptime_3 = QLabel(self.grpbox_settings_5)
        self.lbl_looptime_3.setObjectName("lbl_looptime_3")
        self.lbl_looptime_3.setMinimumSize(QSize(100, 0))
        palette10 = QPalette()
        palette10.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette10.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette10.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_looptime_3.setPalette(palette10)
        self.lbl_looptime_3.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_looptime_3)

        self.widget = QWidget(self.grpbox_settings_5)
        self.widget.setObjectName("widget")
        self.widget.setMaximumSize(QSize(16777215, 32))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, 0, 0, 0)
        self.comboBox = QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setMaximumSize(QSize(128, 16777215))
        palette11 = QPalette()
        palette11.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        palette11.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        self.comboBox.setPalette(palette11)

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.btn_insert = QPushButton(self.widget)
        self.btn_insert.setObjectName("btn_insert")

        self.horizontalLayout_2.addWidget(self.btn_insert)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.widget)

        self.btn_downloadTools = QPushButton(self.grpbox_settings_5)
        self.btn_downloadTools.setObjectName("btn_downloadTools")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.btn_downloadTools)

        self.btn_showUnixCreator = QPushButton(self.grpbox_settings_5)
        self.btn_showUnixCreator.setObjectName("btn_showUnixCreator")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.btn_showUnixCreator)

        self.btn_showOutputHandlerCreator = QPushButton(self.grpbox_settings_5)
        self.btn_showOutputHandlerCreator.setObjectName("btn_showOutputHandlerCreator")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.btn_showOutputHandlerCreator)

        self.verticalLayout_3.addWidget(self.grpbox_settings_5)

        self.groupBox = QGroupBox(self.settings)
        self.groupBox.setObjectName("groupBox")
        palette12 = QPalette()
        palette12.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette12.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        self.groupBox.setPalette(palette12)
        self.groupBox.setFlat(True)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 4, 6, -1)
        self.widget_6 = QWidget(self.groupBox)
        self.widget_6.setObjectName("widget_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy2)
        self.formLayout_3 = QFormLayout(self.widget_6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout_3.setContentsMargins(0, 6, 0, 6)
        self.lbl_looptime = QLabel(self.widget_6)
        self.lbl_looptime.setObjectName("lbl_looptime")
        self.lbl_looptime.setMinimumSize(QSize(100, 0))
        palette13 = QPalette()
        palette13.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette13.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette13.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_looptime.setPalette(palette13)
        self.lbl_looptime.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_looptime)

        self.cfgui_looptime = QLineEdit(self.widget_6)
        self.cfgui_looptime.setObjectName("cfgui_looptime")
        palette14 = QPalette()
        palette14.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        brush15 = QBrush(QColor(0, 0, 0, 128))
        brush15.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette14.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette14.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette14.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette14.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        brush16 = QBrush(QColor(206, 206, 206, 128))
        brush16.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette14.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_looptime.setPalette(palette14)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfgui_looptime)

        self.lbl_maximumruns = QLabel(self.widget_6)
        self.lbl_maximumruns.setObjectName("lbl_maximumruns")
        self.lbl_maximumruns.setMinimumSize(QSize(100, 0))
        palette15 = QPalette()
        palette15.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette15.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette15.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_maximumruns.setPalette(palette15)
        self.lbl_maximumruns.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_maximumruns)

        self.cfgui_maximumruns = QLineEdit(self.widget_6)
        self.cfgui_maximumruns.setObjectName("cfgui_maximumruns")
        palette16 = QPalette()
        palette16.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette16.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette16.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette16.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette16.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette16.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_maximumruns.setPalette(palette16)
        self.cfgui_maximumruns.setReadOnly(False)
        self.cfgui_maximumruns.setClearButtonEnabled(False)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfgui_maximumruns)

        self.label = QLabel(self.widget_6)
        self.label.setObjectName("label")
        self.label.setMinimumSize(QSize(100, 0))
        palette17 = QPalette()
        palette17.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette17.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        self.label.setPalette(palette17)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)

        self.cfgui_errortrigger = QLineEdit(self.widget_6)
        self.cfgui_errortrigger.setObjectName("cfgui_errortrigger")
        palette18 = QPalette()
        palette18.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette18.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette18.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette18.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette18.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette18.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_errortrigger.setPalette(palette18)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfgui_errortrigger)

        self.verticalLayout_2.addWidget(self.widget_6)

        self.widget_5 = QWidget(self.groupBox)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_5 = QGridLayout(self.widget_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.cfgui_exitcode = QCheckBox(self.widget_5)
        self.cfgui_exitcode.setObjectName("cfgui_exitcode")
        palette19 = QPalette()
        palette19.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette19.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette19.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.cfgui_exitcode.setPalette(palette19)

        self.gridLayout_5.addWidget(self.cfgui_exitcode, 1, 1, 1, 1)

        self.cfgui_errorboxes = QCheckBox(self.widget_5)
        self.cfgui_errorboxes.setObjectName("cfgui_errorboxes")
        palette20 = QPalette()
        palette20.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette20.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette20.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.cfgui_errorboxes.setPalette(palette20)

        self.gridLayout_5.addWidget(self.cfgui_errorboxes, 3, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(105, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.cfgui_nocursorupdate = QCheckBox(self.widget_5)
        self.cfgui_nocursorupdate.setObjectName("cfgui_nocursorupdate")
        palette21 = QPalette()
        palette21.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette21.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        self.cfgui_nocursorupdate.setPalette(palette21)

        self.gridLayout_5.addWidget(self.cfgui_nocursorupdate, 2, 2, 1, 1)

        self.cfgui_nostatsupdate = QCheckBox(self.widget_5)
        self.cfgui_nostatsupdate.setObjectName("cfgui_nostatsupdate")
        palette22 = QPalette()
        palette22.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette22.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette22.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.cfgui_nostatsupdate.setPalette(palette22)

        self.gridLayout_5.addWidget(self.cfgui_nostatsupdate, 3, 2, 1, 1)

        self.cfgui_randomizelist = QCheckBox(self.widget_5)
        self.cfgui_randomizelist.setObjectName("cfgui_randomizelist")
        palette23 = QPalette()
        palette23.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette23.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        self.cfgui_randomizelist.setPalette(palette23)

        self.gridLayout_5.addWidget(self.cfgui_randomizelist, 2, 1, 1, 1)

        self.cfgui_nounixupdate = QCheckBox(self.widget_5)
        self.cfgui_nounixupdate.setObjectName("cfgui_nounixupdate")
        palette24 = QPalette()
        palette24.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette24.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette24.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.cfgui_nounixupdate.setPalette(palette24)

        self.gridLayout_5.addWidget(self.cfgui_nounixupdate, 1, 2, 1, 1)

        self.verticalLayout_2.addWidget(self.widget_5)

        self.verticalLayout_3.addWidget(self.groupBox)

        self.grpbox_settings_2 = QGroupBox(self.settings)
        self.grpbox_settings_2.setObjectName("grpbox_settings_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.grpbox_settings_2.sizePolicy().hasHeightForWidth())
        self.grpbox_settings_2.setSizePolicy(sizePolicy3)
        palette25 = QPalette()
        palette25.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette25.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush1)
        palette25.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush11)
        palette25.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush2)
        brush17 = QBrush(QColor(206, 206, 206, 128))
        brush17.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette25.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush17)
        # endif
        palette25.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        palette25.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush1)
        palette25.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush11)
        palette25.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush2)
        brush18 = QBrush(QColor(206, 206, 206, 128))
        brush18.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette25.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush18)
        # endif
        palette25.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette25.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush1)
        palette25.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette25.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        brush19 = QBrush(QColor(206, 206, 206, 128))
        brush19.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette25.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush19)
        # endif
        self.grpbox_settings_2.setPalette(palette25)
        self.grpbox_settings_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.grpbox_settings_2.setTitle("General Settings")
        self.grpbox_settings_2.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.grpbox_settings_2.setFlat(True)
        self.formLayout_4 = QFormLayout(self.grpbox_settings_2)
        self.formLayout_4.setObjectName("formLayout_4")
        self.formLayout_4.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_4.setContentsMargins(-1, -1, 6, -1)
        self.lbl_maximumruns_3 = QLabel(self.grpbox_settings_2)
        self.lbl_maximumruns_3.setObjectName("lbl_maximumruns_3")
        self.lbl_maximumruns_3.setMinimumSize(QSize(100, 0))
        palette26 = QPalette()
        palette26.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette26.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette26.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_maximumruns_3.setPalette(palette26)
        self.lbl_maximumruns_3.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_maximumruns_3)

        self.cfgui_maxlogsize = QLineEdit(self.grpbox_settings_2)
        self.cfgui_maxlogsize.setObjectName("cfgui_maxlogsize")
        palette27 = QPalette()
        palette27.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette27.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette27.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette27.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette27.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette27.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_maxlogsize.setPalette(palette27)
        self.cfgui_maxlogsize.setReadOnly(False)
        self.cfgui_maxlogsize.setClearButtonEnabled(False)

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfgui_maxlogsize)

        self.cfgui_maxlogentries = QLineEdit(self.grpbox_settings_2)
        self.cfgui_maxlogentries.setObjectName("cfgui_maxlogentries")
        palette28 = QPalette()
        palette28.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette28.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette28.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette28.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette28.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette28.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_maxlogentries.setPalette(palette28)
        self.cfgui_maxlogentries.setReadOnly(False)
        self.cfgui_maxlogentries.setClearButtonEnabled(False)

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfgui_maxlogentries)

        self.cfgui_showontaskbar = QCheckBox(self.grpbox_settings_2)
        self.cfgui_showontaskbar.setObjectName("cfgui_showontaskbar")
        palette29 = QPalette()
        palette29.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette29.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette29.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.cfgui_showontaskbar.setPalette(palette29)

        self.formLayout_4.setWidget(4, QFormLayout.ItemRole.FieldRole, self.cfgui_showontaskbar)

        self.cfgui_autotester = QCheckBox(self.grpbox_settings_2)
        self.cfgui_autotester.setObjectName("cfgui_autotester")
        palette30 = QPalette()
        palette30.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette30.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        palette30.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette30.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        self.cfgui_autotester.setPalette(palette30)

        self.formLayout_4.setWidget(5, QFormLayout.ItemRole.FieldRole, self.cfgui_autotester)

        self.cfgui_skiploadingbars = QCheckBox(self.grpbox_settings_2)
        self.cfgui_skiploadingbars.setObjectName("cfgui_skiploadingbars")
        palette31 = QPalette()
        palette31.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette31.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        self.cfgui_skiploadingbars.setPalette(palette31)

        self.formLayout_4.setWidget(6, QFormLayout.ItemRole.FieldRole, self.cfgui_skiploadingbars)

        self.lbl_maxlogentries = QLabel(self.grpbox_settings_2)
        self.lbl_maxlogentries.setObjectName("lbl_maxlogentries")
        self.lbl_maxlogentries.setMinimumSize(QSize(100, 0))
        palette32 = QPalette()
        palette32.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette32.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette32.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_maxlogentries.setPalette(palette32)
        self.lbl_maxlogentries.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_maxlogentries)

        self.verticalLayout_3.addWidget(self.grpbox_settings_2)

        self.grpbox_settings_3 = QGroupBox(self.settings)
        self.grpbox_settings_3.setObjectName("grpbox_settings_3")
        sizePolicy3.setHeightForWidth(self.grpbox_settings_3.sizePolicy().hasHeightForWidth())
        self.grpbox_settings_3.setSizePolicy(sizePolicy3)
        palette33 = QPalette()
        palette33.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush1)
        palette33.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush1)
        palette33.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush11)
        palette33.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush2)
        brush20 = QBrush(QColor(206, 206, 206, 128))
        brush20.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette33.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush20)
        # endif
        palette33.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush1)
        palette33.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush1)
        palette33.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush11)
        palette33.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush2)
        brush21 = QBrush(QColor(206, 206, 206, 128))
        brush21.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette33.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush21)
        # endif
        palette33.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        palette33.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush1)
        palette33.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        palette33.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        brush22 = QBrush(QColor(206, 206, 206, 128))
        brush22.setStyle(Qt.BrushStyle.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette33.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush22)
        # endif
        self.grpbox_settings_3.setPalette(palette33)
        self.grpbox_settings_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.grpbox_settings_3.setTitle("Gallery-dl Settings")
        self.grpbox_settings_3.setFlat(True)
        self.formLayout = QFormLayout(self.grpbox_settings_3)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.lbl_maximumruns_2 = QLabel(self.grpbox_settings_3)
        self.lbl_maximumruns_2.setObjectName("lbl_maximumruns_2")
        self.lbl_maximumruns_2.setMinimumSize(QSize(100, 0))
        palette34 = QPalette()
        palette34.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette34.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette34.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_maximumruns_2.setPalette(palette34)
        self.lbl_maximumruns_2.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_maximumruns_2)

        self.cfgui_maxdlspeed = QLineEdit(self.grpbox_settings_3)
        self.cfgui_maxdlspeed.setObjectName("cfgui_maxdlspeed")
        palette35 = QPalette()
        palette35.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette35.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette35.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette35.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette35.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette35.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_maxdlspeed.setPalette(palette35)
        self.cfgui_maxdlspeed.setReadOnly(False)
        self.cfgui_maxdlspeed.setClearButtonEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfgui_maxdlspeed)

        self.lbl_sleepModulate = QLabel(self.grpbox_settings_3)
        self.lbl_sleepModulate.setObjectName("lbl_sleepModulate")
        self.lbl_sleepModulate.setMinimumSize(QSize(100, 0))
        palette36 = QPalette()
        palette36.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette36.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        palette36.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush1)
        self.lbl_sleepModulate.setPalette(palette36)
        self.lbl_sleepModulate.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_sleepModulate)

        self.cfgui_sleepmodulate = QLineEdit(self.grpbox_settings_3)
        self.cfgui_sleepmodulate.setObjectName("cfgui_sleepmodulate")
        palette37 = QPalette()
        palette37.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette37.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette37.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush2)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette37.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush15)
        # endif
        palette37.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette37.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush16)
        # endif
        self.cfgui_sleepmodulate.setPalette(palette37)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfgui_sleepmodulate)

        self.cfgui_extendedmetadata = QCheckBox(self.grpbox_settings_3)
        self.cfgui_extendedmetadata.setObjectName("cfgui_extendedmetadata")
        palette38 = QPalette()
        palette38.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush2)
        palette38.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush2)
        self.cfgui_extendedmetadata.setPalette(palette38)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfgui_extendedmetadata)

        self.verticalLayout_3.addWidget(self.grpbox_settings_3)

        self.scrollArea.setWidget(self.settings)

        self.verticalLayoutLeft.addWidget(self.scrollArea)

        self.gridLayout.addLayout(self.verticalLayoutLeft, 0, 0, 1, 1)

        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.tabWidget.addTab(self.tab2, icon1, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(TabGeneral)

        self.tabWidget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(TabGeneral)

    # setupUi

    def retranslateUi(self, TabGeneral):
        TabGeneral.setWindowTitle(QCoreApplication.translate("TabGeneral", "Form", None))
        self.btn_StopRun.setText(QCoreApplication.translate("TabGeneral", "Run All", None))
        self.grpbox_tabconsole.setTitle(QCoreApplication.translate("TabGeneral", "Console Settings", None))
        self.cfgui_consoleshowWHITE.setText(QCoreApplication.translate("TabGeneral", "Infos", None))
        self.cfgui_consoleshowYELLOW.setText(QCoreApplication.translate("TabGeneral", "Alerts", None))
        self.cfgui_consoleshowRED.setText(QCoreApplication.translate("TabGeneral", "Errors", None))
        self.cfgui_consoleshowGREY.setText(QCoreApplication.translate("TabGeneral", "Debug", None))
        self.cfgui_consoleshowOTHER.setText(QCoreApplication.translate("TabGeneral", "Options", None))
        self.cfgui_consoleshowGREEN.setText(QCoreApplication.translate("TabGeneral", "Files", None))
        self.theLogPlace.setDocumentTitle("")
        self.theLogPlace.setPlaceholderText(QCoreApplication.translate("TabGeneral", "General logs will be shown here", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("TabGeneral", "Console", None))
        # if QT_CONFIG(tooltip)
        self.lbl_looptime_3.setToolTip(
            QCoreApplication.translate(
                "TabGeneral", "Time to wait after restarting the whole extraction \n(So after going through all users)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_looptime_3.setText(QCoreApplication.translate("TabGeneral", "Extractor type", None))
        self.btn_insert.setText(QCoreApplication.translate("TabGeneral", "Insert", None))
        # if QT_CONFIG(tooltip)
        self.btn_downloadTools.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "<html><head/><body><p>Download Gallery-dl, ffmpeg and mkvtoolnix</p><p>You can also download them manually and put them in the /external folder as:</p><p>/gallery-dl.exe</p><p>/ffmpeg.exe</p><p>/mkvmerge.exe</p><p>All around it should be 170MB</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_downloadTools.setText(QCoreApplication.translate("TabGeneral", "Download tools", None))
        self.btn_showUnixCreator.setText(QCoreApplication.translate("TabGeneral", "UNIX timestamp creator", None))
        self.btn_showOutputHandlerCreator.setText(QCoreApplication.translate("TabGeneral", "Output handling manager", None))
        self.groupBox.setTitle(QCoreApplication.translate("TabGeneral", "Extraction Settings", None))
        # if QT_CONFIG(tooltip)
        self.lbl_looptime.setToolTip(
            QCoreApplication.translate(
                "TabGeneral", "Time to wait after restarting the whole extraction \n(So after going through all users)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_looptime.setText(QCoreApplication.translate("TabGeneral", "Loop pause", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_looptime.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "<html><head/><body><p>Time to wait before restarting the whole extraction after going through all users</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_looptime.setText("")
        self.cfgui_looptime.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer (Seconds)", None))
        # if QT_CONFIG(tooltip)
        self.lbl_maximumruns.setToolTip(
            QCoreApplication.translate("TabGeneral", "Maximum amount of restarts after each whole extraction", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_maximumruns.setText(QCoreApplication.translate("TabGeneral", "Maximum runs", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_maximumruns.setToolTip(
            QCoreApplication.translate("TabGeneral", "Maximum amount of restarts after each whole extraction", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_maximumruns.setText("")
        self.cfgui_maximumruns.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer", None))
        self.label.setText(QCoreApplication.translate("TabGeneral", "Error trigger", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_errortrigger.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "<html><head/><body><p>How much an extractor can error a minute before it's stopped, if set to 20 then an extractor that errors 20 times a minute will be stopped</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_errortrigger.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer (Errors per minute)", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_exitcode.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "If the gallery-dl process randomly decides to shut down, this will automatically repeat the job, otherwise skip to the next user",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_exitcode.setText(QCoreApplication.translate("TabGeneral", "Restart on exit code 1", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_errorboxes.setToolTip(
            QCoreApplication.translate("TabGeneral", "Pop up error or warning boxes to alert you of problems", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_errorboxes.setText(QCoreApplication.translate("TabGeneral", "Error boxes pop-up", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_nocursorupdate.setToolTip(
            QCoreApplication.translate("TabGeneral", "Don't update the user cursor when a new one is seen", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_nocursorupdate.setText(QCoreApplication.translate("TabGeneral", "No Cursor update", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_nostatsupdate.setToolTip(QCoreApplication.translate("TabGeneral", "Don't update stats", None))
        # endif // QT_CONFIG(tooltip)
        self.cfgui_nostatsupdate.setText(QCoreApplication.translate("TabGeneral", "No Stats update", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_randomizelist.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "Randomize the user list before pressing the run button so that all users get a chance of getting extracted",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_randomizelist.setText(QCoreApplication.translate("TabGeneral", "Randomize user list on extraction", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_nounixupdate.setToolTip(
            QCoreApplication.translate("TabGeneral", "Don't update user UNIX timestamp when it's extraction is finished", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_nounixupdate.setText(QCoreApplication.translate("TabGeneral", "No Unix update", None))
        # if QT_CONFIG(tooltip)
        self.lbl_maximumruns_3.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "Max log size in saved/logs/*.txt\n\nThe logs will be gracefully sent to the bin after closing the program",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_maximumruns_3.setText(QCoreApplication.translate("TabGeneral", "Max logs size", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_maxlogsize.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "<html><head/><body><p>Max log size in MB in saved/logs/*.txt</p><p>The logs will be gracefully sent to the bin after closing the program</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_maxlogsize.setText("")
        self.cfgui_maxlogsize.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer (Megabytes)", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_maxlogentries.setToolTip(
            QCoreApplication.translate("TabGeneral", "Max rows to display at a time in the consoles\nThis does not affect saved logs", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_maxlogentries.setText("")
        self.cfgui_maxlogentries.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer (Entries)", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_showontaskbar.setToolTip(
            QCoreApplication.translate("TabGeneral", "Show on taskbar when minimized, otherwise in the tray", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_showontaskbar.setText(QCoreApplication.translate("TabGeneral", "Show on taskbar when minimized", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_autotester.setToolTip(QCoreApplication.translate("TabGeneral", "Test if the extractors are valid automatically", None))
        # endif // QT_CONFIG(tooltip)
        self.cfgui_autotester.setText(QCoreApplication.translate("TabGeneral", "Validate extractors on launch", None))
        self.cfgui_skiploadingbars.setText(QCoreApplication.translate("TabGeneral", "No Loading bars pop-up", None))
        # if QT_CONFIG(tooltip)
        self.lbl_maxlogentries.setToolTip(
            QCoreApplication.translate(
                "TabGeneral", "Max rows to display at a time in the consoles\n\nThis does not affect saved logs", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lbl_maxlogentries.setText(QCoreApplication.translate("TabGeneral", "Log display limit", None))
        # if QT_CONFIG(tooltip)
        self.lbl_maximumruns_2.setToolTip(QCoreApplication.translate("TabGeneral", "Max download speed", None))
        # endif // QT_CONFIG(tooltip)
        self.lbl_maximumruns_2.setText(QCoreApplication.translate("TabGeneral", "Max DL speed", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_maxdlspeed.setToolTip(QCoreApplication.translate("TabGeneral", "Max download speed in kb/s", None))
        # endif // QT_CONFIG(tooltip)
        self.cfgui_maxdlspeed.setText("")
        self.cfgui_maxdlspeed.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer (Kb/s)", None))
        self.lbl_sleepModulate.setText(QCoreApplication.translate("TabGeneral", "Modulate Sleep", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_sleepmodulate.setToolTip(
            QCoreApplication.translate(
                "TabGeneral", "Modulate sleep time between extractor Sleep and (extractor Sleep + ModulateSleep)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_sleepmodulate.setText("")
        self.cfgui_sleepmodulate.setPlaceholderText(QCoreApplication.translate("TabGeneral", "Integer (Seconds)", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_extendedmetadata.setToolTip(
            QCoreApplication.translate(
                "TabGeneral",
                "<html><head/><body><p>Adds to every gallery-dl job configuration:</p><p>&quot;http-metadata&quot;</p><p>&quot;version-metadata&quot;</p><p>&quot;extractor-metadata&quot;</p><p>&quot;url-metadata&quot;</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfgui_extendedmetadata.setText(QCoreApplication.translate("TabGeneral", "Extended metadata", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QCoreApplication.translate("TabGeneral", "Settings", None))

    # retranslateUi
