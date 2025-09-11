from Helper import Helper


def initializeVariables(metadata):
    if (metadata_type == "background") or (metadata_type == "avatar"):
        initBannerOrAvatarVariables(metadata)
    else:
        initTweetVariables(metadata)


def initBannerOrAvatarVariables(metadata):
    global userHandle
    global userNick
    global userID
    global elementBannerName
    global elementAvatarName
    global elementAvatarExtention

    userID = metadata.get("author", {}).get("id")
    userHandle = Helper.sanitize(metadata.get("author", {}).get("name"))
    userNick = Helper.sanitize(metadata.get("author", {}).get("nick"))

    if bannerExists(metadata):
        elementBannerName = getBannerName(metadata.get("author", {}).get("profile_banner"))
    if avatarExists(metadata):
        elementAvatarName = Helper.sanitize(getName(metadata.get("author", {}).get("profile_image")))
        elementAvatarExtention = getExtension(metadata.get("author", {}).get("profile_image"))


def initTweetVariables(metadata):
    global userHandle
    global userID
    global elementCount
    global userTweetID
    global elementBannerName
    global elementAvatarName
    global elementAvatarExtention
    global elementImageExtention
    global creationTime
    global userName

    elementCount = metadata.get("count")
    elementImageExtention = getElementImageExtention(metadata)
    userTweetID = metadata.get("tweet_id")
    creationTime = Helper.extractDate(metadata.get("date"))
    userID = metadata.get("author", {}).get("id")
    userHandle = metadata.get("author", {}).get("name")
    userName = metadata.get("author", {}).get("nick")


def getExtension(s):
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
        return getExtension(media_url_https)
    return ""


def getMetadataType(metadata):
    global metadata_type
    metadata_type = metadata.get("subcategory")
    if metadata.get("subcategory") == "background":
        metadata_type = "background"
    elif metadata.get("subcategory") == "avatar":
        metadata_type = "avatar"
    else:
        metadata_type = "timeline"


def bannerExists(metadata):
    return bool(metadata.get("subcategory"))


def avatarExists(metadata):
    return bool(metadata.get("subcategory"))


def getPostprocessorAvatarOrBanner(metadata):
    initBannerOrAvatarVariables(metadata)
    if metadata.get("subcategory") == "avatar":
        return f"twitter_{userHandle}-{userID}_{elementAvatarName}_avatar.json"
    else:
        return f"twitter_{userHandle}-{userID}_{elementBannerName}_banner.json"


def getFilenameAvatarOrBanner(metadata):
    initBannerOrAvatarVariables(metadata)
    if metadata.get("subcategory") == "avatar":
        return f"twitter_{userHandle}-{userID}_{elementAvatarName}_avatar.{metadata.get('extension')}"
    else:
        return f"twitter_{userHandle}-{userID}_{elementBannerName}_banner.{metadata.get('extension')}"


def getFilenameTweet(metadata):
    userTweetID = metadata.get("tweet_id")
    creationTime = Helper.extractDate(metadata.get("date"))
    userID = metadata.get("user", {}).get("id")
    userHandle = Helper.sanitize(metadata.get("user", {}).get("name"))
    userName = Helper.sanitize(metadata.get("user", {}).get("nick"))
    authorID = metadata.get("author", {}).get("id")
    authorHandle = Helper.sanitize(metadata.get("author", {}).get("name"))
    authorName = Helper.sanitize(metadata.get("author", {}).get("nick"))

    #   If it's a retweet, quote, reply, media of a reply, display both users
    users = f"{userHandle}-ID{userID}"
    #  Media of a reply (no easy way of knowing)
    if authorID != userID:
        users = f"{authorHandle}-ID{authorID}"
    #  Retweet
    if metadata.get("retweet_id") != 0:
        users = f"{userHandle}-ID{userID}-RT-{authorHandle}-ID{authorID}-ST{metadata.get('retweet_id')}"
    #  Reply
    if metadata.get("reply_id") != 0:
        users = f"{userHandle}-ID{userID}-@-{metadata.get('reply_to')}-ST{metadata.get('reply_id')}"
    #  Quote
    if metadata.get("quote_id") != 0:
        userTweetID = metadata.get("quote_id")
        users = f"{userHandle}-ID{userID}-QT-ST{metadata.get('tweet_id')}"

    return f"twitter_{users}_{creationTime}_ST{userTweetID}_{metadata.get('num')}.{metadata.get('extension')}"


def getFilenameTweetLegacy(metadata):
    userTweetID = metadata.get("tweet_id")
    creationTime = Helper.extractDate(metadata.get("date"))
    userID = metadata.get("author", {}).get("id")
    userHandle = metadata.get("author", {}).get("name")
    userName = metadata.get("author", {}).get("nick")

    return f"twitter_[{userHandle}-{userName}-{userID}][{creationTime}]_{userTweetID}_{metadata.get('num')}.{metadata.get('extension')}"


def getPostprocessorTweet(metadata):
    userTweetID = metadata.get("tweet_id")
    creationTime = Helper.extractDate(metadata.get("date"))
    userID = metadata.get("user", {}).get("id")
    userHandle = Helper.sanitize(metadata.get("user", {}).get("name"))
    userName = Helper.sanitize(metadata.get("user", {}).get("nick"))
    authorID = metadata.get("author", {}).get("id")
    authorHandle = Helper.sanitize(metadata.get("author", {}).get("name"))
    authorName = Helper.sanitize(metadata.get("author", {}).get("nick"))

    #   If it's a retweet, quote, reply, media of a reply, display both users
    users = f"{userHandle}-ID{userID}"
    #  Media of a reply (no easy way of knowing)
    if authorID != userID:
        users = f"{authorHandle}-ID{authorID}"
    #  Retweet
    if metadata.get("retweet_id") != 0:
        users = f"{userHandle}-ID{userID}-RT-{authorHandle}-ID{authorID}-ST{metadata.get('retweet_id')}"
    #  Reply
    if metadata.get("reply_id") != 0:
        users = f"{userHandle}-ID{userID}-@-{metadata.get('reply_to')}-ST{metadata.get('reply_id')}"
    #  Quote
    if metadata.get("quote_id") != 0:
        userTweetID = metadata.get("quote_id")
        users = f"{userHandle}-ID{userID}-QT-ST{metadata.get('tweet_id')}"

    return f"twitter_{users}_{creationTime}_ST{userTweetID}.json"


def getPostprocessorTweetLegacy(metadata):
    userTweetID = metadata.get("tweet_id")
    creationTime = Helper.extractDate(metadata.get("date"))
    userID = metadata.get("author", {}).get("id")
    userHandle = metadata.get("author", {}).get("name")
    userName = metadata.get("author", {}).get("nick")

    return f"twitter_[{userHandle}-{userName}-{userID}][{creationTime}]_{userTweetID}.json"
