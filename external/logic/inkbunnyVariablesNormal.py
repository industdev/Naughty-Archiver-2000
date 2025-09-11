from Helper import Helper


def getNormal(metadata):
    userHandle = metadata.get("username")
    userHandle = Helper.sanitize(userHandle)
    userID = metadata.get("user_id")
    elementCreationTime = Helper.extractDate(metadata.get("date"))
    elementId = metadata.get("submission_id")
    if metadata.get("scraps"):
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}_scrap.{metadata.get('extension')}"
    else:
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}.{metadata.get('extension')}"


def getNormal_Postprocessor(metadata):
    userHandle = metadata.get("username")
    userHandle = Helper.sanitize(userHandle)
    userID = metadata.get("user_id")
    elementCreationTime = Helper.extractDate(metadata.get("date"))
    elementId = metadata.get("submission_id")
    if metadata.get("scraps"):
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}_scrap.json"
    else:
        return f"inkbunny_{userHandle}-{userID}_{elementCreationTime}_{elementId}.json"
