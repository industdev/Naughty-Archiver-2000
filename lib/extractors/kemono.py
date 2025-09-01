import copy
from typing import Any
from lib.ui.UserTable_manager import Table
from lib.Enums import Configure
from lib.extractors.ExtractorInterface import ExtractorInterface


class Kemono(ExtractorInterface):
    def __init__(self):
        self.extractorName = "Kemonoparty"
        self.galleryName = "kemono"
        self.commonUserOptions = None
        self.filterAppend = ""
        self.argsAppend = ""
        self.sleepTime = 3
        self.cursorExtractionEnabled = False

    def getExtractorUrls(self) -> list[str]:
        urls = [
            "kemono.cr/%s",
            "kemono.cr/%s/user/%s",
            "kemono.cr/discord/server/%s",
            "kemono.cr/account/favorites/artists",
            "kemono.cr/posts/%s",
            "kemono.cr/artists/%s",
        ]
        return urls

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

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        append = [
            {
                "MATCH": "NotFoundError",
                "MESSAGE_ON_LINE": "The item you were searching for was not found!",
                "LINE_LEVEL": "YELLOW",
                "INHIBIT_BOX": True,
                "VERSION": "1.2",
            }
        ]
        return append

    def getUsertableTemplate(self):
        tableTemplate = [
            [Table.SHOW, Table.COMBO, "Type", "urltype", 1, None],
            [Table.HIDE, Table.CHECKBOX, "File meta", "filemeta", False, None],
            [Table.SHOW, Table.CHECKBOX, "User meta", "usermeta", True, None],
            [Table.HIDE, Table.CHECKBOX, "Announcements", "announcements", True, None],
            [Table.HIDE, Table.CHECKBOX, "Revisions", "revisions", False, None],
            [Table.HIDE, Table.CHECKBOX, "Comments", "comments", False, None],
        ]

        comboTemplate = [
            "Discord Server",
            "Patreon.com",
            "Fanbox.cc",
            "Gumroad.com",
            "subscribestar.adult",
            "play.dlsite.com",
            "Fantia.jp",
            "Boosty.to",
            "Afdian.net",
        ]
        userIdentificationString = "Kemono ID"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        ui = []
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main):
        try:
            #   This function returns the list of jobs to pass to the gallery-dl configuration
            #   It is extractor dependent, it will overlap from the top:
            #       jobBaseConfig
            #       extBaseConfig
            #       userconfig
            #   The job configurations are based on the current user passed as argument

            overrideConf = {
                "extractor": {
                    self.galleryName: {
                        "filename": "\fM ./external/logic/kemonoVariablesNormal.py:getNormal",
                        "postprocessors": [{"filename": "\fM ./kemonoVariablesNormal.py:getNormal_Postprocessor"}],
                    }
                }
            }
            fullBaseConf = copy.deepcopy(baseConf)
            deepUpdate(fullBaseConf, overrideConf)

            fullBaseConf["extractor"][self.galleryName]["archives"] = user["filemeta"]
            fullBaseConf["extractor"][self.galleryName]["comments"] = user["comments"]
            fullBaseConf["extractor"][self.galleryName]["announcements"] = user["announcements"]

            if user["revisions"]:
                fullBaseConf["extractor"][self.galleryName]["revisions"] = "unique"
            else:
                fullBaseConf["extractor"][self.galleryName]["revisions"] = False

            jobs = []

            jobs.append(self._kemono_baseConfig(user, fullBaseConf))
            return jobs, self._kemono_baseConfig(user, fullBaseConf)
        except Exception as e:
            self.main.varHelper.exception(e)
            raise Exception(f"Error getting the jobs for {self.extractorName} (See cmd with CTRL+.): {e}")

    def _kemono_baseConfig(self, user, base_config):
        comboValues = self.getUsertableTemplate()[1]
        _typeindex = user["urltype"]
        urltype = comboValues[_typeindex]

        urlname = urltype.replace("play.", "")
        urlname = urlname.split(".")[0]
        urlname = urlname.lower()
        config = copy.deepcopy(base_config)
        if urltype == "Discord Server":
            url = f"https://kemono.cr/discord/server/{user['UserHandle']}"
        else:
            url = f"https://kemono.cr/{urlname}/user/{user['UserHandle']}"
        return {"url": url, "config": config, "type": f"{urlname}"}

    def defaultJob(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": None, "config": config, "type": None}
