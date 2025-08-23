from datetime import datetime


def getNormal(metadata):

    userHandle = metadata["artist"]
    userHandle = sanitize(userHandle)
    userID = metadata["id"]
    elementCreationTime = _ExtractDate(metadata["date"])
    elementId = metadata["filename"].split(".")[0]
    elementName = metadata["filename"].split(".")[1]

    elementTitle = sanitize(metadata["title"])
    elementTitle = Shorten(elementTitle, 28)
    
    if metadata["rating"] == "Adult":
        r18 = "-R18"
    else:
        r18 = ""
            
    return f"furaffinity_{userHandle}_{elementCreationTime}_[{elementId}-{elementName}{r18}].{metadata['extension']}"

def getNormal_Postprocessor(metadata):

    userHandle = metadata["artist"]
    userHandle = sanitize(userHandle)
    userID = metadata["id"]
    elementCreationTime = _ExtractDate(metadata["date"])
    elementId = metadata["filename"].split(".")[0]
    elementName = metadata["filename"].split(".")[1]

    elementTitle = sanitize(metadata["title"])
    elementTitle = Shorten(elementTitle, 28)

    if metadata["rating"] == "Adult":
        r18 = "-R18"
    else:
        r18 = ""

    return f"furaffinity_{userHandle}_{elementCreationTime}_[{elementId}-{elementName}{r18}].json"

def Shorten(string, length = 64):
    if len(string) > length:
        string = string[:length]
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

