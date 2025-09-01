from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QHBoxLayout, QLabel, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(684, 566)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.Window, brush)
        Form.setPalette(palette)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.cb_fileDropdown = QComboBox(self.widget)
        self.cb_fileDropdown.setObjectName(u"cb_fileDropdown")
        self.cb_fileDropdown.setMinimumSize(QSize(128, 30))

        self.horizontalLayout.addWidget(self.cb_fileDropdown)

        self.btn_saveSelection = QPushButton(self.widget)
        self.btn_saveSelection.setObjectName(u"btn_saveSelection")
        self.btn_saveSelection.setMinimumSize(QSize(0, 32))

        self.horizontalLayout.addWidget(self.btn_saveSelection)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.txt_fileName = QPlainTextEdit(self.widget)
        self.txt_fileName.setObjectName(u"txt_fileName")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_fileName.sizePolicy().hasHeightForWidth())
        self.txt_fileName.setSizePolicy(sizePolicy)
        self.txt_fileName.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.txt_fileName)

        self.btn_add = QPushButton(self.widget)
        self.btn_add.setObjectName(u"btn_add")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy1)
        self.btn_add.setMinimumSize(QSize(32, 32))
        self.btn_add.setMaximumSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.btn_add)

        self.btn_remove = QPushButton(self.widget)
        self.btn_remove.setObjectName(u"btn_remove")
        self.btn_remove.setMinimumSize(QSize(32, 32))
        self.btn_remove.setMaximumSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.btn_remove)

        self.btn_oauth = QPushButton(self.widget)
        self.btn_oauth.setObjectName(u"btn_oauth")
        self.btn_oauth.setMinimumSize(QSize(32, 32))
        self.btn_oauth.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout.addWidget(self.btn_oauth)


        self.verticalLayout.addWidget(self.widget)

        self.textEdit2_line_2 = QFrame(Form)
        self.textEdit2_line_2.setObjectName(u"textEdit2_line_2")
        self.textEdit2_line_2.setFrameShape(QFrame.HLine)
        self.textEdit2_line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.textEdit2_line_2)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textEdit2 = QTextEdit(self.widget_3)
        self.textEdit2.setObjectName(u"textEdit2")
        self.textEdit2.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Courier New"])
        self.textEdit2.setFont(font)
        self.textEdit2.setFrameShape(QFrame.NoFrame)
        self.textEdit2.setFrameShadow(QFrame.Plain)
        self.textEdit2.setLineWidth(0)
        self.textEdit2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

        self.verticalLayout_2.addWidget(self.textEdit2)

        self.textEdit2_line = QFrame(self.widget_3)
        self.textEdit2_line.setObjectName(u"textEdit2_line")
        self.textEdit2_line.setFrameShape(QFrame.HLine)
        self.textEdit2_line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.textEdit2_line)

        self.textEdit1 = QTextEdit(self.widget_3)
        self.textEdit1.setObjectName(u"textEdit1")
        self.textEdit1.setFont(font)
        self.textEdit1.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.textEdit1)


        self.verticalLayout.addWidget(self.widget_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Cookie file:", None))
        self.btn_saveSelection.setText(QCoreApplication.translate("Form", u"Use this one!", None))
        self.txt_fileName.setPlainText("")
        self.txt_fileName.setPlaceholderText(QCoreApplication.translate("Form", u"Enter new filename and press '+'", None))
        self.btn_add.setText(QCoreApplication.translate("Form", u"+", None))
        self.btn_remove.setText(QCoreApplication.translate("Form", u"-", None))
        self.btn_oauth.setText(QCoreApplication.translate("Form", u"Run Pixiv Oauth", None))
        self.textEdit2.setPlaceholderText(QCoreApplication.translate("Form", u"textEdit2", None))
        self.textEdit1.setPlaceholderText(QCoreApplication.translate("Form", u"textEdit1", None))
    # retranslateUi

