import copy
from typing import Any
from lib.ExtractorUsersTable import ExtractorUsersTable
from lib.Enums import Configure, Table
from lib.extractors.ExtractorInterface import ExtractorInterface


class Inkbunny(ExtractorInterface):
    def __init__(self):
        self.extractorName = "Inkbunny"
        self.galleryName = "inkbunny"
        self.commonUserOptions = None
        self.filterAppend = []
        self.argsAppend = ""
        self.sleepTime = 3

        self.cursorExtractionEnabled = False
        self.errorListEnabled = False

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 0
        cookiesTextBoxText = [
            f"Insert your {self.extractorName.lower()} cookies, and hit 'Use this one!\nIf you get cookie errors enable 'API External scripting' in inkbunny.net/account.php"
        ]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = False
        errorListRegex = []
        errorListIdExtractRegex = ""
        errorListFullURL = ""

        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        append = []
        return append

    def getExtractorUrls(self) -> tuple[list[str], list[str]]:
        urls = [
            "inkbunny.net/%s",
            "inkbunny.net/s/%s",
            "inkbunny.net/poolview_process.php?pool_id=%s",
            "inkbunny.net/userfavorites_process.php?favs_user_id=%s",
            "inkbunny.net/userfavorites_process.php?mode=watching&user_id=%s",
            "inkbunny.net/submissionsviewall.php?text=%s&mode=search&type=%s",
        ]
        return urls, ["inkbunny.net"]

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[list[str]], str]:
        tableTemplate = [
            [Table.SHOW, Table.CHECKBOX, "Scraps", "Scraps", False, None],
        ]

        comboTemplate = []

        userIdentificationString = "User Handle"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        ui = []
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main) -> tuple[list[Any], dict[str, Any]]:
        try:
            overrideConf = {
                "extractor": {
                    self.galleryName: {
                        "filename": "\fM ./external/logic/inkbunnyVariablesNormal.py:getNormal",
                        "directory": {"scraps": ["Scraps"], "": ""},
                        "postprocessors": [{"filename": "\fM ./inkbunnyVariablesNormal.py:getNormal_Postprocessor"}],
                    }
                }
            }

            #   It's required right after defining the options to override
            #   You can keep modifying the config after this
            fullBaseConf = copy.deepcopy(baseConf)
            deepUpdate(fullBaseConf, overrideConf)

            jobs = []

            jobs.append(self._inkbunny_galleryConfig(user, fullBaseConf))
            if user["Scraps"]:
                jobs.append(self._inkbunny_scrapsConfig(user, fullBaseConf))

            return jobs, self.defaultJob(user, fullBaseConf)
        except Exception as e:
            main.varHelper.exception(e, main.General.logger)
            raise Exception(f"Error getting the jobs for {self.extractorName}: {e}")

    def _inkbunny_galleryConfig(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": f"https://inkbunny.net/gallery/{user['UserHandle']}", "config": config, "type": f"gallery"}

    def _inkbunny_scrapsConfig(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": f"https://inkbunny.net/scraps/{user['UserHandle']}", "config": config, "type": f"scraps"}

    def defaultJob(self, user, base_config):
        config = copy.deepcopy(base_config)
        return {"url": None, "config": config, "type": None}

    def getRunnerChoice(self) -> int:
        return 0
