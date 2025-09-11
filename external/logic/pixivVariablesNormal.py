from Helper import Helper


def getNormal(metadata):
    userHandle = metadata.get("user", {}).get("name")
    userHandle = Helper.sanitize(userHandle)

    userID = metadata.get("user", {}).get("id")
    elementCreationTime = Helper.extractDate(metadata.get("date"))

    if metadata.get("subcategory") == "avatar":
        mediaName = metadata.get("user", {}).get("profile_image_urls", {}).get("medium")
        mediaName = mediaName.split("/")[-1]
        mediaName = Helper.limit(mediaName.split("_")[1])
        return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_{mediaName}_avatar.{metadata.get('extension')}"

    elementId = metadata.get("id")
    elementTitle = Helper.sanitize(metadata.get("title"))
    if metadata.get("x_restrict"):
        R18 = "-R18"
    else:
        R18 = ""

    return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}{R18}]_{metadata.get('num')}.{metadata.get('extension')}"


def getNormal_Postprocessor(metadata):
    userHandle = metadata.get("user", {}).get("name")
    userHandle = Helper.sanitize(userHandle)
    userID = metadata.get("user", {}).get("id")
    elementCreationTime = Helper.extractDate(metadata.get("date"))

    if metadata.get("subcategory") == "avatar":
        mediaName = metadata.get("user", {}).get("profile_image_urls", {}).get("medium")
        mediaName = mediaName.split("/")[-1]
        mediaName = Helper.limit(mediaName.split("_")[1])
        return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_{mediaName}_avatar.json"

    if metadata.get("subcategory") == "background":
        mediaName = metadata.get("profile", {}).get("background_image_url")
        mediaName = mediaName.split("/")[-1]
        mediaName = Helper.limit(mediaName.split("_")[1])
        return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_{mediaName}_banner.json"

    elementId = metadata.get("id")
    elementTitle = Helper.sanitize(metadata.get("title"))
    if metadata.get("x_restrict"):
        R18 = "-R18"
    else:
        R18 = ""

    return f"pixiv_{userHandle}-{userID}_{elementCreationTime}_[{elementId}-{elementTitle}{R18}].json"
