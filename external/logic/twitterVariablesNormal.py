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
    
    userID = metadata['author']['id']
    userHandle = sanitize(metadata['author']['name'])
    userNick = sanitize(metadata['author']['nick'])

    if (bannerExists(metadata)):   
        elementBannerName = getBannerName(metadata['author']['profile_banner'])
    if (avatarExists(metadata)):
        elementAvatarName = sanitize(getName(metadata['author']['profile_image']))
        elementAvatarExtention = getExtension(metadata['author']['profile_image'])

    
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
    
    elementCount = metadata['count']
    elementImageExtention = getElementImageExtention(metadata)
    userTweetID = metadata['tweet_id']
    creationTime = extractDate(metadata['date'])
    userID = metadata['author']['id']
    userHandle = metadata['author']['name']
    userName = metadata['author']['nick']
    
def getExtension(s):
    strSplit = s.split('/')
    extSplit = strSplit[-1].split('.')
    ext = extSplit[1]
    return ext

def getName(s):
    strSplit = s.split('/')
    nameSplit = strSplit[-1].split('.')
    name = nameSplit[0]
    return name

def getBannerName(s):
    strSplit = s.split('/')
    name = strSplit[-1]
    return name

def getElementImageExtention(metadata):
    try:
        media_url_https = metadata['legacy']['entities']['media'][0]['media_url_https']
        return getExtension(media_url_https)
    except (KeyError, IndexError):
        return ""
    
def getMetadataType(metadata):
    global metadata_type
    try:
        metadata_type = metadata['subcategory']
    except KeyError:
        if (metadata['subcategory'] == "background"):
            metadata_type = "background"
        elif (metadata['subcategory'] == "avatar"):
            metadata_type = "avatar"
        else:
            metadata_type = "timeline"
    
def bannerExists(metadata):
    try:
        metadata['subcategory']
        return 1
    except Exception:
        return 0
        
def avatarExists(metadata):
    try:
        metadata['subcategory']
        return 1
    except Exception:
        return 0

def getPostprocessorAvatarOrBanner(metadata):
    initBannerOrAvatarVariables(metadata)
    if (metadata['subcategory'] == "avatar"):
        return f"twitter_{userHandle}-{userID}_{elementAvatarName}_avatar.json"
    else:
        return f"twitter_{userHandle}-{userID}_{elementBannerName}_banner.json"

def getFilenameAvatarOrBanner(metadata):
    initBannerOrAvatarVariables(metadata)
    if (metadata['subcategory'] == "avatar"):
        return f"twitter_{userHandle}-{userID}_{elementAvatarName}_avatar.{metadata['extension']}"
    else:
        return f"twitter_{userHandle}-{userID}_{elementBannerName}_banner.{metadata['extension']}"

def getFilenameTweet(metadata):
    userTweetID = metadata['tweet_id']
    creationTime = extractDate(metadata['date'])
    userID = metadata['user']['id']
    userHandle = sanitize(metadata['user']['name'])
    userName =  sanitize(metadata['user']['nick'])
    authorID = metadata['author']['id']
    authorHandle =  sanitize(metadata['author']['name'])
    authorName =  sanitize(metadata['author']['nick'])
    
    #   If it's a retweet, quote, reply, media of a reply, display both users
    users = f"{userHandle}-ID{userID}"
    #  Media of a reply (no easy way of knowing)
    if authorID != userID:
        users = f'{authorHandle}-ID{authorID}'
    #  Retweet
    if metadata["retweet_id"] != 0:
        users = f'{userHandle}-ID{userID}-RT-{authorHandle}-ID{authorID}-ST{metadata["retweet_id"]}'
    #  Reply
    if metadata["reply_id"] != 0:
        users = f'{userHandle}-ID{userID}-@-{metadata["reply_to"]}-ST{metadata["reply_id"]}'
    #  Quote
    if metadata["quote_id"] != 0:
        userTweetID = metadata["quote_id"]
        users = f'{userHandle}-ID{userID}-QT-ST{metadata["tweet_id"]}'
        
    return f"twitter_{users}_{creationTime}_ST{userTweetID}_{metadata['num']}.{metadata['extension']}"

def getFilenameTweetLegacy(metadata):
    userTweetID = metadata['tweet_id']
    creationTime = extractDate(metadata['date'])
    userID = metadata['author']['id']
    userHandle = metadata['author']['name']
    userName = metadata['author']['nick']
    
    return f"twitter_[{userHandle}-{userName}-{userID}][{creationTime}]_{userTweetID}_{metadata['num']}.{metadata['extension']}"

def getPostprocessorTweet(metadata):
    userTweetID = metadata['tweet_id']
    creationTime = extractDate(metadata['date'])
    userID = metadata['user']['id']
    userHandle =  sanitize(metadata['user']['name'])
    userName =  sanitize(metadata['user']['nick'])
    authorID = metadata['author']['id']
    authorHandle =  sanitize(metadata['author']['name'])
    authorName =  sanitize(metadata['author']['nick'])
    
    #   If it's a retweet, quote, reply, media of a reply, display both users
    users = f"{userHandle}-ID{userID}"
    #  Media of a reply (no easy way of knowing)
    if authorID != userID:
        users = f'{authorHandle}-ID{authorID}'
    #  Retweet
    if metadata["retweet_id"] != 0:
        users = f'{userHandle}-ID{userID}-RT-{authorHandle}-ID{authorID}-ST{metadata["retweet_id"]}'
    #  Reply
    if metadata["reply_id"] != 0:
        users = f'{userHandle}-ID{userID}-@-{metadata["reply_to"]}-ST{metadata["reply_id"]}'
    #  Quote
    if metadata["quote_id"] != 0:
        userTweetID = metadata["quote_id"]
        users = f'{userHandle}-ID{userID}-QT-ST{metadata["tweet_id"]}'
         
    return f"twitter_{users}_{creationTime}_ST{userTweetID}.json"

def getPostprocessorTweetLegacy(metadata):
    userTweetID = metadata['tweet_id']
    creationTime = extractDate(metadata['date'])
    userID = metadata['author']['id']
    userHandle = metadata['author']['name']
    userName = metadata['author']['nick']

    return f"twitter_[{userHandle}-{userName}-{userID}][{creationTime}]_{userTweetID}.json"

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