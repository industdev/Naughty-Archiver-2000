from datetime import datetime


def initializeVariables(metadata):
    try:
        getMetadataType(metadata)

        if metadata_type == "User":
            initUserVariables(metadata)
            return
        elif (metadata_type == "background") or (metadata_type == "avatar"):
            initBannerOrAvatarVariables(metadata)
            return
    except Exception as e:
        raise Exception(f"Error in initializeVariables {e}")

    initTweetVariables(metadata)


def initUserVariables(metadata):
    global userHandle
    global userID
    global userCreationtime

    global elementQuoteID
    global elementRetweetID
    global elementReplyID
    global elementTweetID
    global elementCreationTime
    global elementCount

    elementTweetID = metadata["rest_id"]
    elementQuoteID = getQuoteID(metadata)
    elementRetweetID = getRetweetID(metadata)
    elementReplyID = getReplyID(metadata)

    try:
        elementCreationTime = getDate(metadata["legacy"]["created_at"])
        userHandle = sanitize(metadata["legacy"]["screen_name"])
        userCreationtime = getDate(metadata["legacy"]["created_at"])
    except:
        elementCreationTime = getDate(metadata["core"]["created_at"])
        userHandle = sanitize(metadata["core"]["screen_name"])
        userCreationtime = getDate(metadata["core"]["created_at"])

    userID = metadata["rest_id"]


def initBannerOrAvatarVariables(metadata):
    global userHandle
    global userID
    global userCreationtime

    global elementQuoteID
    global elementRetweetID
    global elementReplyID
    global elementBannerName
    global elementBannerExtention
    global elementAvatarName
    global elementAvatarExtention

    userID = metadata["user"]["rest_id"]
    userHandle = sanitize(metadata["user"]["legacy"]["name"])
    if bannerExists(metadata):
        elementBannerName = getBannerName(metadata["user"]["legacy"]["profile_banner_url"])
        elementBannerExtention = "jpg"
    if avatarExists(metadata):
        elementAvatarName = sanitize(getName(metadata["user"]["legacy"]["profile_image_url_https"]))
        elementAvatarExtention = getExtention(metadata["user"]["legacy"]["profile_image_url_https"])


def initTweetVariables(metadata):
    global userHandle
    global userID
    global userCreationtime
    global elementCount
    global elementTweetID
    global elementQuoteID
    global elementRetweetID
    global elementReplyID
    global elementCreationTime
    global elementBannerName
    global elementBannerExtention
    global elementAvatarName
    global elementAvatarExtention
    global elementImageExtention

    elementQuoteID = getQuoteID(metadata)
    elementRetweetID = getRetweetID(metadata)
    elementReplyID = getReplyID(metadata)
    elementCreationTime = getDate(metadata["legacy"]["created_at"])
    elementCount = metadata["count"]
    elementImageExtention = getElementImageExtention(metadata)
    elementTweetID = metadata["rest_id"]
    userID = metadata["core"]["user_results"]["result"]["rest_id"]
    userHandle = sanitize(metadata["core"]["user_results"]["result"]["legacy"]["name"])


def getDate(created_at_str):
    date_format = "%a %b %d %H:%M:%S %z %Y"
    created_at = datetime.strptime(created_at_str, date_format)
    return created_at.strftime("%Y-%m-%d")


def getExtention(s):
    strSplit = s.split("/")
    extSplit = strSplit[-1].split(".")
    ext = extSplit[1]
    return ext


def getName(s):
    strSplit = s.split("/")
    nameSplit = strSplit[-1].split(".")
    name = nameSplit[0]
    return name


def getBannerName(s):
    strSplit = s.split("/")
    name = strSplit[-1]
    return name


def getElementImageExtention(metadata):
    try:
        media_url_https = metadata["legacy"]["entities"]["media"][0]["media_url_https"]
        return getExtention(media_url_https)
    except (KeyError, IndexError):
        return ""


def getMetadataType(metadata):
    global metadata_type
    try:
        metadata_type = metadata["__typename"]
    except KeyError:
        if metadata["subcategory"] == "background":
            metadata_type = "background"
        elif metadata["subcategory"] == "avatar":
            metadata_type = "avatar"
        else:
            metadata_type = "tweet"


def getReplyID(metadata):
    try:
        return metadata["legacy"]["in_reply_to_status_id_str"]
    except KeyError:
        return 0


def getRetweetID(metadata):
    try:
        return metadata["legacy"]["retweeted_status_id_str"]
    except KeyError:
        return 0


def getQuoteID(metadata):
    try:
        return metadata["legacy"]["quoted_status_id_str"]
    except KeyError:
        return 0


def bannerExists(metadata):
    try:
        metadata["user"]["legacy"]["profile_banner_url"]
        return 1
    except Exception:
        return 0


def avatarExists(metadata):
    try:
        metadata["user"]["legacy"]["profile_image_url_https"]
        return 1
    except Exception:
        return 0


def getPostprocessorUserprofile(metadata):
    initializeVariables(metadata)
    return f"twitter_{userHandle}-{userID}_profile.json"


def getFilenameTweet(metadata):
    initializeVariables(metadata)
    return f"twitter_{userHandle}-{userID}_{elementCreationTime}_{elementTweetID}.{elementImageExtention}"


def getPostprocessorTweet(metadata):
    initializeVariables(metadata)
    return f"twitter_{userHandle}-{userID}_{elementCreationTime}_{elementTweetID}.json"


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


def extractDate(dt):
    return dt.strftime("%Y-%m-%d")
