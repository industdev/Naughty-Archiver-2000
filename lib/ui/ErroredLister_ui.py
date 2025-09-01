
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(564, 488)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        Form.setPalette(palette)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 5)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.table = QTableWidget(Form)
        if (self.table.columnCount() < 3):
            self.table.setColumnCount(3)
        font = QFont()
        font.setFamilies([u"Courier New"])
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.table.rowCount() < 2):
            self.table.setRowCount(2)
        self.table.setObjectName(u"table")
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setProperty(u"showDropIndicator", False)
        self.table.setDragDropOverwriteMode(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.setGridStyle(Qt.PenStyle.SolidLine)
        self.table.setRowCount(2)
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.horizontalHeader().setHighlightSections(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.table)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_retrySelected = QPushButton(self.widget)
        self.btn_retrySelected.setObjectName(u"btn_retrySelected")

        self.horizontalLayout.addWidget(self.btn_retrySelected)

        self.btn_clear = QPushButton(self.widget)
        self.btn_clear.setObjectName(u"btn_clear")

        self.horizontalLayout.addWidget(self.btn_clear)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Blahblah", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"User", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Url", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Message", None));
#if QT_CONFIG(tooltip)
        self.btn_retrySelected.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Retry extracting the urls in the selected rows, please take this in consideration:</p><p>- It will use the user on the first column as data for each url in the second</p><p>- If the user is not found in the table then you have to re-create it<br/>- Only selected rows by the index number will be retried<br/>- It can only be done when the extractor is not running</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btn_retrySelected.setText(QCoreApplication.translate("Form", u"Retry selected", None))
#if QT_CONFIG(tooltip)
        self.btn_clear.setToolTip(QCoreApplication.translate("Form", u"Clear the table permanently", None))
#endif // QT_CONFIG(tooltip)
        self.btn_clear.setText(QCoreApplication.translate("Form", u"Clear", None))
    # retranslateUi

