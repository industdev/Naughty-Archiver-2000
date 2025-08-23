from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lib.Extractor import Extractor
class Logic:
    
    def __init__(self, generalSettings, extractor: "Extractor"):
        try:
            #   Skip media -> "image-filter": "width == 0"
            self.extSettings = extractor.config.settings
            self.extractor = extractor
            self.jobBaseConfig = {
                "actions": {"warning:limit_sanity_level": "level = debug"},
                "metadata": {
                    "mtime": True
                },
                "output": {
                    "mode": "null",
                    "shorten": False,
                    "ansi": False,
                    "private": True,
                    "skip": False,
                    "progress": False,
                    "log": "[g-dl][{levelname}] {message}",
                    "unsupportedfile": "",
                    "errorfile": "",
                    "stdout": {
                        "encoding": "utf-8",
                        "errors": "backslashreplace",
                        "line_buffering": False,
                    },
                    "stderr": {
                        "encoding": "utf-8",
                        "errors": "backslashreplace",
                        "line_buffering": False,
                    },
                },
                "downloader": {
                    extractor.galleryName: {
                        "part": False,
                        "rate": f'{generalSettings["maxdlspeed"]}k',
                        "progress": None,
                        "retries": -1,
                    }
                },
                "extractor": {
                    #   "modules": [f"{extractor.galleryName}"], The modules option slows gallery-dl down upon start
                    extractor.galleryName: {
                    "filename": "NoFilenameSet",
                    "directory": {"": [""]},
                    "extension-map": {
                        "jpeg": "jpg",
                        "jpe" : "jpg",
                        "jfif": "jpg",
                        "jif" : "jpg",
                        "jfi" : "jpg",
                        ".htm": ".html",
                        ".tif": ".tiff",
                        ".yml": ".yaml",
                        ".mpg": ".mpeg",
                        ".aif": ".aiff",
                        ".text": ".txt",
                        ".mdown": ".md",
                        ".markdown": ".md",
                    },
                    "sleep": [
                        self.extSettings["sleeptime"], 
                        self.extSettings["sleeptime"] + generalSettings["sleepmodulate"]
                    ],
                    "sleep-extractor": [
                        self.extSettings["sleeptime"], 
                        self.extSettings["sleeptime"] + generalSettings["sleepmodulate"]
                    ],
                    "sleep-request": [
                        self.extSettings["sleeptime"], 
                        self.extSettings["sleeptime"] + generalSettings["sleepmodulate"]
                    ],
                    "input": False,
                    "cookies": self.extSettings["cookiespath"],
                    "retries": -1,
                    "postprocessors": [
                            {
                                "name": "metadata",
                                "mode": "json",
                                "private": True,
                                "directory": "metadata",
                                "skip": True,
                                "event": "post",
                                "mtime": True,
                                "filename": "NoFilenameSet"
                            }
                        ]
                    }
                },
            }
            if generalSettings["extendedmetadata"]:
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["http-metadata"] = "_http"
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["version-metadata"] = "_gallery-dl"
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["extractor-metadata"] ="_extractor"
                self.jobBaseConfig["extractor"][self.extractor.galleryName]["url-metadata"]  ="_url"
        except Exception as e:
            raise
        
    def getBaseConf(self, user):
        try:
            #   Needed because dependent on user

            if user["DestinationPath"] != "default":
                destination = user["DestinationPath"]
            else:
                destination = f'{self.extSettings["defaultpath"]}/{user["UserHandle"]}'

            self.jobBaseConfig["extractor"][self.extractor.galleryName]["base-directory"] = destination
            self.jobBaseConfig["extractor"][self.extractor.galleryName]["archive"] = f'{destination}/{user["UserHandle"]}.sql'

            return self.jobBaseConfig
        except Exception as e:
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
