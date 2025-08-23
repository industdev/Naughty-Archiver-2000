from datetime import datetime


def getNormal(metadata):
    userHandle = metadata["user_profile"]["name"]
    userHandle = sanitize(userHandle)
    userID = metadata["user_profile"]["id"]
    elementCreationTime = _ExtractDate(metadata["date"])
    elementId = metadata["id"]
    elementTitle = sanitize(metadata["title"])
    elementTitle = Shorten(elementTitle)

    return f"kemono_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}].{metadata['extension']}"

def getNormal_Postprocessor(metadata):
    userHandle = metadata["user_profile"]["name"]
    userHandle = sanitize(userHandle)
    userID = metadata["user_profile"]["id"]
    elementCreationTime = _ExtractDate(metadata["date"])
    elementId = metadata["id"]
    elementTitle = sanitize(metadata["title"])
    elementTitle = Shorten(elementTitle)

    return f"kemono_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}].json"

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

