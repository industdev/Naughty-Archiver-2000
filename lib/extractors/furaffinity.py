import copy
from typing import Any
from lib.ui.userTable_manager import Table
from lib.Enums import Configure, Validation, Widgets
from lib.extractors.ExtractorInterface import ExtractorInterface


class Furaffinity(ExtractorInterface):
    def __init__(self) -> None:
        self.extractorName = "Furaffinity"
        self.galleryName = "furaffinity"
        self.commonUserOptions = None
        self.filterAppend = ""
        self.argsAppend = ""
        self.sleepTime = 1
        self.cursorExtractionEnabled = False

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 2
        cookiesTextBoxText = [f"Insert your furaffinity 'a' token here, then hit 'Use this one!'", "Insert your furaffinity 'b' token here"]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = False
        errorListRegex = []
        errorListIdExtractRegex = ""
        errorListFullURL = ""

        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getExtractorUrls(self) -> list[str]:
        urls = [
            "furaffinity.net/%s",
            "furaffinity.net/gallery/%s",
            "furaffinity.net/gallery/%s/folder/%s",
            "furaffinity.net/user/%s",
            "furaffinity.net/search/?q=%s",
            "furaffinity.net/view/%s",
            "furaffinity.net/watchlist/by/%s",
            "furaffinity.net/msg/submissions",
            "t.furaffinity.net/%s",
        ]
        return urls

    def getUsertableTemplate(self):
        tableTemplate = [
            [Table.SHOW, Table.CHECKBOX, "Scraps", "Scraps", True, None],
        ]

        comboTemplate = []

        userIdentificationString = "User Handle"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        ui = [
            {
                Configure.NAME: "cfg_desctype",
                Configure.WIDGET: Widgets.COMBOBOX,
                Configure.KEY: "desctype",
                Configure.DEFAULT: 0,
                Configure.TOOLTIP: "Choose the format of extracted descriptions",
                Configure.LABEL: "Descriptions",
                Configure.ENTRIES: ["Text (plain)", "HTML"],
                Configure.VALIDATION: Validation.INTEGER,
            },
        ]
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main) -> tuple[list[Any], dict[str, Any]]:
        a = self.readFile(f"{extSettings['cookiespath']}")
        b = self.readFile(f"{extSettings['cookiespath']}_token")

        overrideConf = {
            "extractor": {
                self.galleryName: {
                    "filename": "\fM ./external/logic/furVariablesNormal.py:getNormal",
                    "cookies": {"a": a, "b": b},
                    "directory": {"scraps": ["scraps"], "": ""},
                    "postprocessors": [{"filename": "\fM ./furVariablesNormal.py:getNormal_Postprocessor"}],
                }
            }
        }
        fullBaseConf = copy.deepcopy(baseConf)
        deepUpdate(fullBaseConf, overrideConf)

        if user["Scraps"]:
            fullBaseConf["extractor"][self.galleryName]["include"] = ["scraps", "gallery"]
        else:
            fullBaseConf["extractor"][self.galleryName]["include"] = ["gallery"]

        if extSettings["desctype"]:
            fullBaseConf["extractor"][self.galleryName]["descriptions"] = "text"
        else:
            fullBaseConf["extractor"][self.galleryName]["descriptions"] = "html"

        jobs = []

        config = self._furaffinity_baseConfig(user, fullBaseConf)
        jobs.append(config)
        return jobs, self.defaultJob(user, fullBaseConf)

    def _furaffinity_baseConfig(self, user, base_config):
        config = copy.deepcopy(base_config)

        return {"url": f"https://www.furaffinity.net/gallery/{user['UserHandle']}", "config": config, "type": f"gallery"}

    def readFile(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def defaultJob(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": None, "config": config, "type": None}
