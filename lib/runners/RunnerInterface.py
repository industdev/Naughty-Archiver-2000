from abc import ABC, abstractmethod
import re
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from lib.Extractor import Extractor


class RunnerInterface(ABC):
    @abstractmethod
    def getPrefix(self) -> str:
        """Return a runner prefix, used in logs to differentiate between the runner process stdout and .log commands"""
        pass

    @abstractmethod
    def getBaseConf(self, user) -> dict[str, Any]:
        """Return base configuration for extractors jobs"""
        pass

    @abstractmethod
    def deepUpdate(self, user):
        """Legacy Gallery-dl only function to update the original config with an override"""
        pass

    @abstractmethod
    def writeConfig(self, data, path):
        """Runner's own way to format a configuration file, raise an exception if needed"""
        pass

    @abstractmethod
    def getPath(self) -> str:
        """Get the full path to the exe"""
        pass

    @abstractmethod
    def getName(self) -> str:
        """Get the full runner name"""
        pass

    @abstractmethod
    def getArguments(self, extractor: "Extractor", user: dict, url: str) -> list[str]:
        """Return a string with the runner's custom format for arguments
        A series of arguments will be passed in case they are needed"""
        pass

    @abstractmethod
    def getCompiledPatterns(self) -> list[tuple[re.Pattern[str], dict[str, Any]]]:
        """Return hidden runner-specific compiled runner handler patterns, like in the Runner Handler Creator tab"""
        pass

    @abstractmethod
    def makeJobsQuick(self, jobList: list[dict], args: list) -> None:
        """Runner's own way to make a job quicker, for example removing sleep times"""
        pass
