from Helper import Helper


def getNormal(metadata):
    userHandle = Helper.sanitize(metadata.get("artist"))
    elementCreationTime = Helper.extractDate(metadata.get("date"))

    filename = metadata.get("filename")
    elementId = filename.split(".")[0] if filename else None

    r18 = "-R18" if metadata.get("rating") == "Adult" else ""

    return f"furaffinity_{userHandle}_{elementCreationTime}_[{elementId}{r18}].{metadata.get('extension')}"


def getNormal_Postprocessor(metadata):
    userHandle = Helper.sanitize(metadata.get("artist"))
    elementCreationTime = Helper.extractDate(metadata.get("date"))

    filename = metadata.get("filename")
    elementId = filename.split(".")[0] if filename else None

    r18 = "-R18" if metadata.get("rating") == "Adult" else ""

    return f"furaffinity_{userHandle}_{elementCreationTime}_[{elementId}{r18}].json"
