from enum import Enum


#   Extractor UI configuration for widgets
class Configure(Enum):
    NAME = "NAME"
    WIDGET = "WIDGET"
    VALIDATION = "VALIDATION"
    FUNCTION = "FUNCTION"
    KEY = "KEY"
    VALUE = "VALUE"
    DEFAULT = "DEFAULT"
    ENTRIES = "ENTRIES"
    TOOLTIP = "TOOLTIP"
    LABEL = "LABEL"
    PLACEHOLDER = "PLACEHOLDER"


#   Widgets available for the extractor's UI
class Widgets(Enum):
    CHECKBOX = "CHECKBOX"
    TEXTBOX = "TEXTBOX"
    COMBOBOX = "COMBOBOX"
    BUTTON = "BUTTON"


#   Log levels for console loggers
from PySide6.QtGui import QColor


class LogLevel(Enum):
    WHITE = (QColor(240, 240, 240), "1", "Info")
    YELLOW = (QColor(255, 165, 0), "2", "Warning")
    RED = (QColor(255, 0, 0), "3", "Error")
    OTHER = (QColor(0, 255, 255), "4", "Other")
    GREY = (QColor(128, 128, 128), "0", "Debug")
    GREEN = (QColor(0, 255, 0), "5", "Success")

    def __init__(self, color: QColor, num: str, string: str):
        self.color = color
        self.num = num
        self.string = string


#   Output operations/filtering
class Handlers(Enum):
    MESSAGE_ON_ACTION = "MESSAGE_ON_ACTION"
    MESSAGE_ON_LINE = "MESSAGE_ON_LINE"
    LINE_LEVEL = "LINE_LEVEL"
    EVENT = "EVENT"
    RESET_AT = "RESET_AT"
    INHIBIT_BOX = "INHIBIT_BOX"
    STATEMASK = "STATEMASK"
    RUNNERMASK = "RUNNERMASK"
    ACTION = "ACTION"
    REPEATED_ACTION = "REPEATED_ACTION"
    MATCH = "MATCH"


class HandlersActions(Enum):
    STOP = ("STOP", "Stop extraction")
    SKIP_JOB = ("SKIP_JOB", "Skip job")
    SKIP_USER = ("SKIP_USER", "Skip user")
    RETRY_JOB = ("RETRY_JOB", "Retry job")

    def __init__(self, id: str, desc: str):
        self.id = id
        self.desc = desc


#   Validation for variables
class Validation(Enum):
    BOOLEAN = "isValidBoolean"
    NUMBER = "isValidNumber"
    INTEGER = "isValidInteger"
    FLOAT = "isValidFloat"
    DIGIT = "isValidSingleDigit"
    PATH = "isValidPath"
    FILE_PATH = "isValidFPATH"
    DIR_PATH = "isValidDPATH"
    EMPTY = "isEmpty"


##  Internal widgets ##


#   Available widgets for tables
class Table(Enum):
    SHOW = "True"
    HIDE = "False"

    #   Widgets supported
    CHECKBOX = "CHECKBOX"
    DESTINATION = "DESTINATION"
    AUTOTIMESTAMP = "AUTOTIMESTAMP"
    SQLDELETER = "SQLDELETER"
    COMBO = "COMBO"
    TEXTBOX = "TEXTBOX"


#   Na2000 functionalities
#       If a widget has a EXT_GRPBOX validation, it will change it's text to be the extractor name
#       If a widget has a EXT_COOKIESLABEL validation, it will change it's text to be the selected cookies
class SpecialWidgets(Enum):
    EXT_GRPBOX = "EXT_GRPBOX"
    EXT_COOKIESLABEL = "EXT_COOKIESLABEL"
    EXT_BROWSER = "EXT_BROWSER"


#   Message type enum to convert pyqt message icon to loglevel
from PySide6.QtWidgets import QMessageBox


class MessageType(Enum):
    CRITICAL = (QMessageBox.Icon.Critical, LogLevel.RED)
    WARNING = (QMessageBox.Icon.Warning, LogLevel.YELLOW)
    INFO = (QMessageBox.Icon.Information, LogLevel.WHITE)

    def __init__(self, pyqt: QMessageBox.Icon, loglevel):
        self.qtLevel = pyqt
        self.logLevel = loglevel


#   Names for output events
class EventNames(Enum):
    API_CALL = "API_CALL"
    UPDATE_CURSOR = "UPDATE_CURSOR"
    RESET_CURSOR = "RESET_CURSOR"
    ERRORED_URL = "ERRORED_URL"
    USER_NOTFOUND = "USER_NOTFOUND"
    CONVERT_TO_GIF = "CONVERT_TO_GIF"
    TIMESTAMP = "TIMESTAMP"

    @classmethod
    def comboBoxEvents(cls):
        return [cls.API_CALL, cls.UPDATE_CURSOR, cls.RESET_CURSOR, cls.ERRORED_URL, cls.USER_NOTFOUND, cls.CONVERT_TO_GIF, cls.TIMESTAMP]


#   Current state of extractor
class ExtractorState(Enum):
    NORMAL_EXTRACTION = ("NORMAL_EXTRACTION", "extracting user list")
    CUSTOM_URLS_EXTRACTION = ("CUSTOM_URLS_EXTRACTION", "extracting custom URLs")
    ERRORED_URLS_EXTRACTION = ("ERRORED_URLS_EXTRACTION", "recovering errored URLs")
    ANY_URLS_EXTRACTION = ("ANY_URLS_EXTRACTION", "extracting custom or errored URLs")
    IDLE = ("IDLE", "idle (unused)")

    def __init__(self, id: str, desc: str):
        self.id = id
        self.desc = desc


#   Return states for extractions
class Return(Enum):
    USER_SKIPPED = "USER_SKIPPED"
    JOB_SKIPPED = "JOB_SKIPPED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ERR_GALLERY_GENERAL = "ERR_GALLERY_GENERAL"
    ERR_RUNNER_CODE1 = "ERR_RUNNER_CODE1"
    ERR_GALLERY_RETRY = "ERR_GALLERY_RETRY"
    FORCE_TERMINATED = "FORCE_TERMINATED"
