#   This class is an example and tutorial to use to setup settings for a custom extractor
#   Do not rename variables, functions, add/remove arguments in your extractor
#   If you want to share a variable between functions use class variables (self.variable = foo)
#   If you find anything confusing take a look at the already-made extractors py files
#   Remember that most of the existing widgets in the template are already setup for you, anything you need or want to add should be added manually

#   Don't forget to import these modules
import copy
from typing import Any
from lib.ui.UserTable_manager import Table
from lib.Enums import Configure, Validation, Widgets
from lib.extractors.ExtractorInterface import ExtractorInterface


#   Rename the class to your liking but keep ExtractorInterface
class ExtractorTemplate(ExtractorInterface):
    def __init__(self) -> None:
        #   Mandatory: define the settings of the extractor, if you are unsure you can leave options without '*' to none
        #       extractorName (String)*:
        #           The extractor's name (also tab's)
        #       galleryName (String)*:
        #           The extractor's name in a gallery-dl configuration
        #       commonUserOptions (String[]):
        #           Defines options that can't be the same in the userTable (like 'nomedia' and 'notweets' simultaneously)
        #       filterAppend (String):
        #           Defines what to append on the --filter argument when gallery-dl is called
        #           it's used to stop extraction when a certain date is reached by default
        #           however other things like pinned posts may have an older date but still want to be included
        #           the filterAppend will be reloaded for each job, so it can be dynamic
        #           Ex: "retweet_id or reply_id or subcategory == 'avatar' or subcategory == 'banner' or"
        #               This will ignore stopping the extraction at any posts that's a retweet or a reply or banner or avatar
        #               It will automatically append 'date >= datetime({unix}) or abort()' based on the user unix value
        #       argsAppend (String):
        #           Append some more arguments to the command
        #       cursorExtractionEnabled(Bool):
        #           Enable cursor extraction and managing based on output, only available for instagram and twitter
        #       sleepTime(Int):
        #           Default value for sleep

        self.extractorName = "Test"
        self.galleryName = "test"
        self.commonUserOptions = ["One", "Two"]
        self.filterAppend = "Test1 or Test2 "
        self.argsAppend = "Test1 or Test2 "
        self.cursorExtractionEnabled = False
        self.sleepTime = 4

    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        #   Mandatory: define the settings for the cookies menu
        #       cookiesTextBoxType* (int):
        #           Defines the kind of textbox the cookie table should have (useful when extractors ask you for multiple cookies)
        #           0:  Normal textbox with 1 value to input
        #           1:  Two textboxes (one is thin)
        #           2:  Two textboxes (both same size)
        #       cookiesTextBoxText* (String[]):
        #           Defines the text to show in the cookie textboxes preview
        #       cookiesShowPixivOauthButton* (Bool):
        #           Shows a button to run Pixiv's Oauth

        cookiesTextBoxType = 0
        cookiesTextBoxText = [f"Insert your {self.extractorName.lower()} cookies, and hit 'Use this one!'"]
        cookiesShowPixivOauthButton = False

        return cookiesTextBoxType, cookiesTextBoxText, cookiesShowPixivOauthButton

    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        #   Optional: define patterns to watch in the gallery-dl output so to put them into the errored urls list, set errorListEnabled to false if you don't want to use this
        #       errorListEnabled* (bool):
        #           Enable the error lister menu (if false everything else is ignored)
        #       errorListRegex (Str[]):
        #           For every line of the output it will look for every regex in the array, and will extract that part if it's found and put it on the right as the error message
        #       errorListIdExtractRegex (Str):
        #           Regex that extracts the ID of the post that errored from that same line, triggered by errorListRegex
        #       errorListFullURL (Str):
        #           Replaced %s with the status id extracted from errorListIdExtract to put it on the left side of the errored urls table, as the actual full url

        #   Any text between (' & ') is an error message
        errorListEnabled = True
        errorListRegex = [
            r"\('([^']*)'\)",
        ]
        #   Skipping 8662361832117276043 (deleted) matches 8662361832117276043
        errorListIdExtractRegex = r"\b\d{6,}\b"
        #   build extractor.com/status/8662361832117276043/
        errorListFullURL = "extractor.com/status/%s/"

        return errorListEnabled, errorListRegex, errorListIdExtractRegex, errorListFullURL

    def getExtractorUrls(self) -> list[str]:
        #   Define an array of strings where '%s' will be replaced by the user input, this will be used for the custom urls page
        #   It should be None if you don't want this functionality
        urls = ["extractor.com/%s", "extractor.com/search?q=%s", "extractor.com/i/status/%s"]
        return urls

    def getOutputHandlingCases(self) -> list[dict[str, Any]]:
        #   Optional: Append to the top of the output manager table more handling cases specifically tied to this extractor
        #   They have the same format as the ones in /external/defaultOutputPatterns.json
        #   You may create them using the manager and copy each entry in here

        append = [
            {
                "MATCH": "AuthorizationError: (.+) Tweets are protected",
                "MESSAGE_ON_ACTION": "Setting the user to skip as you don't have access to this twitter account",
                "LINE_LEVEL": "YELLOW",
                "INHIBIT_BOX": False,
                "ACTION": ["SKIP_USER", 1],
                "EVENT": "USER_NOTFOUND",
                "VERSION": "1.2",
            }
        ]
        return append

    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[str], str]:
        #   Stores information to create user tables of different extractors
        #   Each entry in the matrix describes what the row holds, inside the rows there's what each column will have
        #       0:Show on Addtable (Shows the option in the smaller table when adding an user to not make it too cluttered, use Table.SHOW or Table.HIDE)
        #       1:Widget type
        #           Table.CHECKBOX
        #           Table.COMBO
        #           Table.TEXTBOX
        #       2:Header Title (Title of the column)
        #       3:Json KEY name (The key name that will be loaded and saved for it, reference from 'getConfigTemplate')
        #       4:Default value
        #       5:Check (blocks the user from saving invalid settings: see VarHelper.py)
        #   Fully modular :)

        tableTemplate = [
            #   Checkbox that changes key 'DeepTimeline' in the user Data
            [Table.SHOW, Table.CHECKBOX, "Deep Timeline", "DeepTimeline", False, None],
            #   Combobox that defines 'importance'
            [Table.SHOW, Table.COMBO, "Importance Level", "importance", 2, None],
            #   Hidden Textbox that defines 'append' and that can't be empty
            [Table.HIDE, Table.TEXTBOX, "Append to filename", "append", "original", Validation.EMPTY],
        ]

        #   Define every level/element in the combobox in your table
        #   Required if any of the columns have comboboxes
        #   If you need more than 1 combobox i may implement it
        comboTemplate = ["First option", "Second option"]

        #       userIdentificationString(String):
        #           Text to show as the type of username needed in the column, example: 'User Handle', 'User short ID', 'Gallery number'
        userIdentificationString = "User name"

        return tableTemplate, comboTemplate, userIdentificationString

    def getUiConfiguration(self, extractor, main) -> list[dict[Configure, Any]]:
        #   Define the connections of the widgets to functions and the extractor config in an array of dictionaries, each entry is a widget
        #   Widgets+signal supported: Buttons.clicked, Checkboxes.stateChanged, GroupBoxes.toggled, TextBox.editingFinished, ComboBox.currentIndexChanged
        #   Here you also define which keys the widgets are connected to
        #   By default no widget is needed

        #   Configure.NAME*             String, Widget name in the class (like btn_setUsers or cfg_argumentAppend), respect python's format
        #   Configure.WIDGET*:          Widgets, Type of the widget to add
        #                                   Widgets.CHECKBOX
        #                                   Widgets.TEXTBOX
        #                                   Widgets.COMBOBOX
        #                                   Widgets.BUTTON
        #   Configure.KEY:              String, Configuration key to update when the widget is interacted with
        #   Configure.DEFAULT*:         Any value you want already in the widget (like have it already checked, or have text in it, use to put text in buttons)
        #   Configure.LABEL:            String, Text shown near the widget or if checkbox the text of the checkbox
        #   Configure.TOOLTIP:          String, Text shown when hovering
        #   Configure.VALIDATION:       Validation, Enum that corresponds to a function in VarHelper.py, it will check if the input of a text box is for example an invalid path, and it will skip saving the config if so
        #                               For this purpose enums like Validation.BOOLEAN will turn the value of the widget into a boolean, here's some of the validations:
        #                                   Validation.BOOLEAN
        #                                   Validation.INTEGER
        #                                   Validation.FLOAT
        #                                   Validation.DIGIT
        #                                   Validation.PATH
        #                                   Validation.FPATH
        #                                   Validation.DPATH
        #                                   Validation.EMPTY
        #
        #   Configure.FUNCTION:         Function, The function to connect to from 2 different sources:
        #                                   'extractor' is Extractor.py
        #                                   'main' is NA2000.py
        #                                   To connect the function use 'lambda: func(*args)'
        #   Configure.PLACEHOLDER:      String, Textboxes only: Text shown inside textboxes when it's empty
        #   Configure.ENTRIES:     String[], Comboboxes only: Each string in the array will be put in the combobox

        #   For you own information:
        #       When the extractor reads this dictionary it will instantiate the widgets in self.ui, the widgets will be named: f'{Configure.WIDGET.value}_{Configure.KEY}'
        #       Settings are stored in a dict at extractor.config.settings[key]
        ui = [
            #   Example of a textbox that saves 'resolution' and has to be integer
            {
                Configure.NAME: "cfg_resolution",
                Configure.WIDGET: Widgets.TEXTBOX,
                Configure.KEY: "resolution",
                Configure.DEFAULT: 120,
                Configure.TOOLTIP: "Changes the amount of iteration'",
                Configure.LABEL: "Resolution",
                Configure.PLACEHOLDER: "Integer (iterations)",
                Configure.VALIDATION: Validation.INTEGER,
            },
            #   Example of a combobox that defines twitter filenames
            {
                Configure.NAME: "cfg_filename",
                Configure.WIDGET: Widgets.COMBOBOX,
                Configure.KEY: "filename",
                Configure.DEFAULT: 0,
                Configure.ENTRIES: ["NA2000 (New)", "Old"],
                Configure.TOOLTIP: "Select between old and new filenames, it's recommended you leave it at 'NA2000 (new)'",
                Configure.LABEL: "Output filenames",
            },
            #   Example of a button that copies the cursor key in the extractor settings
            {
                Configure.NAME: "btn_copyCursor",
                Configure.WIDGET: Widgets.BUTTON,
                Configure.DEFAULT: "Copy last cursor",
                Configure.FUNCTION: lambda: self.copyLastCursor(extractor.config.settings["cursor"]),  # type: ignore
                Configure.TOOLTIP: "Copy the last valid cursor saved to your cliboard to be used in the user's cursor field'",
            },
        ]
        return ui

    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate, main) -> tuple[list[Any], dict[str, Any]]:
        try:
            #   This function returns the list of jobs to pass to the gallery-dl configuration
            #   It is extractor dependent, it will overlap from the top:
            #       baseConf (logic.py)
            #       overrideConf -> fullBaseConf (defined here)
            #       User custom config (defined in each different job by the user data)

            #   The job configurations are based on the current user passed as argument, so here you apply the keys you put in the user table for each user
            #   This is the equivalent of 'conf' files when you do them manually for gallery-dl
            #   Feel free to overwrite any options that come from logic.py, which already comes with options that should be the same between every extractor

            #   Settings not entirely provided:
            #       extractor.postprocessors.filename
            #       extractor.cookies (If your extractor needs more than 1 cookie or not a path to the cookies)
            #       extractor.filename
            #       extractor.directory (If it needs a separation between files)

            #   How to edit the base job:
            #       1 - Define a dictionary and write the options you need to override from the base
            #       2 - Run deepUpdate() on the job (see snippet later)

            overrideConf = {
                "extractor": {
                    self.galleryName: {
                        #   Calls getFilename.py passing metadata in, what the python file returns becomes the filename
                        #   It's not necessary to use a module but I do recommend it
                        "filename": "\fM ./external/getFilename.py:getNormalFilename",
                        "postprocessors": [{"filename": None}],
                    }
                }
            }
            #   It's required right after defining the options to override
            #   You can keep modifying the config after this
            fullBaseConf = copy.deepcopy(baseConf)
            deepUpdate(fullBaseConf, overrideConf)

            #   User-based example: Change extraction directory to Bar if username is Foo
            if user["UserHandle"] == "Foo":
                fullBaseConf["extractor"][self.galleryName]["directory"] = {"": "Bar"}

            #   Settings-based example: Change base filename of file to Bar if extractor settings say so
            if extSettings["changeFilenameToBar"]:
                fullBaseConf["extractor"][self.galleryName]["filename"] = "Bar"

            #   Now define which jobs to pass to gallery-dl after these lines
            #   Remember to append and return the right format for jobs:
            #       Array of dictionaries with
            #       'url'       The url that gallery-dl is going to user
            #       'config'    The config that gallery-dl is going to read (json above)
            #       'type'      Just a log of the current type of extraction
            #   The extractor will run on all jobs given
            #   To separate the kinds of job you should use a function that returns a modified job based on the current configuration or user
            #   Pass the normal config and user to the function and you can modify the configuration
            #   You should deepcopy the config so that they don't share an address and thus be changed when one changses

            jobs = []
            jobs.append(self._normalJob(user, fullBaseConf))
            jobs.append(self._differentJob(user, fullBaseConf))

            return jobs, self.defaultJob(user, fullBaseConf)
        except Exception as e:
            main.varHelper.exception(e)
            raise Exception(f"Error getting the jobs for {self.extractorName}: {e}")

    #   This job returns the original configuration
    def _normalJob(self, user, fullBaseConf):
        return {"url": f"https://test.com/{user['UserHandle']}", "config": copy.deepcopy(fullBaseConf), "type": "first"}

    #   This job changes a key and uses a different url
    #   Now there will be 2 different urls and configurations gallery-dl will go through, the one in _normalJob, _differentJob as we appended and returned them in the job array
    def _differentJob(self, user, fullBaseConf):
        fullBaseConf["key"] = "Different"
        return {"url": f"https://test.com/{user['UserHandle']}/different", "config": copy.deepcopy(fullBaseConf), "type": "different"}

    #   If errorListEnabled is enabled, recovering failed urls needs a default job that gets it from function 'defaultJob', it should serve a global purpose
    #   It is only necessary to return key 'config'
    def defaultJob(self, user, fullBaseConf):
        return {"url": None, "config": copy.deepcopy(fullBaseConf), "type": None}

    #   Helper method that can be called by specific extractors
    def copyLastCursor(self, cursor):
        pass

    #   The next step is to define the extractor in ExtractorsManager.py
