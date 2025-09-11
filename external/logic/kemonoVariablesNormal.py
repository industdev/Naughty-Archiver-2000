from Helper import Helper


def getNormal(metadata):
    userHandle = metadata.get("user_profile", {}).get("name")
    userHandle = Helper.sanitize(userHandle)
    userID = metadata.get("user_profile", {}).get("id")
    elementCreationTime = Helper.extractDate(metadata.get("date"))
    elementId = metadata.get("id")
    elementTitle = Helper.sanitize(metadata.get("title"))
    elementTitle = Helper.shorten(elementTitle)

    return f"kemono_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}].{metadata.get('extension')}"


def getNormal_Postprocessor(metadata):
    userHandle = metadata.get("user_profile", {}).get("name")
    userHandle = Helper.sanitize(userHandle)
    userID = metadata.get("user_profile", {}).get("id")
    elementCreationTime = Helper.extractDate(metadata.get("date"))
    elementId = metadata.get("id")
    elementTitle = Helper.sanitize(metadata.get("title"))
    elementTitle = Helper.shorten(elementTitle)

    return f"kemono_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}].json"
