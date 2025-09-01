import os
import sys
from datetime import datetime


class PathManager:
    def __init__(self, file):
        self.file = file

    def getScriptDir(self):
        if getattr(sys, "frozen", False):
            return os.path.normpath(os.path.dirname(sys.executable))
        else:
            return os.path.normpath(os.path.dirname(os.path.abspath(self.file)))

    def getInternalRes(self, rel):
        try:
            base_path = sys._MEIPASS  # type: ignore
        except AttributeError:
            base_path = os.path.join(self.getScriptDir())

        path = os.path.join(base_path, rel)

        if os.path.exists(path):
            print(f"[{datetime.now()}] Get: {path}")
        else:
            if not os.path.splitext(rel)[1]:
                os.makedirs(path, exist_ok=True)
                print(f"[{datetime.now()}] Created internal folder: {path}")
            else:
                print(f"[{datetime.now()}] Internal path not found: {path}")
                sys.exit(0)

        return os.path.normpath(path)

    def getExternalRes(self, rel):
        base_path = self.getScriptDir()
        path = os.path.join(base_path, rel)

        if os.path.exists(path):
            print(f"[{datetime.now()}] Get: {path}")
        else:
            if not os.path.splitext(rel)[1]:
                os.makedirs(path, exist_ok=True)
                print(f"[{datetime.now()}] Created external folder: {path}")
            else:
                print(f"[{datetime.now()}] External path not found: {path}")

        return os.path.normpath(path)
