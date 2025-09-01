from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor, ExtractorEntry

from lib.Enums import Configure, SpecialWidgets, Validation, Widgets
from lib.VarHelper import VarHelper

from lib.ui.StatCounter import StatCounter
from PySide6.QtWidgets import *  # type: ignore
from datetime import datetime
import os
import time


class Configurator:
    def __init__(self, main: "MainApp"):
        start = time.perf_counter()
        self.main = main
        self.oneTimeLoaded = False
        self.logger = None
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")

    def loadwidgetsConnection(self, extractor: "Extractor", logger=None):
        if logger:
            self.logger = logger
        if extractor:
            self._setupTabConnections(extractor)

    #   Sets up all connections for a tab based on its getConnections returned dict
    def _setupTabConnections(self, ext):
        try:
            tab = ext.ui
            cfg = ext.config.settings

            keyCount = 0
            funCount = 1
            widgetCount = 0

            for conn in ext.widgetsConnection:
                name = conn.get(Configure.WIDGET)
                widget = getattr(tab, name)
                widgetCount += 1
                key = conn.get(Configure.KEY)
                validation = conn.get(Configure.VALIDATION)
                function = conn.get(Configure.FUNCTION)

                self.main.debuggy(f" :{name} -> {key} ({validation}) to {function}", "init")

                #   Connect optional external function
                if function:
                    if hasattr(widget, "clicked"):
                        widget.clicked.connect(function)
                    elif hasattr(widget, "toggled"):
                        widget.toggled.connect(function)
                    elif hasattr(widget, "editingFinished"):
                        widget.editingFinished.connect(function)
                    elif hasattr(widget, "currentIndexChanged"):
                        widget.currentIndexChanged.connect(function)
                    else:
                        self.main.cmd.warning(f"No connectable signal found for function on widget {name}")

                #   Connect to config update
                if not key:
                    continue
                else:
                    keyCount += 1
                try:
                    funCount += 1
                    if isinstance(widget, QCheckBox):
                        widget.stateChanged.connect(
                            lambda val, c=cfg, k=key, v=validation, e=ext, w=widget: self.updateConfigByWidget(c, k, bool(val), e, v, w)
                        )
                    elif isinstance(widget, QGroupBox):
                        widget.toggled.connect(
                            lambda val, c=cfg, k=key, v=validation, e=ext, w=widget: self.updateConfigByWidget(c, k, bool(val), e, v, w)
                        )
                    elif isinstance(widget, QLineEdit):
                        widget.editingFinished.connect(
                            lambda c=cfg, k=key, v=validation, e=ext, w=widget: self.updateConfigByWidget(c, k, w.text(), e, v, w)
                        )
                    elif isinstance(widget, QComboBox):
                        widget.currentIndexChanged.connect(
                            lambda val, c=cfg, k=key, v=validation, e=ext, w=widget: self.updateConfigByWidget(c, k, int(val), e, v, w)
                        )
                    elif isinstance(widget, QLabel):
                        pass
                    else:
                        self.main.cmd.warning(f"[{datetime.now()}] Unsupported widget type for config binding: {name}")
                        funCount -= 1
                except Exception as e:
                    self.main.varHelper.exception(e)
                    self.main.cmd.error(f"Error when connecting the widgets: {e}")
            self.main.cmd.info(f" :Loaded {widgetCount} widgets")
            self.main.cmd.info(f" :Loaded {funCount} functions to {keyCount} keys")
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(message=f"Error when loading widgets: {e}", title=f"{ext.name} widgets loading error")

    #   Function to update the config once a widget is interacted with or handle special needs
    def updateConfigByWidget(self, jsonKey, keyName, value, ext, validation, widget):
        if validation:
            if validation == Validation.INTEGER:
                if not VarHelper.isValidInteger(value):
                    self.main.qtHelper.Throw(f"The value of {keyName} must be an integer!")
                    return
                else:
                    value = int(value)
            elif validation == Validation.BOOLEAN:
                value = bool(value)
            elif validation == Validation.PATH:
                if not VarHelper.isValidPath(value, allowDefault=False):
                    self.main.qtHelper.Throw(f"The value of {keyName} must be a valid absolute path!")
                    return
                value = os.path.normpath(value)
            elif validation == SpecialWidgets.EXT_GRPBOX:
                if not value:
                    widget.setTitle(f"{ext.fullName} Settings (Disabled)")
                else:
                    widget.setTitle(f"{ext.fullName} Settings")
            elif validation == Validation.FLOAT:
                if not VarHelper.isValidFloat(value):
                    self.main.qtHelper.Throw(f"The value of {keyName} must be a float!")
                    return
            elif validation == Validation.NUMBER:
                if not VarHelper.isValidFloat(value):
                    self.main.qtHelper.Throw(f"The value of {keyName} must be any number!")
                    return

        jsonKey[keyName] = value
        self.logger.other(f"Saved {ext.configName}.{keyName} with value {value}")  # type: ignore
        ext.config.saveConfig()

    #   Creates and sets the widgets to extractor.ui from the configuration provided by the user
    def createWidgetsFromConfig(self, extractor, main):
        try:
            #   Get the UI configuration from the extractor
            ui_config = extractor.widgetsConfiguration

            grpbox = extractor.ui.grpbox_settings
            layout = grpbox.layout()

            #   Process each widget configuration
            widgetCount = 0
            for config in ui_config:
                widgetName = config.get(Configure.NAME)
                widgetType = config.get(Configure.WIDGET)
                defaultValue = config.get(Configure.DEFAULT)
                labelText = config.get(Configure.LABEL, "")
                tooltip = config.get(Configure.TOOLTIP, "")
                placeholder = config.get(Configure.PLACEHOLDER, "")
                entries = config.get(Configure.ENTRIES, [])

                if not widgetName or not widgetType:
                    main.cmd.warning(f"Widget configuration missing NAME or WIDGET: {config}")
                    continue
                else:
                    widgetCount += 1

                #   Create the widget based on type
                widget = None

                if widgetType == Widgets.CHECKBOX:
                    widget = QCheckBox()
                    if labelText:
                        widget.setText(labelText)

                    widget.setChecked(bool(defaultValue))

                elif widgetType == Widgets.TEXTBOX:
                    widget = QLineEdit()
                    if placeholder:
                        widget.setPlaceholderText(placeholder)
                    widget.setText(str(defaultValue))

                elif widgetType == Widgets.COMBOBOX:
                    widget = QComboBox()
                    if entries:
                        widget.addItems(entries)
                    if defaultValue is not None and isinstance(defaultValue, int):
                        if 0 <= defaultValue < len(entries):
                            widget.setCurrentIndex(defaultValue)

                elif widgetType == Widgets.BUTTON:
                    widget = QPushButton()
                    if labelText:
                        widget.setText(labelText)
                    widget.setText(defaultValue)
                else:
                    main.cmd.warning(f"Unsupported widget type: {widgetType}")
                    continue

                if widget is None:
                    continue

                #   Set tooltip if provided
                if tooltip:
                    widget.setToolTip(tooltip)

                setattr(extractor.ui, widgetName, widget)

                #   Add to layout
                if widgetType == Widgets.CHECKBOX:
                    layout.addRow("", widget)
                else:
                    if labelText:
                        label = QLabel(labelText)
                        layout.addRow(label, widget)
                    else:
                        layout.addRow("", widget)

                main.debuggy(f" :{widgetName} -> {extractor.name} ", "init")
            main.cmd.info(f" :Created {widgetCount} widgets")
        except Exception as e:
            self.main.varHelper.exception(e)
            main.cmd.error(f"{[datetime.now()]} Error creating widgets for {extractor.name}: {e}")
            main.qtHelper.Throw(title="Widget Creation Error", message=f"Failed to create widgets: {e}")

    def updateNonExtractorUI(self):
        try:
            if not self.oneTimeLoaded:
                #   Stats
                statFields = [
                    "totAmount",
                    "totSize",
                    "totMediaAmount",
                    "totMetadataAmount",
                    "totMetadataSize",
                    "totMediaSize",
                    "totApiCalls",
                    "totExtractorsRuntime",
                    "totExtractorsRuns",
                ]

                for field in statFields:
                    label = getattr(self.main.stats.ui, f"lbl_{field}")
                    value = self.main.stats.counter.config.settings[field]

                    if field == "totMediaSize" or field == "totMetadataSize":
                        value = StatCounter.toSize(value)

                    if field == "totExtractorsRuntime":
                        value = StatCounter.toTime(value)

                    label.setText(f"{label.text()}{value}")

                if self.main.stats.counter.config.settings["since"] == None:
                    date = datetime.today().strftime("%d/%m/%Y")
                    self.main.stats.ui.lbl_since.setText(f"Since: {date}")
                    self.main.stats.counter.config.settings["since"] = date
                else:
                    date = self.main.stats.counter.config.settings["since"]
                    self.main.stats.ui.lbl_since.setText(f"Since: {date}")

                self.oneTimeLoaded = True

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Error updating UI from config: {e}")  # type: ignore
            self.main.qtHelper.Throw(title="Config error", message=f"Error updating UI from config: {e}")
