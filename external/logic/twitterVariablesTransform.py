from Helper import Helper


def initializeVariables(metadata):
    getMetadataType(metadata)

    if metadata_type == "User":
        initUserVariables(metadata)
        return
    elif (metadata_type == "background") or (metadata_type == "avatar"):
        initBannerOrAvatarVariables(metadata)
        return

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

    elementTweetID = metadata.get("rest_id")
    elementQuoteID = getQuoteID(metadata)
    elementRetweetID = getRetweetID(metadata)
    elementReplyID = getReplyID(metadata)

    if metadata.get("legacy"):
        elementCreationTime = Helper.extractCreationDate(metadata.get("legacy", {}).get("created_at"))
        userHandle = Helper.sanitize(metadata.get("legacy", {}).get("screen_name"))
        userCreationtime = Helper.extractCreationDate(metadata.get("legacy", {}).get("created_at"))
    else:
        elementCreationTime = Helper.extractCreationDate(metadata.get("core", {}).get("created_at"))
        userHandle = Helper.sanitize(metadata.get("core", {}).get("screen_name"))
        userCreationtime = Helper.extractCreationDate(metadata.get("core", {}).get("created_at"))

    userID = metadata.get("rest_id")


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

    userID = metadata.get("user", {}).get("rest_id")
    userHandle = Helper.sanitize(metadata.get("user", {}).get("legacy", {}).get("name"))
    if bannerExists(metadata):
        elementBannerName = getBannerName(metadata.get("user", {}).get("legacy", {}).get("profile_banner_url"))
        elementBannerExtention = "jpg"
    if avatarExists(metadata):
        elementAvatarName = Helper.sanitize(getName(metadata.get("user", {}).get("legacy", {}).get("profile_image_url_https")))
        elementAvatarExtention = getExtention(metadata.get("user", {}).get("legacy", {}).get("profile_image_url_https"))


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
    elementCreationTime = Helper.extractCreationDate(metadata.get("legacy", {}).get("created_at"))
    elementCount = metadata.get("count")
    elementImageExtention = getElementImageExtention(metadata)
    elementTweetID = metadata.get("rest_id")
    userID = metadata.get("core", {}).get("user_results", {}).get("result", {}).get("rest_id")
    userHandle = Helper.sanitize(metadata.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("name"))


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
    media_url_https = metadata.get("legacy", {}).get("entities", {}).get("media", [{}])[0].get("media_url_https")
    if media_url_https:
        return getExtention(media_url_https)
    return ""


def getMetadataType(metadata):
    global metadata_type
    metadata_type = metadata.get("__typename")
    if metadata.get("subcategory") == "background":
        metadata_type = "background"
    elif metadata.get("subcategory") == "avatar":
        metadata_type = "avatar"
    else:
        metadata_type = "tweet"


def getReplyID(metadata):
    return metadata.get("legacy", {}).get("in_reply_to_status_id_str") or 0


def getRetweetID(metadata):
    return metadata.get("legacy", {}).get("retweeted_status_id_str") or 0


def getQuoteID(metadata):
    return metadata.get("legacy", {}).get("quoted_status_id_str") or 0


def bannerExists(metadata):
    return bool(metadata.get("user", {}).get("legacy", {}).get("profile_banner_url"))


def avatarExists(metadata):
    return bool(metadata.get("user", {}).get("legacy", {}).get("profile_image_url_https"))


def getPostprocessorUserprofile(metadata):
    initializeVariables(metadata)
    return f"twitter_{userHandle}-{userID}_profile.json"


def getFilenameTweet(metadata):
    initializeVariables(metadata)
    return f"twitter_{userHandle}-{userID}_{elementCreationTime}_{elementTweetID}.{elementImageExtention}"


def getPostprocessorTweet(metadata):
    initializeVariables(metadata)
    return f"twitter_{userHandle}-{userID}_{elementCreationTime}_{elementTweetID}.json"
