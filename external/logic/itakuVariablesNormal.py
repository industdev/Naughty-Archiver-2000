from Helper import Helper


def getNormal(metadata):
    userHandle = metadata.get("owner_username")
    userHandle = Helper.sanitize(userHandle)
    elementCreationTime = Helper.extractDate(metadata.get("date"))
    elementId = metadata.get("id")
    elementTitle = Helper.sanitize(metadata.get("title"))
    elementTitle = Helper.shorten(elementTitle)

    return f"itaku_{userHandle}_{elementCreationTime}_[{elementId}-{elementTitle}].{metadata.get('extension')}"


def getNormal_Postprocessor(metadata):
    userHandle = metadata.get("owner_username")
    userHandle = Helper.sanitize(userHandle)
    elementCreationTime = Helper.extractDate(metadata.get("date"))
    elementId = metadata.get("id")
    elementTitle = Helper.sanitize(metadata.get("title"))
    elementTitle = Helper.shorten(elementTitle)

    return f"itaku_{userHandle}_{elementCreationTime}_[{elementId}-{elementTitle}].json"
