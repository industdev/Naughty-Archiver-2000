import copy
from typing import Any
from lib.Enums import Configure
from lib.extractors.ExtractorInterface import ExtractorInterface


class Itaku(ExtractorInterface):
    def __init__(self):
        self.extractorName = "Itaku"
        self.galleryName = "itaku"
        self.commonUserOptions = None
        self.filterAppend = []
        self.argsAppend = None
        self.sleepTime = 3

        self.cursorExtractionEnabled = False
        self.errorListEnabled = False

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 0
        cookiesTextBoxText = [f"Insert your {self.extractorName.lower()} cookies, and hit 'Use this one!'"]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = False
        errorListRegex = []
        errorListIdExtractRegex = ""
        errorListFullURL = ""

        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getExtractorUrls(self) -> tuple[list[str], list[str]]:
        urls = [
            "itaku.ee/%s",
            "itaku.ee/images/%s",
            "itaku.ee/posts/%s",
            "itaku.ee/profile/%s",
            "itaku.ee/profile/%s/gallery",
            "itaku.ee/profile/%s/posts",
            "itaku.ee/profile/%s/stars",
            "itaku.ee/profile/%s/bookmarks/image/%s",
            "itaku.ee/home/images?tags=%s",
        ]
        return urls, ["itaku.ee"]

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        append = []
        return append

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[list[str]], str]:
        tableTemplate = []
        comboTemplate = [[]]

        userIdentificationString = "User Handle"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        ui = []
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main):
        overrideConf = {
            "extractor": {
                self.galleryName: {
                    "filename": "\fM ./external/logic/itakuVariablesNormal.py:getNormal",
                    "postprocessors": [{"filename": "\fM ./itakuVariablesNormal.py:getNormal_Postprocessor"}],
                }
            }
        }
        #   It's required right after defining the options to override
        #   You can keep modifying the config after this
        fullBaseConf = copy.deepcopy(baseConf)
        deepUpdate(fullBaseConf, overrideConf)

        jobs = []

        jobs.append(self._itaku_baseConfig(user, overrideConf))
        return jobs, self.defaultJob(user, overrideConf)

    def _itaku_baseConfig(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": f"https://itaku.ee/profile/{user['UserHandle']}/gallery", "config": config, "type": f"gallery"}

    def defaultJob(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": None, "config": config, "type": None}

    def getRunnerChoice(self) -> int:
        return 0
