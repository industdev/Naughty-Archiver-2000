
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_URLManager(object):
    def setupUi(self, URLManager):
        if not URLManager.objectName():
            URLManager.setObjectName(u"URLManager")
        URLManager.resize(586, 418)
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
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_7 = QWidget(URLManager)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_7)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.extractorUrls = QListWidget(self.widget)
        QListWidgetItem(self.extractorUrls)
        self.extractorUrls.setObjectName(u"extractorUrls")
        font = QFont()
        font.setFamilies([u"Courier New"])
        font.setStyleStrategy(QFont.NoAntialias)
        self.extractorUrls.setFont(font)

        self.verticalLayout.addWidget(self.extractorUrls)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.cfgui_argumets = QLineEdit(self.widget_5)
        self.cfgui_argumets.setObjectName(u"cfgui_argumets")

        self.horizontalLayout_4.addWidget(self.cfgui_argumets)


        self.horizontalLayout_3.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.widget_2)


        self.horizontalLayout_2.addWidget(self.widget)

        self.widget_6 = QWidget(self.widget_7)
        self.widget_6.setObjectName(u"widget_6")
        self.widget_6.setMaximumSize(QSize(230, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget_6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.widget_6)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.cfgui_arg1 = QLineEdit(self.widget_6)
        self.cfgui_arg1.setObjectName(u"cfgui_arg1")

        self.verticalLayout_3.addWidget(self.cfgui_arg1)

        self.label_5 = QLabel(self.widget_6)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.cfgui_arg2 = QLineEdit(self.widget_6)
        self.cfgui_arg2.setObjectName(u"cfgui_arg2")

        self.verticalLayout_3.addWidget(self.cfgui_arg2)

        self.label_6 = QLabel(self.widget_6)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_3.addWidget(self.label_6)

        self.cfgui_combo = QComboBox(self.widget_6)
        self.cfgui_combo.setObjectName(u"cfgui_combo")

        self.verticalLayout_3.addWidget(self.cfgui_combo)

        self.btn_insert = QPushButton(self.widget_6)
        self.btn_insert.setObjectName(u"btn_insert")

        self.verticalLayout_3.addWidget(self.btn_insert)


        self.horizontalLayout_2.addWidget(self.widget_6)


        self.verticalLayout_4.addWidget(self.widget_7)

        self.line = QFrame(URLManager)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.widget_3 = QWidget(URLManager)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, -1, -1, 6)
        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.chosenUrls = QListWidget(self.widget_3)
        self.chosenUrls.setObjectName(u"chosenUrls")
        self.chosenUrls.setFont(font)
        self.chosenUrls.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.verticalLayout_2.addWidget(self.chosenUrls)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_removeselected = QPushButton(self.widget_4)
        self.btn_removeselected.setObjectName(u"btn_removeselected")

        self.horizontalLayout.addWidget(self.btn_removeselected)

        self.btn_start = QPushButton(self.widget_4)
        self.btn_start.setObjectName(u"btn_start")

        self.horizontalLayout.addWidget(self.btn_start)


        self.verticalLayout_2.addWidget(self.widget_4)


        self.verticalLayout_4.addWidget(self.widget_3)


        self.retranslateUi(URLManager)

        QMetaObject.connectSlotsByName(URLManager)
    # setupUi

    def retranslateUi(self, URLManager):
        URLManager.setWindowTitle(QCoreApplication.translate("URLManager", u"Form", None))
        self.label.setText(QCoreApplication.translate("URLManager", u"Extractor URLs List", None))

        __sortingEnabled = self.extractorUrls.isSortingEnabled()
        self.extractorUrls.setSortingEnabled(False)
        ___qlistwidgetitem = self.extractorUrls.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("URLManager", u"rwar", None));
        self.extractorUrls.setSortingEnabled(__sortingEnabled)

#if QT_CONFIG(tooltip)
        self.extractorUrls.setToolTip(QCoreApplication.translate("URLManager", u"Select the URL and write in the textboxes to modify it", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("URLManager", u"Append these arguments to pass to gallery-dl", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("URLManager", u"Additional arguments:", None))
#if QT_CONFIG(tooltip)
        self.cfgui_argumets.setToolTip(QCoreApplication.translate("URLManager", u"Append these arguments to pass to gallery-dl", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("URLManager", u"<html><head/><body><p>Specify what you want to write in the url</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("URLManager", u"Argument 1:", None))
#if QT_CONFIG(tooltip)
        self.cfgui_arg1.setToolTip(QCoreApplication.translate("URLManager", u"Specify what you want to write in the url", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("URLManager", u"Specify what you want to write in the url", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("URLManager", u"Argument 2:", None))
#if QT_CONFIG(tooltip)
        self.cfgui_arg2.setToolTip(QCoreApplication.translate("URLManager", u"Specify what you want to write in the url", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("URLManager", u"<html><head/><body><p>Base off settings such as directory and filters from this user</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("URLManager", u"Settings based on user:", None))
#if QT_CONFIG(tooltip)
        self.cfgui_combo.setToolTip(QCoreApplication.translate("URLManager", u"<html><head/><body><p>Base off settings such as directory and filters from this user</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_insert.setToolTip(QCoreApplication.translate("URLManager", u"Insert the URL for extraction", None))
#endif // QT_CONFIG(tooltip)
        self.btn_insert.setText(QCoreApplication.translate("URLManager", u"Insert", None))
        self.label_2.setText(QCoreApplication.translate("URLManager", u"URLs Chosen", None))
#if QT_CONFIG(tooltip)
        self.chosenUrls.setToolTip(QCoreApplication.translate("URLManager", u"Press 'Start!' to start the extraction with these urls", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_removeselected.setToolTip(QCoreApplication.translate("URLManager", u"Remove selected url", None))
#endif // QT_CONFIG(tooltip)
        self.btn_removeselected.setText(QCoreApplication.translate("URLManager", u"Remove Selected", None))
#if QT_CONFIG(tooltip)
        self.btn_start.setToolTip(QCoreApplication.translate("URLManager", u"Start the extraction with the urls defined above", None))
#endif // QT_CONFIG(tooltip)
        self.btn_start.setText(QCoreApplication.translate("URLManager", u"Start!", None))
    # retranslateUi

