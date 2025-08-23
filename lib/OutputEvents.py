class Events:
    @staticmethod
    def apicall(debuggy, main):
        main.stats.counter.increase(1, "totApiCalls", False)
        debuggy("apicall", "Events")

    @staticmethod
    def updateCursor(debuggy, ext, value, gallery):
        #   update the copy cursor on the settings, update the user cursor on the table and update the user cursor on the user variable in the extraction
        ext.config.settings["cursor"] = value
        _handle = gallery.extractor.user["UserHandle"]
        gallery.extractor.users.setUserKey(_handle, "Cursor", value)
        gallery.extractor.user["Cursor"] = value
        debuggy(f"updateCursor -> {_handle} to {value}", "Events")

    @staticmethod
    def setUserToSkip(debuggy, gallery):
        _handle = gallery.extractor.user["UserHandle"]
        gallery.extractor.users.setUserKey(_handle, "Skip", True)
        gallery.extractor.user["Skip"] = True
        debuggy(f"setUserToSkip -> {_handle}", "Events")

    @staticmethod
    def addErroredUrl(debuggy, line, extErroredConfig, userName):
        import os
        import re
        import json

        path = extErroredConfig[0]  # Path to JSON file
        errorRegexes = extErroredConfig[1]  # List of regexes to extract error reason
        idRegex = extErroredConfig[2]  # Regex to extract post ID
        urlFormat = extErroredConfig[3]  # Format string with %s placeholder

        #   Extract ID from line
        id_match = re.search(idRegex, line)
        if not id_match:
            return False, "no id found"
        postID = id_match.group().strip("'")

        #   Extract error message
        message = None
        for regex in errorRegexes:
            match = re.search(regex, line)
            if match:
                message = match.group(1) if match.groups() else match.group(0).strip("()'")
                break

        if not message:
            debuggy(f"addErroredUrl -> No message found in '{line}'", "Events")
            return False, "no message found"

        #   Construct URL
        full_url = urlFormat.replace("%s", postID)

        #   Load existing JSON data
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = []
        else:
            data = []

        #   Check for duplicate
        if any(entry.get("url") == full_url for entry in data):
            return False, "duplicate"

        #   Append new entry
        newEntry = {"user": userName, "url": full_url, "error": message}
        data.append(newEntry)

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as write_err:
            return False, f"write error: {write_err}"

        debuggy(f"addErroredUrl -> {newEntry}", "Events")
        return newEntry, None
