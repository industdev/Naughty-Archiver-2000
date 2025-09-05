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
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(343, 156)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        Form.setPalette(palette)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName("widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.cfg_mkvmerge = QCheckBox(self.widget)
        self.cfg_mkvmerge.setObjectName("cfg_mkvmerge")

        self.gridLayout.addWidget(self.cfg_mkvmerge, 4, 0, 1, 1)

        self.cfg_l3 = QLabel(self.widget)
        self.cfg_l3.setObjectName("cfg_l3")

        self.gridLayout.addWidget(self.cfg_l3, 4, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.cfg_l2 = QLabel(self.widget)
        self.cfg_l2.setObjectName("cfg_l2")

        self.gridLayout.addWidget(self.cfg_l2, 3, 2, 1, 1)

        self.cfg_c3 = QLabel(self.widget)
        self.cfg_c3.setObjectName("cfg_c3")

        self.gridLayout.addWidget(self.cfg_c3, 4, 1, 1, 1)

        self.cfg_ffmpeg = QCheckBox(self.widget)
        self.cfg_ffmpeg.setObjectName("cfg_ffmpeg")

        self.gridLayout.addWidget(self.cfg_ffmpeg, 3, 0, 1, 1)

        self.cfg_l1 = QLabel(self.widget)
        self.cfg_l1.setObjectName("cfg_l1")

        self.gridLayout.addWidget(self.cfg_l1, 1, 2, 1, 1)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName("label_11")

        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)

        self.cfg_gdl = QCheckBox(self.widget)
        self.cfg_gdl.setObjectName("cfg_gdl")

        self.gridLayout.addWidget(self.cfg_gdl, 1, 0, 1, 1)

        self.cfg_c2 = QLabel(self.widget)
        self.cfg_c2.setObjectName("cfg_c2")

        self.gridLayout.addWidget(self.cfg_c2, 3, 1, 1, 1)

        self.cfg_c1 = QLabel(self.widget)
        self.cfg_c1.setObjectName("cfg_c1")

        self.gridLayout.addWidget(self.cfg_c1, 1, 1, 1, 1)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName("label_12")

        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)

        self.verticalLayout.addWidget(self.widget)

        self.btn_download = QPushButton(self.widget_2)
        self.btn_download.setObjectName("btn_download")

        self.verticalLayout.addWidget(self.btn_download)

        self.horizontalLayout.addWidget(self.widget_2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        # if QT_CONFIG(tooltip)
        self.cfg_mkvmerge.setToolTip(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>MKVMerge is used by gallery-dl to convert media to high quality gifs<br/>source: https://mkvtoolnix.download/doc/mkvmerge.html</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_mkvmerge.setText(QCoreApplication.translate("Form", "MKVMerge", None))
        self.cfg_l3.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_l2.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_c3.setText(QCoreApplication.translate("Form", "0", None))
        # if QT_CONFIG(tooltip)
        self.cfg_ffmpeg.setToolTip(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>FFmpeg is used by gallery-dl to convert media to other formats<br/>Source: https://ffmpeg.org/</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_ffmpeg.setText(QCoreApplication.translate("Form", "FFmpeg", None))
        self.cfg_l1.setText(QCoreApplication.translate("Form", "0", None))
        self.label_11.setText(QCoreApplication.translate("Form", "Current version", None))
        # if QT_CONFIG(tooltip)
        self.cfg_gdl.setToolTip(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>Gallery-dl is used to download media from many websites<br/>Source: https://github.com/mikf/gallery-dl</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_gdl.setText(QCoreApplication.translate("Form", "Gallery-dl", None))
        self.cfg_c2.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_c1.setText(QCoreApplication.translate("Form", "0", None))
        self.label_12.setText(QCoreApplication.translate("Form", "Latest version", None))
        # if QT_CONFIG(tooltip)
        self.btn_download.setToolTip(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>Download selected programs, they are all required to be downloaded before starting any instruction</p><p>You can also download them manually and put them in the /external folder as:</p><p>/gallery-dl.exe</p><p>/ffmpeg.exe</p><p>/mkvmerge.exe</p><p>All around it should be 170MB</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_download.setText(QCoreApplication.translate("Form", "Download Selected", None))

    # retranslateUi
