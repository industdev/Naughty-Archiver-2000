from ctypes.wintypes import HANDLE
from datetime import datetime
import os
from re import Pattern
from typing import TYPE_CHECKING, Any
import tempfile

if TYPE_CHECKING:
    from lib.Extractor import Extractor, ExtractorEntry

from lib.runners.RunnerInterface import RunnerInterface
from lib.Enums import EventNames, Handlers, LogLevel


class Ytdlp(RunnerInterface):
    @staticmethod
    def searchReplace(array, old, new):
        for i, item in enumerate(array):
            if item == old:
                array[i] = new

    @staticmethod
    def modifyArgValue(array, flag, new):
        for i, arg in enumerate(array):
            if arg.startswith(flag):
                array[i] = f"{flag} {new}"
                break

    @staticmethod
    def stringToArgs(string) -> list[Any]:
        parts = string.split()
        args = []
        i = 0
        while i < len(parts):
            if parts[i].startswith("-") and i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                args.append(f"{parts[i]} {parts[i + 1]}")
                i += 2
            else:
                args.append(parts[i])
                i += 1
        return args

    def __init__(self, generalSettings, extractor: "Extractor"):
        try:
            self.extSettings = extractor.config.settings
            self.generalSettings = generalSettings
            self.extractor = extractor

            patterns = [
                {
                    Handlers.MATCH.name: r"rem Naughty Archiver, please timestamp",
                    Handlers.LINE_LEVEL.name: LogLevel.GREY.name,
                    Handlers.EVENT.name: EventNames.TIMESTAMP.name,
                },
                {Handlers.MATCH.name: r"^\[MoveFiles\]", Handlers.LINE_LEVEL.name: LogLevel.GREY.name},
                {Handlers.MATCH.name: r"^\[hls.*?\]", Handlers.LINE_LEVEL.name: LogLevel.GREY.name},
                {Handlers.MATCH.name: r"^\[debug\]", Handlers.LINE_LEVEL.name: LogLevel.GREY.name},
                {Handlers.MATCH.name: r"^\[info\]", Handlers.LINE_LEVEL.name: LogLevel.WHITE.name},
                {Handlers.MATCH.name: r"^\[error\]", Handlers.LINE_LEVEL.name: LogLevel.RED.name},
                {
                    Handlers.MATCH.name: "^(?!\\[).*",
                    Handlers.LINE_LEVEL.name: "GREY",
                    Handlers.INHIBIT_BOX.name: False,
                    Handlers.RUNNERMASK.name: "yt-dlp",
                },
            ]

            self.compiledPatterns = extractor.main.General.runnerHandlerCreator.compile(patterns, self)

            ffmpegLocation = os.path.join(extractor.main.toolsPath, "ffmpeg.exe")
            self.jobBaseConfig: list[str] = [
                "# coding: utf-8",
                "--mtime" if generalSettings["mtimeenabled"] else "-no-mtime",
                "--color no_color",
                "--ignore-config",  #  Ignore any config file in home directory
                "-4",  #  Force IPv4
                "-N 12",  #  Number of concurrent connections
                "--downloader aria2c",  #    Use aria2c
                f'--ffmpeg-location "{ffmpegLocation}"',
                "--ignore-no-formats-error",
                "--output-na-placeholder 'null'",
                "--no-progress",
                "--verbose",
                "--windows-filenames",
                "--encoding utf-8",
                '--postprocessor-args "ffmpeg_i1:-v warning"',
                '--postprocessor-args "ffmpeg_i1:-loglevel warning"',
                "--print-traffic",
                #  Placeholders
                "-f",
                "-o %(id)s_%(fulltitle)s.%(ext)s",
                "--dateafter 20000101"
                # Metadata
                "--embed-info-json",
                "--embed-metadata ",
                "--embed-thumbnail",
                "--embed-subs",
                "--write-info-json",
                "--write-playlist-metafiles",
                #   "--write-description", UNNECESSARY
                "--write-comments",
                f'--paths "temp:{tempfile.gettempdir()}"',
            ]
            if generalSettings["extendedmetadata"]:
                Ytdlp.searchReplace(self.jobBaseConfig, "--clean-info-json", "--no-clean-info-json")

        except Exception:
            raise

    def getPrefix(self) -> str:
        return "yt-dlp"

    def getPath(self) -> str:
        return os.path.join(self.extractor.main.toolsPath, "yt-dlp.exe")

    def getBaseConf(self, user) -> list[str]:
        try:
            config = self.jobBaseConfig.copy()

            #   Needed because dependent on user
            if user["DestinationPath"] != "default":
                destination = user["DestinationPath"]
            else:
                destination = f"{self.extSettings['defaultpath']}/{user['UserHandle']}"

            Ytdlp.modifyArgValue(config, "-P", f"'{destination}'")
            #   Minimum date is 20000101 because they decided so
            date = Ytdlp.toDate(max(946681200, int(user["LastExtracted"])))
            Ytdlp.modifyArgValue(config, "--dateafter", f"{date}")

            sleepTime = self.extSettings["sleeptime"]
            sleepOffset = self.generalSettings["sleepmodulate"]

            config.append(f'--paths "home:{destination}"')
            config.append(f"--sleep-requests {sleepTime}")
            config.append(f"--sleep-subtitles {sleepTime}")
            config.append(f"--min-sleep-interval {sleepTime}")
            config.append(f"--max-sleep-interval {sleepTime + sleepOffset}")
            config.append(f"--limit-rate {self.generalSettings['maxdlspeed']}k")
            config.append(
                f'--cookies "{self.extractor.getCookiesPath()}"',
            )

            if not self.generalSettings["nosqlcreation"]:
                config.append(f"--download-archive '{destination}/{user['UserHandle']}.sql'")
            return config

        except Exception:
            raise

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
            for d in data:
                if d != "":
                    file.write(d + "\n")

    def getArguments(self, extractor: "Extractor", user: dict, url: str) -> str:
        #   Todo: implement filters?
        #   _argDateFilter = ""
        #   if not extractor.inhibitUnixUpdate:
        #       parts = [*extractor.filterAppend]
        #       filterStr = " or ".join(parts)
        #       _argDateFilter = f'--filter "{filterStr}"'

        return f'"{url}" --ignore-config --config-locations "{extractor.runningConfigFPath}" {extractor.argsAppend}'

    @staticmethod
    def toDate(timestamp) -> str:
        dt = datetime.fromtimestamp(timestamp)
        return f"{dt.year:04d}{dt.month:02d}{dt.day:02d}"

    def getCompiledPatterns(self) -> list[tuple[Pattern[str], dict[str, Any]]]:
        return self.compiledPatterns

    def getName(self) -> str:
        return "Yt-Dlp"

    def makeJobsQuick(self, jobList, args) -> None:
        keys = [
            "--sleep-requests",
            "--sleep-subtitles",
            "--min-sleep-interval",
            "--max-sleep-interval",
        ]
        for john in jobList:
            conf = john["config"]

            for key in keys:
                Ytdlp.modifyArgValue(conf, key, "1")
