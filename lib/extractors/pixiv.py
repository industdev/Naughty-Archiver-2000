import copy
from typing import Any
from lib.Configurator import Widgets
from lib.Enums import Configure, Validation
from lib.VarHelper import VarHelper
from lib.ui.userTable_manager import Table
from lib.extractors.ExtractorInterface import ExtractorInterface
import os


class Pixiv(ExtractorInterface):
    def __init__(self) -> None:
        self.extractorName = "Pixiv"
        self.galleryName = "pixiv"
        self.commonUserOptions = None
        self.filterAppend = "subcategory == 'avatar' or subcategory == 'banner' or "
        self.argsAppend = ""
        self.cursorExtractionEnabled = False
        self.sleepTime = 3

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 1
        cookiesTextBoxText = [
            f"Insert your pixiv cookies here then hit 'Use this one!'",
            f"Click the 'Oauth' button, and insert your pixiv refresh token here",
        ]
        cookiesShowPixivOauthButton = True

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = False
        errorListRegex = []
        errorListIdExtractRegex = ""
        errorListFullURL = ""

        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getExtractorUrls(self) -> list[str]:
        #   Define an array of strings where '%s' will be replaced by the user input, this will be used for the custom urls page
        #   It should be None if you don't want this functionality
        urls = [
            "pixiv.net/%s",
            "pixiv.net/artworks/%s",
            "pixiv.net/users/%s",
            "pixiv.net/users/%s/bookmarks/artworks",
            "pixiv.net/users/%s/novels",
            "pixiv.net/user/%s/series/%s",
            "pixiv.net/novel/series/%s",
            "pixiv.net/artworks/unlisted/%s",
            "pixiv.net/tags/%s",
            "pixiv.net/ranking.php",
        ]
        return urls

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[str], str]:
        tableTemplate = [[Table.SHOW, Table.CHECKBOX, "Novels", "IncludeNovels", False, None]]

        comboTemplate = []

        userIdentificationString = "User ID"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        ui = [
            {
                Configure.NAME: "cfg_ugoiraFormat",
                Configure.WIDGET: Widgets.COMBOBOX,
                Configure.KEY: "ugoiraformat",
                Configure.DEFAULT: 0,
                Configure.TOOLTIP: "Convert the ugoira animation to a viewable format",
                Configure.LABEL: "Convert ugoira to",
                Configure.ENTRIES: ["No conversion", "GIF (Inaccurate)", "WEBM", "MKV"],
                Configure.VALIDATION: Validation.INTEGER,
            },
            {
                Configure.NAME: "cfg_ugoiraKeep",
                Configure.WIDGET: Widgets.CHECKBOX,
                Configure.KEY: "ugoirakeep",
                Configure.DEFAULT: True,
                Configure.TOOLTIP: "If disabled frames of ugoira files will be saved as normal images",
                Configure.LABEL: "Move ugoira frames to zip",
                Configure.VALIDATION: Validation.BOOLEAN,
            },
            {
                Configure.NAME: "cfgui_novelSeries",
                Configure.WIDGET: Widgets.CHECKBOX,
                Configure.KEY: "novelseries",
                Configure.DEFAULT: False,
                Configure.TOOLTIP: "When downloading a novel being part of a series, download all novels of that series",
                Configure.LABEL: "Download novel full series",
                Configure.VALIDATION: Validation.BOOLEAN,
            },
            {
                Configure.NAME: "cfg_novelComments",
                Configure.WIDGET: Widgets.CHECKBOX,
                Configure.KEY: "novelcomments",
                Configure.DEFAULT: False,
                Configure.TOOLTIP: "Fetch comments metadata\nNote: This requires 1 or more additional API requests per novel, depending on the number of comments",
                Configure.LABEL: "Fetch novel comments",
                Configure.VALIDATION: Validation.BOOLEAN,
            },
        ]
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main) -> tuple[list[Any], dict[str, Any]]:
        try:
            token = self.readFile(f"{extSettings['cookiespath']}_token")

            if extSettings["ugoiraformat"] == 0:
                ugoiraExtension = None
                demuxer = None
            elif extSettings["ugoiraformat"] == 1:
                ugoiraExtension = "gif"
                demuxer = "concat"
            elif extSettings["ugoiraformat"] == 2:
                ugoiraExtension = "webm"
                demuxer = "mkvmerge"
            elif extSettings["ugoiraformat"] == 3:
                ugoiraExtension = "mkv"
                demuxer = "mkvmerge"

            overrideConf = {
                "extractor": {
                    "postprocessors": [
                        #   Convert to video
                        {
                            "name": "ugoira",
                            "extension": ugoiraExtension,
                            "ffmpeg-demuxer": demuxer,
                            "ffmpeg-location": os.path.join(main.toolsPath, "ffmpeg.exe"),
                            "mkvmerge-location": os.path.join(main.toolsPath, "mkvmerge.exe"),
                            "whitelist": ["pixiv", "danbooru"],
                            "keep-files": False,
                        },
                        #   Save to zip
                        {
                            "name": "ugoira",
                            "ffmpeg-demuxer": "archive",
                            "whitelist": ["pixiv", "danbooru"],
                            "keep-files": False,
                        },
                    ],
                    self.galleryName: {
                        "filename": "\fM ./external/logic/pixivVariablesNormal.py:getNormal",
                        "refresh-token": token,
                        "include": [
                            "avatar",
                            "background",
                            "artworks",
                        ],
                        "metadata": True,
                        "captions": True,
                        "tags": "original",
                        "ugoira": "original",
                        "directory": {"subcategory == 'novel-series'": "novels", "": ""},
                        "postprocessors": [{"filename": "\fM ./pixivVariablesNormal.py:getNormal_Postprocessor"}],
                    },
                }
            }
            #   It's required right after defining the options to override
            #   You can keep modifying the config after this
            fullBaseConf = copy.deepcopy(baseConf)
            deepUpdate(fullBaseConf, overrideConf)

            #   If format is 0 then we keep the original frames as individual files and don't convert
            if extSettings["ugoiraformat"] == 0:
                fullBaseConf["extractor"]["postprocessors"][0] = {}
            elif extSettings["ugoiraformat"] == 1:
                fullBaseConf["extractor"]["postprocessors"][0]["ffmpeg-demuxer"] = "auto"
                fullBaseConf["extractor"]["postprocessors"][0]["ffmpeg-args"] = [
                    "-filter_complex",
                    "split[s0][s1];[s0]palettegen=stats_mode=full[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                    "-qscale:v",
                    "1",
                    "-compression_level",
                    "9",
                ]

            #   If we don't want ugoira ZIP files then we remove the postprocessor
            if not extSettings["ugoirakeep"]:
                fullBaseConf["extractor"]["postprocessors"][1] = {}

            if user["IncludeNovels"]:
                fullBaseConf["extractor"][self.galleryName]["include"] = ["avatar", "background", "artworks", "novel-user"]
                fullBaseConf["extractor"][self.galleryName]["novel"] = {}
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["refresh-token"] = token
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["covers"] = True
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["embeds"] = True
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["tags"] = "original"
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["full-series"] = extSettings["novelseries"]
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["metadata"] = True
                fullBaseConf["extractor"]["pixiv-novel"]["novel"]["comments"] = extSettings["novelcomments"]

            jobs = []
            jobs.append(self._pixiv_baseConfig(user, fullBaseConf))

            return jobs, self.defaultJob(user, fullBaseConf)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Error getting the jobs for {self.extractorName}: {e}")

    def _pixiv_baseConfig(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": f"https://pixiv.net/users/{user['UserHandle']}", "config": config, "type": "illustrations"}

    def readFile(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def defaultJob(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": None, "config": config, "type": None}
