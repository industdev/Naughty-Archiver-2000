from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.Extractor import Extractor

from abc import ABC, abstractmethod
from typing import Any
from lib.ConfigManager import Configure

class ExtractorInterface(ABC):
    
    @abstractmethod
    def getCookiesSettings(self) -> tuple[int, list[str], bool]:
        pass
    
    @abstractmethod
    def getErrorlistSettings(self) -> tuple[bool, list[str], str, str]:
        pass
    
    @abstractmethod
    def getExtractorUrls(self) -> list[str]:
        pass
    
    @abstractmethod
    def getUsertableTemplate(self) -> tuple[list[list[Any]], list[str], str]:
        pass
    
    @abstractmethod
    def getUiConfiguration(self, extractor: "Extractor", main: "MainApp") -> list[dict[Configure, Any]]:
        pass
    
    @abstractmethod
    def getJobs(self, user, extSettings, generalSettings, baseConf, deepUpdate: Callable, main: "MainApp") -> tuple[list[Any], dict[str, Any]]:
        pass
    
    @abstractmethod
    def defaultJob(self, user, fullBaseConf):
        pass