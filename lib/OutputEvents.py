import base64
import os
import re
import subprocess
import sys


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

    @staticmethod
    def convertToGif(debuggy, main, extractor, message):
        try:
            #   Since gallery-dl doesn't let it's interal python process to be called
            #   We have to rely on it's output, so we have to parse the message and thank it for doing so

            extractor.logger.debug("[debug] As you please, Gallery-dl stdout sir.")
            ffmpegPath = os.path.join(main.toolsPath, "ffmpeg.exe")

            match = re.search(r'Archiver, please convert\s+"([^"]+)"', message)
            if not match:
                debuggy("[debug] Could not find video path in message", "Events")
            videoPath = os.path.normpath(match.group(1))  # type: ignore

            delete = True if "removing the original" in message else False

            debuggy(f"[info] Converting {os.path.basename(videoPath)} to GIF", "Events")
            debuggy(f"[debug] ffmpegPath: {ffmpegPath}, delete: {delete}, Path: {videoPath}", "Events")

            if not os.path.exists(videoPath):
                debuggy("[debug] Video file does not exist", "Events")

            base, ext = os.path.splitext(videoPath)
            gifPath = base + ".gif"

            try:
                subprocess.run(
                    [
                        ffmpegPath,
                        "-v",
                        "warning",
                        "-i",
                        videoPath,
                        "-filter_complex",
                        "[0:v] fps=15,scale=640:-1:flags=lanczos,split [a][b]; [a] palettegen=max_colors=256:reserve_transparent=0 [p]; [b][p] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                        "-y",
                        gifPath,
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if delete:
                    debuggy(f"[debug] Deleting source video {videoPath}", "Events")
                    main.safeTrash(videoPath)

            except subprocess.CalledProcessError as e:
                debuggy(f"[debug] FFmpeg command failed with return code {e.returncode}", "Events")

        except Exception as e:
            debuggy(f"[debug] Failed to convert gif: {e}", "Events")
