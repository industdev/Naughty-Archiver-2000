import logging
import os
from datetime import datetime

class LevelPrefixFormatter(logging.Formatter):
    LEVEL_PREFIXES = {
        logging.DEBUG: "[0]",
        logging.INFO: "[1]",
        logging.WARNING: "[2]",
        logging.ERROR: "[3]",
        logging.CRITICAL: "[4]",
    }

    def format(self, record):
        prefix = self.LEVEL_PREFIXES.get(record.levelno, "[?]")
        original_msg = super().format(record)
        return f"{prefix}{original_msg}"

class CmdLogger:
    def __init__(self, log_name="cmdLogger", logDPath=None):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.logger.handlers.clear()

        if logDPath is None:
            logDPath = os.path.join(os.getcwd(), "saved", "logs")

        os.makedirs(logDPath, exist_ok=True)
        log_file = os.path.join(logDPath, "cmd.txt")

        #   Clear previous content
        with open(log_file, 'w') as f:
            pass

        #   Setup formatter
        formatter = LevelPrefixFormatter('%(message)s')

        #   File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        #   Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.logger.debug(f"[{datetime.now()}] Start")
    
    def getLogger(self):
        return self.logger