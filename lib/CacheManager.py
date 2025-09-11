from ast import Tuple
import hashlib
import json
from typing import Any, Dict, List, Optional
from collections import OrderedDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp


class CacheManager:
    def __init__(self, main: "MainApp", maxEntries: int = 40):
        """
        Initialize the cache manager.

        Args:
            maxEntries: Maximum number of entries to keep in cache
        """
        self.main = main
        self.maxEntries = maxEntries
        self.cache = OrderedDict()

    def generateKey(self, data: Any) -> tuple[str, str]:
        """
        Generate a unique cache key for any JSON serializable data.

        Args:
            data: Any JSON serializable data structure

        Returns:
            SHA256 hash of the serialized data
        """
        #   Convert to JSON string with sorted keys for consistent hashing
        dataStr = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(dataStr.encode("utf-8")).hexdigest(), dataStr

    def serveCache(self, data: Any) -> Optional[Any]:
        """
        Check if cached result exists for the given data.

        Args:
            data: The data to look up in cache

        Returns:
            Cached result if found, None otherwise
        """
        key, string = self.generateKey(data)

        if key in self.cache:
            #   Move to end (most recently used)
            result = self.cache.pop(key)
            self.cache[key] = result
            self.main.debuggy(f"Serving {key}", self)
            return result
        self.main.debuggy(f"Not Found -> {key} '{string}'", self)
        return None

    def saveCache(self, data: Any, result: Any):
        """
        Save result to cache for the given data.

        Args:
            data: The original data
            result: The computed result to cache
        """
        key, string = self.generateKey(data)
        if key in self.cache:
            return

        self.main.debuggy(f"SaveCache -> {key} '{string}'", self)

        self.cache[key] = result

        #   Remove oldest
        while len(self.cache) > self.maxEntries:
            key, value = self.cache.popitem(last=False)
            self.main.debuggy(f"Deleting key {key}", self)

    def clearCache(self):
        self.cache.clear()

    def getCacheInfo(self) -> Dict[str, Any]:
        return {"size": len(self.cache), "maxEntries": self.maxEntries, "keys": list(self.cache.keys())}
