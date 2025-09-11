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
        Form.resize(396, 208)
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
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.cfg_l4 = QLabel(self.widget)
        self.cfg_l4.setObjectName("cfg_l4")

        self.gridLayout.addWidget(self.cfg_l4, 5, 2, 1, 1)

        self.cfg_c2 = QLabel(self.widget)
        self.cfg_c2.setObjectName("cfg_c2")

        self.gridLayout.addWidget(self.cfg_c2, 3, 1, 1, 1)

        self.cfg_l5 = QLabel(self.widget)
        self.cfg_l5.setObjectName("cfg_l5")

        self.gridLayout.addWidget(self.cfg_l5, 6, 2, 1, 1)

        self.cfg_l1 = QLabel(self.widget)
        self.cfg_l1.setObjectName("cfg_l1")

        self.gridLayout.addWidget(self.cfg_l1, 1, 2, 1, 1)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName("label_12")

        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)

        self.cfg_ffmpeg = QCheckBox(self.widget)
        self.cfg_ffmpeg.setObjectName("cfg_ffmpeg")

        self.gridLayout.addWidget(self.cfg_ffmpeg, 3, 0, 1, 1)

        self.cfg_l2 = QLabel(self.widget)
        self.cfg_l2.setObjectName("cfg_l2")

        self.gridLayout.addWidget(self.cfg_l2, 3, 2, 1, 1)

        self.cfg_aria2c = QCheckBox(self.widget)
        self.cfg_aria2c.setObjectName("cfg_aria2c")

        self.gridLayout.addWidget(self.cfg_aria2c, 6, 0, 1, 1)

        self.cfg_ytdlp = QCheckBox(self.widget)
        self.cfg_ytdlp.setObjectName("cfg_ytdlp")

        self.gridLayout.addWidget(self.cfg_ytdlp, 5, 0, 1, 1)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName("label_11")

        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)

        self.cfg_c1 = QLabel(self.widget)
        self.cfg_c1.setObjectName("cfg_c1")

        self.gridLayout.addWidget(self.cfg_c1, 1, 1, 1, 1)

        self.cfg_c3 = QLabel(self.widget)
        self.cfg_c3.setObjectName("cfg_c3")

        self.gridLayout.addWidget(self.cfg_c3, 4, 1, 1, 1)

        self.cfg_mkvmerge = QCheckBox(self.widget)
        self.cfg_mkvmerge.setObjectName("cfg_mkvmerge")

        self.gridLayout.addWidget(self.cfg_mkvmerge, 4, 0, 1, 1)

        self.cfg_gdl = QCheckBox(self.widget)
        self.cfg_gdl.setObjectName("cfg_gdl")

        self.gridLayout.addWidget(self.cfg_gdl, 1, 0, 1, 1)

        self.cfg_l3 = QLabel(self.widget)
        self.cfg_l3.setObjectName("cfg_l3")

        self.gridLayout.addWidget(self.cfg_l3, 4, 2, 1, 1)

        self.cfg_c4 = QLabel(self.widget)
        self.cfg_c4.setObjectName("cfg_c4")

        self.gridLayout.addWidget(self.cfg_c4, 5, 1, 1, 1)

        self.cfg_c5 = QLabel(self.widget)
        self.cfg_c5.setObjectName("cfg_c5")

        self.gridLayout.addWidget(self.cfg_c5, 6, 1, 1, 1)

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
        self.cfg_l4.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_c2.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_l5.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_l1.setText(QCoreApplication.translate("Form", "0", None))
        self.label_12.setText(QCoreApplication.translate("Form", "Latest version", None))
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
        self.cfg_l2.setText(QCoreApplication.translate("Form", "0", None))
        # if QT_CONFIG(tooltip)
        self.cfg_aria2c.setToolTip(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>Aria2c is used by YT-dlp to download youtube and nicovideo media faster<br/>Source: https://aria2.github.io/</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_aria2c.setText(QCoreApplication.translate("Form", "Aria2c", None))
        # if QT_CONFIG(tooltip)
        self.cfg_ytdlp.setToolTip(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>YT-dlp is used to download youtube and nicovideo media<br/>Source: https://github.com/yt-dlp/yt-dlp</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cfg_ytdlp.setText(QCoreApplication.translate("Form", "YT-dlp", None))
        self.label_11.setText(QCoreApplication.translate("Form", "Current version", None))
        self.cfg_c1.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_c3.setText(QCoreApplication.translate("Form", "0", None))
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
        self.cfg_l3.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_c4.setText(QCoreApplication.translate("Form", "0", None))
        self.cfg_c5.setText(QCoreApplication.translate("Form", "0", None))
        self.btn_download.setText(QCoreApplication.translate("Form", "Download Selected", None))

    # retranslateUi
