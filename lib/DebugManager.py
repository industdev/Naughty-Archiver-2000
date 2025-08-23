import os
from datetime import datetime


class DebugManager:
    def __init__(self, main, debugDPath: str):
        self.main = main
        self.debugDPath = debugDPath
        self.openFiles = {}

        if not os.path.exists(debugDPath):
            os.makedirs(debugDPath)

    def debug(self, text: str, filename: str, noFormat: bool = False):
        """write text to filename specified

        Args:
            text (str): contents
            filename (str): Name of the debug filename
            noFormat (bool, optional): Don't add date and format new lines correctly. Defaults to False
        """

        if filename:
            filepath = os.path.join(self.debugDPath, f"{filename}.txt")

            if filepath not in self.openFiles:
                self.openFiles[filepath] = open(filepath, "a", encoding="utf-8")

            if noFormat:
                message = text
            else:
                timestamp = f"[{datetime.now()}] "
                message = timestamp + text

            self.openFiles[filepath].write(message + ("\n" if not message.endswith("\n") else ""))
            self.openFiles[filepath].flush()
        else:
            self.main.cmd.error(f"[{datetime.now()}] DebugManager -> No filename specified")

    def closeAll(self):
        """Closes and deletes all opened files"""
        self.main.cmd.info(f"[{datetime.now()}] Closing debug manager...")
        for filepath, file in self.openFiles.items():
            file.close()
            self.main.safeTrash(filepath)
        self.openFiles.clear()

    def closeFile(self, filename: str):
        """Close single file and deletes entry"""
        filepath = os.path.join(self.debugDPath, f"{filename}.txt")
        if filepath in self.openFiles:
            self.openFiles[filepath].close()
            del self.openFiles[filepath]
