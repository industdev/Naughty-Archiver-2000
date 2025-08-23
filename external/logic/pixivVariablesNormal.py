from datetime import datetime


def getNormal(metadata):
    userHandle = metadata["user"]["name"]
    userHandle = sanitize(userHandle)
    
    userID = metadata["user"]["id"]
    elementCreationTime = _ExtractDate(metadata['date'])
    
    if metadata["subcategory"] == "avatar":
        mediaName = metadata["user"]["profile_image_urls"]["medium"]
        mediaName = mediaName.split('/')[-1]
        mediaName = Shorten(mediaName.split('_')[1])
        return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_{mediaName}_avatar.{metadata['extension']}"
    
    elementId = metadata["id"]
    elementTitle = sanitize(metadata["title"])
    if metadata["x_restrict"]:
        R18 = "-R18"
    else:
        R18 = ""
    
    return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}{R18}]_{metadata['num']}.{metadata['extension']}"

def getNormal_Postprocessor(metadata):
    userHandle = metadata["user"]["name"]
    userHandle = sanitize(userHandle)
    userID = metadata["user"]["id"]
    elementCreationTime = _ExtractDate(metadata['date'])
    


    if metadata["subcategory"] == "avatar":
        mediaName = metadata["user"]["profile_image_urls"]["medium"]
        mediaName = mediaName.split('/')[-1]
        mediaName = Shorten(mediaName.split('_')[1])
        return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_{mediaName}_avatar.json"
    
    if metadata["subcategory"] == "background":
        mediaName = metadata["profile"]["background_image_url"]
        mediaName = mediaName.split('/')[-1]
        mediaName = Shorten(mediaName.split('_')[1])
        return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_{mediaName}_banner.json"

    elementId = metadata["id"]
    elementTitle = sanitize(metadata["title"])
    if metadata["x_restrict"]:
        R18 = "-R18"
    else:
        R18 = ""
        
    return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}{R18}].json"

def Shorten(string):
    split2 = f"{string[:4]}{string[-4:]}"
    return split2

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

def extractDate(dt):
    return dt.strftime('%Y-%m-%d')


def _ExtractDate(dt):
    date_obj = dt.date()
    return date_obj

