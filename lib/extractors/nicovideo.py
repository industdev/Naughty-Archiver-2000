import os
import sys
from typing import Any
from PySide6.QtGui import QGuiApplication
from lib.Extractor import Ytdlp
from lib.extractors.ExtractorTemplate import ExtractorInterface
from lib.ExtractorUsersTable import ExtractorUsersTable
from lib.Enums import Configure, Table, Widgets

import copy


class Nicovideo(ExtractorInterface):
    def __init__(self):
        #   Extractor settings
        self.extractorName: str = "Nicovideo"
        self.galleryName: str = "nicovideo"
        self.commonUserOptions: list[str] = []
        self.filterAppend: list[str] = []
        self.argsAppend: str = ""
        self.cursorExtractionEnabled: bool = False
        self.sleepTime: int = 5

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 0
        cookiesTextBoxText = [f"Insert your {self.extractorName.lower()} cookies, and hit 'Use this one!'"]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = False
        errorListRegex = []
        errorListIdExtractRegex = r"\b\d{6,}\b"
        errorListFullURL = "https://www.nicovideo.com/channel/%s/videos"
        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        append = [
            {
                "MATCH": "Extracting URL:",
                "LINE_LEVEL": "WHITE",
                "RUNNERMASK": "yt-dlp",
            },
            {
                "MATCH": "^\\[nico.*?\\]",
                "LINE_LEVEL": "GREY",
                "RUNNERMASK": "yt-dlp",
            },
        ]
        return append

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[list[str]], str]:
        tableTemplate = [
            [Table.SHOW, Table.COMBO, "Type", "type", 0, None],
            [Table.SHOW, Table.COMBO, "Quality", "quality", 0, None],
            [Table.SHOW, Table.CHECKBOX, "Video Metadata", "videoMetadata", False, None],
            [Table.SHOW, Table.CHECKBOX, "Fetch Comments", "comments", False, None],
        ]
        comboTemplate = [["User ID", "Mylist ID", "Series ID"], ["Merge Best", "Best", "360p", "Best audio only"]]
        userIdentificationString = "ID"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        #   Configure.WIDGET:           Widgets, Type of the widget to add
        #   Configure.KEY*:             String, Configuration key to update when the widget is interacted with
        #   Configure.DEFAULT:          Any value you want already in the widget (like have it already checked, or have text in it)
        #   Configure.LABEL*:           String, Text shown near the widget or if checkbox the text of the checkbox
        #   Configure.TOOLTIP*:         String, Text shown when hovering
        #   Configure.VALIDATION*:      Validation, Enum that corresponds to a function in VarHelper.py, it will check if the input of a text box is for example an invalid path, and it will skip saving the config if so
        #   Configure.FUNCTION*:        Function, The function to connect to from 2 different sources:
        #   Configure.PLACEHOLDER:      String, Textboxes only: Text shown inside textboxes when it's empty
        #   Configure.ENTRIES:          String[], Comboboxes only: Each string in the array will be put in the combobox
        #       When the extractor reads this dictionary it will instantiate the widgets in self.ui, the widgets will be named: f'{Configure.WIDGET}_{Configure.KEY}'
        ui = [
            {
                Configure.NAME: "cfg_arguments",
                Configure.WIDGET: Widgets.TEXTBOX,
                Configure.KEY: "arguments",
                Configure.DEFAULT: "",
                Configure.TOOLTIP: "Append these arguments to yt-dlp (Ex: '--add-header Test --no-mtime ')",
                Configure.LABEL: "Other arguments",
                Configure.PLACEHOLDER: "String (arguments)",
            },
            {
                Configure.NAME: "cfg_combo",
                Configure.WIDGET: Widgets.COMBOBOX,
                Configure.KEY: "lang",
                Configure.DEFAULT: 0,
                Configure.TOOLTIP: "Choose between japanese and english language during video extraction (Japanese is recommended)",
                Configure.LABEL: "Extraction language",
                Configure.ENTRIES: ["Japanese", "English"],
            },
            {
                Configure.NAME: "cfg_embedmetadata",
                Configure.WIDGET: Widgets.CHECKBOX,
                Configure.KEY: "embedmetadata",
                Configure.DEFAULT: False,
                Configure.TOOLTIP: "Embed the video metadata into the video file when possible",
                Configure.LABEL: "Embed metadata in video",
            },
        ]
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main) -> tuple[list[Any], dict[str, Any]]:
        try:
            self.extSettings = extSettings
            fullBaseConf = baseConf

            #   Don't write video metadata if not wanted
            if not user["videoMetadata"]:
                remove = [
                    "--write-info-json",  # Metadata
                    "--write-playlist-metafiles",  # Metadata
                ]

                for r in remove:
                    Ytdlp.searchReplace(fullBaseConf, r, "")

            #   Don't write comments if not wanted
            if not user["comments"]:
                Ytdlp.searchReplace(fullBaseConf, "--write-comments", "")

            #   Don't embed metadata if not wanted
            if not extSettings["embedmetadata"]:
                remove = [
                    "--embed-info-json",
                    "--embed-metadata",
                    "--embed-thumbnail",
                    "--embed-subs",
                ]

                for r in remove:
                    Ytdlp.searchReplace(fullBaseConf, r, "")

            #   Quality choice
            opts = [
                "bestvideo*+bestaudio/best",
                "b",
                "best[height=360]",
                "bestaudio",
            ]
            quality = opts[user["quality"]]
            Ytdlp.modifyArgValue(fullBaseConf, "-f", f"{quality}")

            #   Language
            if extSettings["lang"] == 0:
                fullBaseConf.append("--add-header 'Accept-Language:ja'")
            else:
                fullBaseConf.append("--add-header 'Accept-Language:en'")

            filenames = [
                #   Video subtitles
                "subtitle:metadata/nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s_sub",
                #   Video thumbnail
                "thumbnail:thumbnails/nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s",
                #   Video info
                "infojson:metadata/nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s",
                #   Single video metadata?
                "link:metadata/nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s",
                #   Single video?
                "pl_video:nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s",
                #   Playlist thumbnail?
                "pl_thumbnail:thumbnails/nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s",
                #   Playlist description
                "pl_description:metadata/nv_playlist_%(title)s_%(id)s",
                #   Playlist/channel info
                "pl_infojson:metadata/nv-ID%(id)s",
                #   Any video, pl_link is treated as a folder
                "nv_%(uploader)s-ID%(uploader_id)s_%(fulltitle)s-%(id)s_%(playlist_index)s",
            ]

            for filename in filenames:
                fullBaseConf.append(f'-o "{filename}" ')

            fullBaseConf.extend(Ytdlp.stringToArgs(extSettings["arguments"]))

            if user["type"] == 0:
                self.baseUrl = "https://www.nicovideo.jp/user/"
            elif user["type"] == 1:
                self.baseUrl = "https://www.nicovideo.jp/mylist/"
            else:
                self.baseUrl = "https://www.nicovideo.jp/series/"
            jobs = []

            jobs.append(self._niconico_channelJob(user, fullBaseConf))

            return jobs, self.defaultJob(user, fullBaseConf)
        except Exception as e:
            main.varHelper.exception(e)
            raise Exception(f"Error getting the jobs for {self.extractorName} , check the latest exception file: {e}")

    def _niconico_channelJob(self, user, fullBaseConf):
        return {
            "url": f"{self.baseUrl}{user['UserHandle']}",
            "config": copy.deepcopy(fullBaseConf),
            "type": "channel",
        }

    def defaultJob(self, user, fullBaseConf):
        return {
            "url": f"{self.baseUrl}{user['UserHandle']}",
            "config": copy.deepcopy(fullBaseConf),
            "type": "channel",
        }

    def getRunnerChoice(self) -> int:
        return 1

    def getExtractorUrls(self) -> tuple[list[str], list[str]]:
        return [
            "nicovideo.jp/%s",
            "nicovideo.jp/watch/%s",
            "nicovideo.jp/user/%s/mylist/%s",
            "nicovideo.jp/my/history/video",
            "ch.nicovideo.jp/channel/%s",
        ], ["nicovideo.jp", "ch.nicovideo.jp", "nico.ms"]
