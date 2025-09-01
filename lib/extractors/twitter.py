import os
import sys
from typing import Any
from PySide6.QtGui import QGuiApplication
from lib.extractors.ExtractorTemplate import ExtractorInterface
from lib.ui.UserTable_manager import Table
from lib.Enums import Configure, Widgets

import copy


class Twitter(ExtractorInterface):
    def __init__(self):
        #   Extractor settings
        self.extractorName = "Twitter"
        self.galleryName = "twitter"
        self.commonUserOptions = ["IncludeTweets", "IncludeMedia"]
        self.filterAppend = "retweet_id or quote_id or reply_id or subcategory == 'avatar' or subcategory == 'banner' or "
        self.argsAppend = ""
        self.cursorExtractionEnabled = True
        self.sleepTime = 5

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        cookiesTextBoxType = 0
        cookiesTextBoxText = [f"Insert your {self.extractorName.lower()} cookies, and hit 'Use this one!'"]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        errorListEnabled = True
        errorListRegex = [
            r"\('([^']*)'\)"  #     For messages in parentheses and quotes
            # r"\(deleted\)"        #     Literal (deleted) too many small id posts!!!
        ]
        errorListIdExtractRegex = r"\b\d{6,}\b"
        errorListFullURL = "twitter.com/i/status/%s/"
        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        append = [
            {
                "MATCH": "Rate limit exceeded",
                "MESSAGE_ON_ACTION": "Rate limit exceeded\nIncrease the sleep time to prevent your account from possibly getting suspended",
                "LINE_LEVEL": "RED",
                "INHIBIT_BOX": False,
                "ACTION": ["STOP", 1],
                "VERSION": "1.2",
            },
            {
                "MATCH": "AuthorizationError: (.+) blocked your account",
                "MESSAGE_ON_ACTION": "Setting the user to skip as you don't have access to this twitter account",
                "LINE_LEVEL": "YELLOW",
                "INHIBIT_BOX": False,
                "ACTION": ["SKIP_USER", 1],
                "EVENT": "USER_NOTFOUND",
                "VERSION": "1.2",
            },
            {
                "MATCH": "AuthorizationError: (.+) Tweets are protected",
                "MESSAGE_ON_ACTION": "Setting the user to skip as you don't have access to this twitter account",
                "LINE_LEVEL": "YELLOW",
                "INHIBIT_BOX": False,
                "ACTION": ["SKIP_USER", 1],
                "EVENT": "USER_NOTFOUND",
                "VERSION": "1.2",
            },
        ]
        return append

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[str], str]:
        tableTemplate = [
            [Table.SHOW, Table.COMBO, "Extraction Level", "ExtractionLevel", 1, None],
            [Table.SHOW, Table.CHECKBOX, "Deep Timeline", "DeepTimeline", False, None],
            [Table.SHOW, Table.CHECKBOX, "Text Tweets", "IncludeTweets", False, None],
            [Table.SHOW, Table.CHECKBOX, "Media", "IncludeMedia", True, None],
            [Table.SHOW, Table.CHECKBOX, "Retweets", "IncludeRetweets", False, None],
        ]
        comboTemplate = ["Profile", "Media", "Timeline", "Search", "Conversations"]
        userIdentificationString = "User Handle"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        #   Configure.WIDGET:           Widgets, Type of the widget to add
        #   Configure.KEY*:             String, Configuration key to update when the widget is interacted with
        #   Configure.DEFAULT:     Any value you want already in the widget (like have it already checked, or have text in it)
        #   Configure.LABEL*:           String, Text shown near the widget or if checkbox the text of the checkbox
        #   Configure.TOOLTIP*:         String, Text shown when hovering
        #   Configure.VALIDATION*:      Validation, Enum that corresponds to a function in VarHelper.py, it will check if the input of a text box is for example an invalid path, and it will skip saving the config if so
        #   Configure.FUNCTION*:        Function, The function to connect to from 2 different sources:
        #   Configure.PLACEHOLDER:      String, Textboxes only: Text shown inside textboxes when it's empty
        #   Configure.ENTRIES:          String[], Comboboxes only: Each string in the array will be put in the combobox
        #       When the extractor reads this dictionary it will instantiate the widgets in self.ui, the widgets will be named: f'{Configure.WIDGET}_{Configure.KEY}'
        ui = [
            {
                Configure.NAME: "cfg_convert",
                Configure.WIDGET: Widgets.COMBOBOX,
                Configure.KEY: "convertmp4",
                Configure.DEFAULT: 0,
                Configure.ENTRIES: ["No", "Convert and delete", "Convert and keep"],
                Configure.TOOLTIP: "Convert videos uploaded as GIFs on twitter\nif you select 'keep' it will keep the video file otherwise remove it \n 'No' means no conversion",
                Configure.LABEL: "Save twitter GIFs",
            },
            {
                Configure.NAME: "cfg_filename",
                Configure.WIDGET: Widgets.COMBOBOX,
                Configure.KEY: "filename",
                Configure.DEFAULT: 0,
                Configure.ENTRIES: ["NA2000 (New)", "Old"],
                Configure.TOOLTIP: "Select between old and new filenames, it's recommended you leave it at 'NA2000 (new)'",
                Configure.LABEL: "Output filenames",
            },
        ]
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main) -> tuple[list[Any], dict[str, Any]]:
        try:
            #   We do this to make extSettings global and not add arguments which is not allowed
            self.extSettings = extSettings

            if self.extSettings["filename"] == 1:
                moduleF = "\fM ./external/logic/twitterVariablesNormal.py:getFilenameTweetLegacy"
            else:
                moduleF = "\fM ./external/logic/twitterVariablesNormal.py:getFilenameTweet"

            if user["Cursor"] == "":
                cursorValue = True
            else:
                cursorValue = user["Cursor"]

            overrideConf = {
                "extractor": {
                    self.galleryName: {
                        "users": "twitter.com/{legacy[screen_name]}",
                        "cards": False,
                        "conversations": True,
                        "pinned": True,
                        "quoted": True,
                        "retweets": True,
                        "expand": True,
                        "text-tweets": True,
                        "unavailable": True,
                        "twitpic": True,
                        "unique": False,
                        "replies": "self",
                        "cursor": cursorValue,
                        "include": ["timeline", "tweets", "media", "replies"],
                        "filename": moduleF,
                        "directory": {
                            "quote_id   != 0": ["quotes"],
                            "retweet_id != 0": ["retweets"],
                            "reply_id != 0": ["replies"],
                            "author['id'] != user['id']": ["replies", "repliedto"],
                            "": "",
                        },
                    }
                }
            }
            fullBaseConf = copy.deepcopy(baseConf)
            deepUpdate(fullBaseConf, overrideConf)

            #   Legacy filename
            if self.extSettings["filename"] == 1:
                module = "\fM ./external/logic/twitterVariablesNormal.py:getPostprocessorTweetLegacy"
            else:
                module = "\fM ./external/logic/twitterVariablesNormal.py:getPostprocessorTweet"

            #   Put postprocessor
            fullBaseConf["extractor"]["twitter"]["postprocessors"][0]["filename"] = module
            #   IncludeTweets
            if not user["IncludeTweets"]:
                fullBaseConf["extractor"]["twitter"]["text-tweets"] = False

            #   IncludeMedia IncludeRetweets
            filters = []

            if not user["IncludeMedia"]:
                filters.append("width == 0")

            if not user["IncludeRetweets"]:
                filters.append("retweet_id == 0")
                fullBaseConf["extractor"]["twitter"]["retweets"] = False
                #   Metadata retweets?  There's no point in adding this because it will still download the metadata, so might aswell save it
                # overrideConf["extractor"]["twitter"]["postprocessors"][0]["filter"] = "retweet_id == 0"

            if filters:
                fullBaseConf["extractor"]["twitter"]["image-filter"] = " or ".join(filters)

            convert = extSettings["convertmp4"]

            if convert != 0:
                value = "keeping" if convert == 2 else "removing"
                command = "rem Naughty Archiver, please convert {_path} to GIF " + value + " the original"
                fullBaseConf["extractor"]["twitter"]["postprocessors"].append({
                    "name": "exec",
                    "filter": "type == 'animated_gif'",
                    "command": command,
                })

            #   Now define which jobs to pass to gallery-dl after these line

            jobs = []

            jobs.append(self._twitter_profileJob(user, fullBaseConf))
            jobs.extend(self._twitter_avatarbannerJob(user, fullBaseConf))

            level = user["ExtractionLevel"]
            if level == 1:
                jobs.append(self._twitter_mediaJob(user, fullBaseConf))
            if level >= 2:
                jobs.append(self._twitter_timelineJob(user, fullBaseConf))
                if user["DeepTimeline"]:
                    jobs.append(self._twitter_tweetsJob(user, fullBaseConf))
                    jobs.append(self._twitter_repliesJob(user, fullBaseConf))

            if level >= 3:
                jobs.append(self._twitter_searchJob(user, fullBaseConf))
            if level >= 4:
                jobs.extend(self._twitter_conversationJob(user, fullBaseConf))

            return jobs, self.defaultJob(user, fullBaseConf)
        except Exception as e:
            main.varHelper.exception(e)
            raise Exception(f"Error getting the jobs for {self.extractorName} (See cmd with CTRL+.): {e}")

    def _twitter_mediaJob(self, user, fullBaseConf):
        return {
            "url": f"https://x.com/{user['UserHandle']}/media",
            "config": copy.deepcopy(fullBaseConf),
            "type": "media",
        }

    def _twitter_timelineJob(self, user, fullBaseConf):
        return {
            "url": f"https://x.com/{user['UserHandle']}/timeline",
            "config": copy.deepcopy(fullBaseConf),
            "type": "timeline",
        }

    def _twitter_tweetsJob(self, user, fullBaseConf):
        return {
            "url": f"https://x.com/{user['UserHandle']}/tweets",
            "config": copy.deepcopy(fullBaseConf),
            "type": "tweets",
        }

    def _twitter_repliesJob(self, user, fullBaseConf):
        return {
            "url": f"https://x.com/{user['UserHandle']}/with_replies",
            "config": copy.deepcopy(fullBaseConf),
            "type": "replies",
        }

    def _twitter_searchJob(self, user, fullBaseConf):
        return {
            "url": f"https://x.com/search?q=from:{user['UserHandle']}",
            "config": copy.deepcopy(fullBaseConf),
            "type": "searches",
        }

    def _twitter_conversationJob(self, user, fullBaseConf):
        config_no_expand = copy.deepcopy(fullBaseConf)
        config_no_expand["extractor"]["twitter"]["sleep"][0] += 7
        config_no_expand["extractor"]["twitter"]["sleep"][1] += 7
        config_no_expand["extractor"]["twitter"]["sleep-request"][0] += 7
        config_no_expand["extractor"]["twitter"]["sleep-request"][1] += 7

        config_no_expand["extractor"]["twitter"].update({
            "expand": False,
            "replies": True,
            "directory": ["conversations"],
        })

        config_expand = copy.deepcopy(fullBaseConf)
        config_expand["extractor"]["twitter"]["sleep"][0] += 7
        config_expand["extractor"]["twitter"]["sleep"][1] += 7
        config_expand["extractor"]["twitter"]["sleep-request"][0] += 7
        config_expand["extractor"]["twitter"]["sleep-request"][1] += 7

        config_expand["extractor"]["twitter"].update({"expand": True, "replies": True, "directory": ["conversations"]})

        return [
            {
                "url": f"https://x.com/search?q=@{user['UserHandle']} filter:replies",
                "config": config_no_expand,
                "type": "conversations (First)",
            },
            {
                "url": f"https://x.com/search?q=@{user['UserHandle']} filter:replies",
                "config": config_expand,
                "type": "conversations (Last)",
            },
        ]

    def _twitter_avatarbannerJob(self, user, fullBaseConf):
        config = copy.deepcopy(fullBaseConf)

        #   Legacy filename
        if self.extSettings["filename"] == 1:
            module = "\fM ./external/logic/twitterVariablesNormal.py:getPostprocessorTweetLegacy"
        else:
            module = "\fM ./external/logic/twitterVariablesNormal.py:getPostprocessorAvatarOrBanner"

        #   Legacy filename
        if self.extSettings["filename"] == 1:
            moduleF = "\fM ./external/logic/twitterVariablesNormal.py:getFilenameTweetLegacy"
        else:
            moduleF = "\fM ./external/logic/twitterVariablesNormal.py:getFilenameAvatarOrBanner"

        config["extractor"]["twitter"].update({
            "filename": moduleF,
            "expand": False,
            "postprocessors": [
                {
                    "name": "metadata",
                    "mode": "json",
                    "private": True,
                    "directory": ["metadata"],
                    "skip": True,
                    "event": "post",
                    "filename": module,
                }
            ],
        })

        return [
            {"url": f"https://x.com/{user['UserHandle']}/header_photo", "config": config, "type": "banner"},
            {"url": f"https://x.com/{user['UserHandle']}/photo", "config": config, "type": "avatar"},
        ]

    def _twitter_profileJob(self, user, fullBaseConf):
        #   Legacy filename
        if self.extSettings["filename"] == 1:
            module = "\fM ./external/logic/twitterVariablesTransform.py:getPostprocessorUserprofile"
        else:
            module = "\fM ./external/logic/twitterVariablesTransform.py:getPostprocessorUserprofile"

        config = copy.deepcopy(fullBaseConf)
        config["extractor"]["twitter"].update({
            "archive": "",
            "logout": False,
            "conversations": False,
            "pinned": False,
            "quoted": False,
            "replies": False,
            "retweets": False,
            "expand": False,
            "strategy": "auto",
            "text-tweets": False,
            "unavailable": False,
            "twitpic": False,
            "videos": False,
            "ads": False,
            "cursor": False,
            "include": ["info"],
            "transform": False,
            "postprocessors": [
                {
                    "name": "metadata",
                    "mode": "json",
                    "private": True,
                    "directory": ["metadata"],
                    "skip": True,
                    "event": "post",
                    "filename": module,
                }
            ],
        })
        return {"url": f"https://x.com/{user['UserHandle']}", "config": config, "type": "profile"}

    def getExtractorUrls(self):
        urls = [
            "twitter.com/%s",
            "twitter.com/i/%s",
            "twitter.com/search?q=%s",
            "twitter.com/i/status/%s",
            "twitter.com/i/bookmarks",
            "twitter.com/i/lists/%s",
            "twitter.com/i/communities/%s",
            "twitter.com/i/events/%s",
            "twitter.com/%s/status/%s",
            "twitter.com/%s/highlights",
            "twitter.com/%s/likes",
            "twitter.com/%s/following",
            "twitter.com/%s/followers",
            "twitter.com/%s/info",
            "twitter.com/%s/photo",
            "twitter.com/%s/header_photo",
            "twitter.com/hashtag/%s",
            "twitter.com/home",
        ]

        return urls

    def copyLastCursor(self, value):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(value)

    def defaultJob(self, user, fullBaseConf):
        conf = copy.deepcopy(fullBaseConf)
        conf["extractor"]["twitter"].update({
            "replies": True,
            "expand": False,
            "include": "all",
        })
        conf["extractor"]["twitter"]["postprocessors"][0]["skip"] = False

        return {
            "url": None,
            "config": copy.deepcopy(conf),
            "type": None,
        }
