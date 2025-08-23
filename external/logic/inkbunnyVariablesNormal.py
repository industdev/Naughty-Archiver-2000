from datetime import datetime


def getNormal(metadata):
    userHandle = metadata["username"]
    userHandle = sanitize(userHandle)
    userID = metadata["user_id"]
    elementCreationTime = _ExtractDate(metadata["date"])
    elementId = metadata["submission_id"]
    if metadata["scraps"]:
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}_scrap.{metadata['extension']}"
    else:
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}.{metadata['extension']}"

def getNormal_Postprocessor(metadata):
    userHandle = metadata["username"]
    userHandle = sanitize(userHandle)
    userID = metadata["user_id"]
    elementCreationTime = _ExtractDate(metadata["date"])
    elementId = metadata["submission_id"]
    if metadata["scraps"]:
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}_scrap.json"
    else:
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}.json"


def Shorten(string):
    if len(string) > 64:
        string = string[:64]
    return string

def sanitize(filename):

    illegal_char_replacements = {
        '/': '⁄', 
        '\\': '∖',
        ':': '꞉',
        '*': '∗',
        '?': '？',
        '"': '＂',
        '<': '＜',
        '>': '＞',
        '|': '｜',
        '_': '＿',
    }

    sanitized = filename
    for char, replacement in illegal_char_replacements.items():
        sanitized = sanitized.replace(char, replacement)

    return sanitized


def _ExtractDate(dt):
    date_obj = dt.date()
    return date_obj

