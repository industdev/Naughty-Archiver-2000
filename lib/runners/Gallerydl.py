from datetime import datetime
import json
import os
from re import Pattern
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lib.Extractor import Extractor, ExtractorEntry

from lib.Enums import EventNames, Handlers, LogLevel
from lib.runners.RunnerInterface import RunnerInterface


class Gallerydl(RunnerInterface):
    def __init__(self, generalSettings, extractor: "Extractor"):
        try:
            #   Skip media -> "image-filter": "width == 0"
            self.extSettings = extractor.config.settings
            self.generalSettings = generalSettings
            self.extractor = extractor

            patterns = [
                {
                    Handlers.MATCH.name: r"rem Naughty Archiver, please convert",
                    Handlers.LINE_LEVEL.name: LogLevel.GREY.name,
                    Handlers.EVENT.name: EventNames.CONVERT_TO_GIF.name,
                },
                {Handlers.MATCH.name: r"warning", Handlers.LINE_LEVEL.name: LogLevel.YELLOW.name},
                {Handlers.MATCH.name: r" 503 ", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
                {Handlers.MATCH.name: r"\[debug\]", Handlers.LINE_LEVEL.name: LogLevel.GREY.name},
                {Handlers.MATCH.name: r"\[info\]", Handlers.LINE_LEVEL.name: LogLevel.WHITE.name},
                {Handlers.MATCH.name: r"\[error\]", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
                {Handlers.MATCH.name: r"timeout", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
            ]
            self.compiledPatterns = extractor.main.General.runnerHandlerCreator.compile(patterns, self)

            sleepTime = self.extSettings["sleeptime"]
            sleepOffset = generalSettings["sleepmodulate"]
            self.jobBaseConfig: dict[str, Any] = {
                "actions": {"warning:limit_sanity_level": "level = debug"},
                "output": {
                    "mode": "null",
                    "shorten": False,
                    "ansi": False,
                    "private": True,
                    "skip": False,
                    "progress": False,
                    "log": "[{levelname}] {message}",
                    "unsupportedfile": "",
                    "errorfile": "",
                    "stdout": {
                        "encoding": "utf-8",
                        "errors": "backslashreplace",
                        "line_buffering": False,
                    },
                    "stderr": {
                        "encoding": "utf-8",
                        "errors": "backslashreplace",
                        "line_buffering": False,
                    },
                },
                "downloader": {
                    extractor.galleryName: {
                        "part": False,
                        "rate": f"{generalSettings['maxdlspeed']}k",
                        "progress": None,
                        "retries": -1,
                        "mtime": generalSettings["mtimeenabled"],
                    }
                },
                "extractor": {
                    #   "modules": [f"{extractor.galleryName}"], The modules option slows gallery-dl down upon start
                    extractor.galleryName: {
                        "filename": "NoFilenameSet",
                        "directory": {"": [""]},
                        "extension-map": {
                            "jpeg": "jpg",
                            "jpe": "jpg",
                            "jfif": "jpg",
                            "jif": "jpg",
                            "jfi": "jpg",
                            ".htm": ".html",
                            ".tif": ".tiff",
                            ".yml": ".yaml",
                            ".mpg": ".mpeg",
                            ".aif": ".aiff",
                            ".text": ".txt",
                            ".mdown": ".md",
                            ".markdown": ".md",
                        },
                        "sleep": [sleepTime, sleepTime + sleepOffset],
                        "sleep-extractor": [
                            sleepTime,
                            sleepTime + sleepOffset,
                        ],
                        "sleep-request": [sleepTime, sleepTime + sleepOffset],
                        "input": False,
                        "cookies": extractor.getCookiesPath(),
                        "retries": -1,
                        "postprocessors": [
                            {
                                "name": "metadata",
                                "mode": "json",
                                "private": True,
                                "directory": "metadata",
                                "skip": True,
                                "event": "post",
                                "mtime": True,
                                "filename": "NoFilenameSet",
                            }
                        ],
                    }
                },
            }
            if generalSettings["extendedmetadata"]:
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["http-metadata"] = "_http"
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["version-metadata"] = "_gallery-dl"
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["url-metadata"] = "_url"
        except Exception as e:
            raise

    def getBaseConf(self, user):
        try:
            #   Needed because dependent on user
            if user["DestinationPath"] != "default":
                destination = user["DestinationPath"]
            else:
                destination = f"{self.extSettings['defaultpath']}/{user['UserHandle']}"

            self.jobBaseConfig["extractor"][self.extractor.galleryName]["base-directory"] = destination
            if not self.generalSettings["nosqlcreation"]:
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["archive"] = f"{destination}/{user['UserHandle']}.sql"

            return self.jobBaseConfig
        except Exception:
            raise

    def getPrefix(self) -> str:
        return "g-dl"

    def deepUpdate(self, original, update):
        for key, value in update.items():
            #   If the key is another dict and it's present in the original dict, run the function again
            if isinstance(value, dict) and key in original and isinstance(original[key], dict):
                self.deepUpdate(original[key], value)

            #   If the key is a list of dict and it's present in the original dict, run the function again
            elif isinstance(value, list) and key in original and isinstance(original[key], list):
                #   Run for every entry in the list, if it contains another dict then run the function again on that dict
                for i, item in enumerate(value):
                    if i < len(original[key]):
                        if isinstance(item, dict) and isinstance(original[key][i], dict):
                            self.deepUpdate(original[key][i], item)
                        else:
                            #   Assign
                            original[key][i] = item
                    else:
                        #   Assign
                        original[key].append(item)
            else:
                #   Assign
                original[key] = value

    def writeConfig(self, data, path):
        with open(path, "w") as file:
            json.dump(data, file)

    def getPath(self) -> str:
        return os.path.join(self.extractor.main.toolsPath, "gallery-dl.exe")

    def getArguments(self, extractor: "Extractor", user: dict, url: str) -> str:
        _userExtractedDate = Gallerydl.toDate(int(user["LastExtracted"]))
        _argDateFilter = ""
        if not extractor.inhibitUnixUpdate:
            parts = [*extractor.filterAppend, f"date >= datetime({_userExtractedDate})", "abort()"]
            filterStr = " or ".join(parts)
            _argDateFilter = f'--filter "{filterStr}"'

        return f'"{url}" --no-input -v --config "{extractor.runningConfigFPath}" {extractor.argsAppend} {_argDateFilter}'

    @staticmethod
    def toDate(timestamp) -> str:
        dt = datetime.fromtimestamp(timestamp)
        return f"{dt.year}, {dt.month}, {dt.day}"

    def getCompiledPatterns(self) -> list[tuple[Pattern[str], dict[str, Any]]]:
        return self.compiledPatterns

    def getName(self) -> str:
        return "gallery-dl"

    def makeJobsQuick(self, jobList, args) -> None:
        extractorName = args[0]
        for john in jobList:
            conf = john["config"]
            base = conf["extractor"][extractorName]
            for key in ["sleep", "sleep-extractor", "sleep-request"]:
                base[key] = [value / 3 for value in base[key]]
