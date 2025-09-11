from datetime import datetime


class Helper:
    @staticmethod
    def shorten(string, length=64):
        if not string:
            return "None"
        if len(string) > length:
            string = string[:length]
        return string

    @staticmethod
    def limit(string):
        if not string:
            return "None"
        split2 = f"{string[:4]}{string[-4:]}"
        return split2

    @staticmethod
    def sanitize(filename) -> str:
        if not filename:
            return "None"

        replacement = {
            "/": "⁄",
            "\\": "∖",
            ":": "꞉",
            "*": "∗",
            "?": "？",
            '"': "＂",
            "<": "＜",
            ">": "＞",
            "|": "｜",
            "_": "＿",
        }

        sanitized = filename
        for char, replacement in replacement.items():
            sanitized = sanitized.replace(char, replacement)

        return sanitized

    @staticmethod
    def extractDate(dt) -> str:
        if not dt:
            return "None"
        obj = dt.date()
        return obj

    @staticmethod
    def extractZDate(dt) -> str:
        if not dt:
            return "None"
        obj = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted = obj.strftime("%Y-%m-%d")
        return formatted

    @staticmethod
    def extractCreationDate(dt) -> str:
        if not dt:
            return "None"

        format = "%a %b %d %H:%M:%S %z %Y"
        obj = datetime.strptime(dt, format)
        return obj.strftime("%Y-%m-%d")
