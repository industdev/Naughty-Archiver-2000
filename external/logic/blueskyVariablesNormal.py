from datetime import datetime


def getMetadataType(metadata):
    global metadata_type
    try:
        metadata_type = metadata["subcategory"]
    except KeyError:
        if metadata["subcategory"] == "background":
            metadata_type = "background"
        elif metadata["subcategory"] == "avatar":
            metadata_type = "avatar"
        else:
            metadata_type = "timeline"


def getNormal(metadata):
    userHandle = metadata["author"]["handle"]
    userHandle = sanitize(userHandle)
    userHandle = userHandle.split(".")[0]
    userID = metadata["author"]["did"].split(":")[2]
    elementCreationTime = _ExtractDate(metadata["createdAt"])
    elementPostID = metadata["post_id"]
    return f"bsky_{userHandle}-{userID}_{elementCreationTime}_{elementPostID}_{metadata['num']}.{metadata['extension']}"


def getNormal_Postprocessor(metadata):
    userHandle = metadata["author"]["handle"]
    userHandle = sanitize(userHandle)
    userHandle = userHandle.split(".")[0]
    userID = metadata["author"]["did"].split(":")[2]
    elementCreationTime = _ExtractDate(metadata["createdAt"])
    elementPostID = metadata["post_id"]
    return f"bsky_{userHandle}-{userID}_{elementCreationTime}_{elementPostID}.json"


def getUserprofile(metadata):
    userHandle = metadata["user"]["handle"]
    userHandle = sanitize(userHandle)
    userHandle = userHandle.split(".")[0]
    userID = metadata["user"]["did"].split(":")[2]
    mediaName = Shorten(metadata["embed"]["images"][0]["image"]["ref"]["$link"])

    if metadata["subcategory"] == "background":
        return f"bsky_{userHandle}-{userID}_{mediaName}_banner.{metadata['extension']}"

    if metadata["subcategory"] == "avatar":
        return f"bsky_{userHandle}-{userID}_{mediaName}_avatar.{metadata['extension']}"


def getUserprofile_Postprocessor(metadata):
    if metadata["subcategory"] == "info":
        userHandle = metadata["handle"]
        userHandle = sanitize(userHandle)
        userID = metadata["did"].split(":")[2]
        return f"bsky_{userHandle}-{userID}_profile.json"
    else:
        userHandle = metadata["user"]["handle"]
        userHandle = sanitize(userHandle)
        userHandle = userHandle.split(".")[0]
        userID = metadata["user"]["did"].split(":")[2]
        mediaName = Shorten(metadata["embed"]["images"][0]["image"]["ref"]["$link"])

        if metadata["subcategory"] == "background":
            return f"bsky_{userHandle}-{userID}_{mediaName}_banner.json"

        if metadata["subcategory"] == "avatar":
            return f"bsky_{userHandle}-{userID}_{mediaName}_avatar.json"


def Shorten(string):
    return f"{string[:2]}{string[-2:]}"


def sanitize(filename):
    illegal_char_replacements = {
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
    for char, replacement in illegal_char_replacements.items():
        sanitized = sanitized.replace(char, replacement)

    return sanitized


def _ExtractDate(dt):
    date_obj = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")

    formatted_date = date_obj.strftime("%Y-%m-%d")

    return formatted_date
