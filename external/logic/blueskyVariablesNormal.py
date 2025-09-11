from Helper import Helper


def getNormal(metadata):
    userHandle = metadata["author"]["handle"]
    userHandle = Helper.sanitize(userHandle)
    userHandle = userHandle.split(".")[0]
    userID = metadata["author"]["did"].split(":")[2]
    elementCreationTime = Helper.extractZDate(metadata.get("createdAt"))
    elementPostID = metadata.get("post_id")
    return f"bsky_{userHandle}-{userID}_{elementCreationTime}_{elementPostID}_{metadata.get('num')}.{metadata.get('extension')}"


def getNormal_Postprocessor(metadata):
    userHandle = metadata["author"]["handle"]
    userHandle = Helper.sanitize(userHandle)
    userHandle = userHandle.split(".")[0]
    userID = metadata["author"]["did"].split(":")[2]
    elementCreationTime = Helper.extractZDate(metadata.get("createdAt"))
    elementPostID = metadata.get("post_id")
    return f"bsky_{userHandle}-{userID}_{elementCreationTime}_{elementPostID}.json"


def getUserprofile(metadata):
    userHandle = metadata["user"]["handle"]
    userHandle = Helper.sanitize(userHandle)
    userHandle = userHandle.split(".")[0]
    userID = metadata["user"]["did"].split(":")[2]
    mediaName = Helper.shorten(metadata["embed"]["images"][0]["image"]["ref"].get("$link"))

    if metadata.get("subcategory") == "background":
        return f"bsky_{userHandle}-{userID}_{mediaName}_banner.{metadata.get('extension')}"

    if metadata.get("subcategory") == "avatar":
        return f"bsky_{userHandle}-{userID}_{mediaName}_avatar.{metadata.get('extension')}"


def getUserprofile_Postprocessor(metadata):
    if metadata.get("subcategory") == "info":
        userHandle = metadata.get("handle")
        userHandle = Helper.sanitize(userHandle)
        userID = metadata.get("did").split(":")[2]
        return f"bsky_{userHandle}-{userID}_profile.json"
    else:
        userHandle = metadata["user"]["handle"]
        userHandle = Helper.sanitize(userHandle)
        userHandle = userHandle.split(".")[0]
        userID = metadata["user"]["did"].split(":")[2]
        mediaName = Helper.shorten(metadata["embed"]["images"][0]["image"]["ref"].get("$link"))

        if metadata.get("subcategory") == "background":
            return f"bsky_{userHandle}-{userID}_{mediaName}_banner.json"

        if metadata.get("subcategory") == "avatar":
            return f"bsky_{userHandle}-{userID}_{mediaName}_avatar.json"
