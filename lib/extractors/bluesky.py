import copy
from typing import Any
from lib.Enums import Configure, Table
from lib.extractors.ExtractorInterface import ExtractorInterface


class Bluesky(ExtractorInterface):
    def __init__(self):
        self.extractorName = "Bluesky"
        self.galleryName = "bluesky"
        self.commonUserOptions = ["IncludeSkies", "IncludeMedia"]
        self.filterAppend = "subcategory == 'avatar' or subcategory == 'banner' or "
        self.argsAppend = ""
        self.cursorExtractionEnabled = False
        self.sleepTime = 3

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = False
        errorListRegex = []
        errorListIdExtractRegex = ""
        errorListFullURL = ""
        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getExtractorUrls(self) -> tuple[list[str], list[str]]:
        urls = [
            "bsky.app/%s",
            "bsky.app/profile/%s",
            "bsky.app/profile/%s/feed/%s",
            "bsky.app/profile/%s/lists/%s",
            "bsky.app/profile/%s/post/%s",
            "bsky.app/profile/%s/info",
            "bsky.app/profile/%s/follows",
            "bsky.app/search?q=%s",
            "bsky.app/hashtag/%s",
        ]
        return urls, ["bsky.app"]

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        append = []
        return append

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 0
        cookiesTextBoxText = [f"Insert your {self.extractorName.lower()} cookies, and hit 'Use this one!'"]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[list[str]], str]:
        tableTemplate = [
            [Table.SHOW, Table.COMBO, "Extraction Level", "ExtractionLevel", 1, None],
            [Table.SHOW, Table.CHECKBOX, "Skies", "IncludeSkies", False, None],
            [Table.SHOW, Table.CHECKBOX, "Media", "IncludeMedia", True, None],
        ]

        comboTemplate = [["Profile", "Normal"]]
        userIdentificationString = "Full User Handle"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        ui = []
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main):
        try:
            overrideConf = {
                "extractor": {
                    self.galleryName: {
                        "metadata": ["facets", "user"],
                        "filename": "\fM ./external/logic/blueskyVariablesNormal.py:getNormal",
                        "quoted": True,
                        "reposts": True,
                        "include": ["replies", "media", "video", "posts"],
                        "directory": {"author['did'] != user['did']": ["reposts"], "": [""]},
                        "postprocessors": [{"filename": "\fM ./external/logic/blueskyVariablesNormal.py:getNormal_Postprocessor"}],
                    }
                }
            }

            fullBaseConf = copy.deepcopy(baseConf)
            deepUpdate(fullBaseConf, overrideConf)

            if not user["IncludeSkies"]:
                fullBaseConf["extractor"]["bluesky"]["include"] = ["media", "video"]

            if not user["IncludeMedia"]:
                fullBaseConf["extractor"]["bluesky"]["include"] = ["media", "video", "replies", "posts"]
                fullBaseConf["extractor"]["bluesky"]["image-filter"] = "width == 0"

            jobs = []

            jobs.append(self._bluesky_profileJob(user, fullBaseConf))

            if user["ExtractionLevel"] >= 1:
                jobs.append(self._bluesky_normalJob(user, fullBaseConf))

            return jobs, self._bluesky_normalJob(user, fullBaseConf)
        except Exception as e:
            main.varHelper.exception(e)
            raise Exception(f"Error getting the jobs for {self.extractorName}: {e}")

    def _bluesky_profileJob(self, user, base_config):
        config = copy.deepcopy(base_config)

        config["extractor"]["bluesky"].update({
            "include": ["info", "avatar", "background"],
            "filename": "\fM ./external/logic/blueskyVariablesNormal.py:getUserprofile",
            "postprocessors": [
                {
                    "name": "metadata",
                    "mode": "json",
                    "private": "true",
                    "directory": ["metadata"],
                    "skip": True,
                    "event": "post",
                    "filename": "\fM ./blueskyVariablesNormal.py:getUserprofile_Postprocessor",
                }
            ],
        })

        return {"url": f"https://bsky.app/profile/{user['UserHandle']}", "config": config, "type": "profile, avatar, banner"}

    def _bluesky_normalJob(self, user, base_config):
        config = copy.deepcopy(base_config)

        config["extractor"]["bluesky"].update({
            "filename": "\fM ./external/logic/blueskyVariablesNormal.py:getNormal",
            "postprocessors": [
                {
                    "name": "metadata",
                    "mode": "json",
                    "private": "true",
                    "directory": ["metadata"],
                    "skip": True,
                    "event": "post",
                    "filename": "\fM ./external/logic/blueskyVariablesNormal.py:getNormal_Postprocessor",
                }
            ],
        })
        return {"url": f"https://bsky.app/profile/{user['UserHandle']}", "config": config, "type": "timeline"}

    def defaultJob(self, user, base_config):
        pass

    def getRunnerChoice(self) -> int:
        return 0
