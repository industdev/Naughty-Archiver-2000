import pathvalidate
import pathlib
import random
import string
import traceback
from typing import TYPE_CHECKING, Union, Literal

if TYPE_CHECKING:
    from na2000 import MainApp


class VarHelper:
    def __init__(self, main: "MainApp"):
        self.main = main

    @staticmethod
    def randomString(n):
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=n))

    @staticmethod
    def isValidBoolean(booleanInput):
        if isinstance(booleanInput, bool):
            return True
        if isinstance(booleanInput, str):
            booleanInput = booleanInput.strip().lower()
            if booleanInput in ("1", "0", "true", "false"):
                return True
        return False

    @staticmethod
    def isValidInteger(stringInput):
        try:
            int(stringInput)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def isValidNumber(stringInput):
        try:
            float(stringInput)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def isValidFloat(stringInput):
        try:
            float(stringInput)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def isValidSingleDigit(stringInput):
        try:
            return len(str(int(stringInput))) == 1 and 0 <= int(stringInput) <= 9
        except (ValueError, TypeError):
            return False

    @staticmethod
    def isValidPath(
        pathInput: Union[str, pathlib.Path],
        allowDefault: bool = False,
        mustExist: bool = False,
        pathType: Literal["any", "file", "dir"] = "any",
    ) -> bool:
        if allowDefault and str(pathInput) == "default":
            return True

        try:
            #   Convert to string for validation
            pathStr = str(pathInput)

            #   Basic path validation using pathvalidate
            pathvalidate.validate_filepath(pathStr, platform="auto")

            #   Convert to Path object for further validation
            path = pathlib.Path(pathStr)

            #   Must be absolute path
            if not path.is_absolute():
                return False

            #   If path must exist, check existence and type
            if mustExist:
                if not path.exists():
                    return False

                if pathType == "file" and not path.is_file():
                    return False
                elif pathType == "dir" and not path.is_dir():
                    return False

        except (pathvalidate.ValidationError, OSError, ValueError, Exception):
            return False

        return True

    @staticmethod
    def isValidFPath(pathInput: Union[str, pathlib.Path], allowDefault: bool = False, mustExist: bool = True) -> bool:
        return VarHelper.isValidPath(pathInput, allowDefault, mustExist, "file")

    @staticmethod
    def isValidDPath(pathInput: Union[str, pathlib.Path], allowDefault: bool = False, mustExist: bool = True) -> bool:
        return VarHelper.isValidPath(pathInput, allowDefault, mustExist, "dir")

    @staticmethod
    def isEmpty(value):
        return isinstance(value, str) and value.strip() == ""

    def exception(self, exc: Exception, logger=None):
        path = self.main.exceptionFPath
        with open(path, "w", encoding="utf-8") as f:

            def log(msg):
                if logger:
                    logger.warning(msg)
                else:
                    print(msg)
                f.write(msg if msg.endswith("\n") else msg + "\n")

            def recurse(e):
                log("Exception Caught:")
                log(f"Type: {type(e).__name__}")
                log(f"Message: {str(e)}")
                log("".join(traceback.format_exception(type(e), e, e.__traceback__)))
                if e.__cause__:
                    log("\nCaused by:")
                    recurse(e.__cause__)
                elif e.__context__:
                    log("\nDuring handling of the above exception, another exception occurred:")
                    recurse(e.__context__)

            recurse(exc)

    @staticmethod
    def returnDictFromMatchedKeyInDictArray(toMatch, key, dict):
        for entry in dict:
            if toMatch == entry[key]:
                return entry

    @staticmethod
    def sizeFormat(bytes):
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"

    @staticmethod
    def speedFormat(bytes, elapsed):
        if elapsed > 0:
            speed_bps = bytes / elapsed
            speed_mbps = speed_bps / (1024 * 1024)
            return speed_mbps
        return 0

    @staticmethod
    def prettyJson(data) -> str:
        import json
        import re

        def stringify(obj):
            if isinstance(obj, re.Pattern):
                return obj.pattern
            if isinstance(obj, dict):
                return {str(k): stringify(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple, set)):
                return [stringify(v) for v in obj]
            #   stringify anything else
            return str(obj)

        safe = stringify(data)
        return json.dumps(safe, indent=4, ensure_ascii=False)
