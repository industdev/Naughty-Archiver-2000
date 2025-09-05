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
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_UnixCreator(object):
    def setupUi(self, UnixCreator):
        if not UnixCreator.objectName():
            UnixCreator.setObjectName("UnixCreator")
        UnixCreator.resize(489, 132)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        UnixCreator.setPalette(palette)
        self.gridLayout_4 = QGridLayout(UnixCreator)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(UnixCreator)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.widget_2)
        self.formLayout.setObjectName("formLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName("label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.cfg_day = QLineEdit(self.widget_2)
        self.cfg_day.setObjectName("cfg_day")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cfg_day)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumSize(QSize(40, 0))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.cfg_month = QLineEdit(self.widget_2)
        self.cfg_month.setObjectName("cfg_month")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cfg_month)

        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.cfg_year = QLineEdit(self.widget_2)
        self.cfg_year.setObjectName("cfg_year")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cfg_year)

        self.verticalLayout_2.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 6)
        self.lbl_unix = QLabel(self.widget_3)
        self.lbl_unix.setObjectName("lbl_unix")
        self.lbl_unix.setMinimumSize(QSize(40, 0))

        self.horizontalLayout.addWidget(self.lbl_unix)

        self.cfg_result = QLineEdit(self.widget_3)
        self.cfg_result.setObjectName("cfg_result")

        self.horizontalLayout.addWidget(self.cfg_result)

        self.btn_copy = QPushButton(self.widget_3)
        self.btn_copy.setObjectName("btn_copy")

        self.horizontalLayout.addWidget(self.btn_copy)

        self.btn_folder = QPushButton(self.widget_3)
        self.btn_folder.setObjectName("btn_folder")

        self.horizontalLayout.addWidget(self.btn_folder)

        self.verticalLayout_2.addWidget(self.widget_3)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.gridLayout_4.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(UnixCreator)

        QMetaObject.connectSlotsByName(UnixCreator)

    # setupUi

    def retranslateUi(self, UnixCreator):
        UnixCreator.setWindowTitle(QCoreApplication.translate("UnixCreator", "Form", None))
        self.label.setText(QCoreApplication.translate("UnixCreator", "Day", None))
        self.label_2.setText(QCoreApplication.translate("UnixCreator", "Month", None))
        self.label_3.setText(QCoreApplication.translate("UnixCreator", "Year", None))
        self.lbl_unix.setText(QCoreApplication.translate("UnixCreator", "UNIX: ", None))
        self.btn_copy.setText(QCoreApplication.translate("UnixCreator", "Copy", None))
        self.btn_folder.setText(QCoreApplication.translate("UnixCreator", "Select from folder", None))

    # retranslateUi
