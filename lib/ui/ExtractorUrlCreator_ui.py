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
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_URLManager(object):
    def setupUi(self, URLManager):
        if not URLManager.objectName():
            URLManager.setObjectName("URLManager")
        URLManager.resize(558, 460)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        URLManager.setPalette(palette)
        self.verticalLayout_4 = QVBoxLayout(URLManager)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(URLManager)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_7)
        self.widget.setObjectName("widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")

        self.verticalLayout.addWidget(self.label)

        self.extractorUrls = QListWidget(self.widget)
        QListWidgetItem(self.extractorUrls)
        self.extractorUrls.setObjectName("extractorUrls")
        font = QFont()
        font.setFamilies(["Courier New"])
        font.setStyleStrategy(QFont.NoAntialias)
        self.extractorUrls.setFont(font)

        self.verticalLayout.addWidget(self.extractorUrls)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName("widget_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.cfgui_argumets = QLineEdit(self.widget_5)
        self.cfgui_argumets.setObjectName("cfgui_argumets")

        self.horizontalLayout_4.addWidget(self.cfgui_argumets)

        self.horizontalLayout_3.addWidget(self.widget_5)

        self.verticalLayout.addWidget(self.widget_2)

        self.horizontalLayout_2.addWidget(self.widget)

        self.widget_6 = QWidget(self.widget_7)
        self.widget_6.setObjectName("widget_6")
        self.widget_6.setMaximumSize(QSize(230, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget_6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QLabel(self.widget_6)
        self.label_3.setObjectName("label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.cfgui_arg1 = QLineEdit(self.widget_6)
        self.cfgui_arg1.setObjectName("cfgui_arg1")

        self.verticalLayout_3.addWidget(self.cfgui_arg1)

        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName("label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.cfgui_arg2 = QLineEdit(self.widget_6)
        self.cfgui_arg2.setObjectName("cfgui_arg2")

        self.verticalLayout_3.addWidget(self.cfgui_arg2)

        self.label_6 = QLabel(self.widget_6)
        self.label_6.setObjectName("label_6")

        self.verticalLayout_3.addWidget(self.label_6)

        self.cfgui_combo = QComboBox(self.widget_6)
        self.cfgui_combo.setObjectName("cfgui_combo")

        self.verticalLayout_3.addWidget(self.cfgui_combo)

        self.btn_insert = QPushButton(self.widget_6)
        self.btn_insert.setObjectName("btn_insert")

        self.verticalLayout_3.addWidget(self.btn_insert)

        self.horizontalLayout_2.addWidget(self.widget_6)

        self.verticalLayout_4.addWidget(self.widget_7)

        self.line = QFrame(URLManager)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.importWidget = QWidget(URLManager)
        self.importWidget.setObjectName("importWidget")
        self.verticalLayout_5 = QVBoxLayout(self.importWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, -1, -1, 6)
        self.label_7 = QLabel(self.importWidget)
        self.label_7.setObjectName("label_7")

        self.verticalLayout_5.addWidget(self.label_7)

        self.ImportedList = QTextEdit(self.importWidget)
        self.ImportedList.setObjectName("ImportedList")
        self.ImportedList.setAcceptRichText(False)

        self.verticalLayout_5.addWidget(self.ImportedList)

        self.widget_10 = QWidget(self.importWidget)
        self.widget_10.setObjectName("widget_10")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_importingDone = QPushButton(self.widget_10)
        self.btn_importingDone.setObjectName("btn_importingDone")

        self.horizontalLayout_5.addWidget(self.btn_importingDone)

        self.verticalLayout_5.addWidget(self.widget_10)

        self.verticalLayout_4.addWidget(self.importWidget)

        self.runWidget = QWidget(URLManager)
        self.runWidget.setObjectName("runWidget")
        self.verticalLayout_2 = QVBoxLayout(self.runWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, -1, -1, 6)
        self.label_2 = QLabel(self.runWidget)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.chosenUrls = QListWidget(self.runWidget)
        self.chosenUrls.setObjectName("chosenUrls")
        self.chosenUrls.setFont(font)
        self.chosenUrls.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.verticalLayout_2.addWidget(self.chosenUrls)

        self.widget_4 = QWidget(self.runWidget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_import = QPushButton(self.widget_4)
        self.btn_import.setObjectName("btn_import")

        self.horizontalLayout.addWidget(self.btn_import)

        self.btn_removeselected = QPushButton(self.widget_4)
        self.btn_removeselected.setObjectName("btn_removeselected")

        self.horizontalLayout.addWidget(self.btn_removeselected)

        self.btn_start = QPushButton(self.widget_4)
        self.btn_start.setObjectName("btn_start")

        self.horizontalLayout.addWidget(self.btn_start)

        self.cfg_quickExtraction = QCheckBox(self.widget_4)
        self.cfg_quickExtraction.setObjectName("cfg_quickExtraction")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cfg_quickExtraction.sizePolicy().hasHeightForWidth())
        self.cfg_quickExtraction.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.cfg_quickExtraction)

        self.verticalLayout_2.addWidget(self.widget_4)

        self.verticalLayout_4.addWidget(self.runWidget)

        self.retranslateUi(URLManager)

        QMetaObject.connectSlotsByName(URLManager)

    # setupUi

    def retranslateUi(self, URLManager):
        URLManager.setWindowTitle(QCoreApplication.translate("URLManager", "Form", None))
        self.label.setText(QCoreApplication.translate("URLManager", "Extractor URLs List", None))

        __sortingEnabled = self.extractorUrls.isSortingEnabled()
        self.extractorUrls.setSortingEnabled(False)
        ___qlistwidgetitem = self.extractorUrls.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("URLManager", "rwar", None))
        self.extractorUrls.setSortingEnabled(__sortingEnabled)

        # if QT_CONFIG(tooltip)
        self.extractorUrls.setToolTip(
            QCoreApplication.translate("URLManager", "Select the URL and write in the textboxes to modify it", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("URLManager", "Append these arguments to pass to gallery-dl", None))
        # endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("URLManager", "Additional arguments:", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_argumets.setToolTip(QCoreApplication.translate("URLManager", "Append these arguments to pass to gallery-dl", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_3.setToolTip(
            QCoreApplication.translate(
                "URLManager", "<html><head/><body><p>Specify what you want to write in the url</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("URLManager", "Argument 1:", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_arg1.setToolTip(QCoreApplication.translate("URLManager", "Specify what you want to write in the url", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("URLManager", "Specify what you want to write in the url", None))
        # endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("URLManager", "Argument 2:", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_arg2.setToolTip(QCoreApplication.translate("URLManager", "Specify what you want to write in the url", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_6.setToolTip(
            QCoreApplication.translate(
                "URLManager", "<html><head/><body><p>Base off settings such as directory and filters from this user</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("URLManager", "Settings based on user:", None))
        # if QT_CONFIG(tooltip)
        self.cfgui_combo.setToolTip(
            QCoreApplication.translate(
                "URLManager", "<html><head/><body><p>Base off settings such as directory and filters from this user</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.btn_insert.setToolTip(QCoreApplication.translate("URLManager", "Insert the URL for extraction", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_insert.setText(QCoreApplication.translate("URLManager", "Insert", None))
        self.label_7.setText(QCoreApplication.translate("URLManager", "Copy and paste your URLs here", None))
        # if QT_CONFIG(tooltip)
        self.ImportedList.setToolTip(
            QCoreApplication.translate(
                "URLManager",
                "Paste here your URLs, one per line\n"
                "The URLs must be compatible with the 'Extractor URLs List', any invalid URL won't be added",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.ImportedList.setPlaceholderText(QCoreApplication.translate("URLManager", "One URL per line", None))
        self.btn_importingDone.setText(QCoreApplication.translate("URLManager", "Done", None))
        self.label_2.setText(QCoreApplication.translate("URLManager", "URLs Chosen", None))
        # if QT_CONFIG(tooltip)
        self.chosenUrls.setToolTip(QCoreApplication.translate("URLManager", "Press 'Start!' to start the extraction with these urls", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.btn_import.setToolTip(QCoreApplication.translate("URLManager", "Import a list of URLs from a list", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_import.setText(QCoreApplication.translate("URLManager", "Import ", None))
        # if QT_CONFIG(tooltip)
        self.btn_removeselected.setToolTip(QCoreApplication.translate("URLManager", "Remove selected url", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_removeselected.setText(QCoreApplication.translate("URLManager", "Remove Selected", None))
        # if QT_CONFIG(tooltip)
        self.btn_start.setToolTip(QCoreApplication.translate("URLManager", "Start the extraction with the urls defined above", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_start.setText(QCoreApplication.translate("URLManager", "Start!", None))
        # if QT_CONFIG(tooltip)
        self.cfg_quickExtraction.setToolTip(
            QCoreApplication.translate(
                "URLManager",
                "<html><head/><body><p>Modify the jobs to have lowered sleep time, this won't prevent you from getting rate limited</p><p>Use this in case you have only a few urls you want to extract</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_quickExtraction.setText(QCoreApplication.translate("URLManager", "Quick extraction", None))

    # retranslateUi
