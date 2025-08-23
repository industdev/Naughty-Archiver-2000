import pystray
from PIL import Image
import threading
from PySide6.QtCore import QMetaObject, Qt
from datetime import datetime
import time


class TrayHelper:
    def __init__(self, main):
        start = time.perf_counter()
        self.main = main
        self.inv = self.main._inv

        self.iconPath = main.iconPath
        self.trayThread = threading.Thread(target=self.initTray, daemon=True)
        self.trayThread.name = "traythread"
        self.main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")
        self.icon = pystray.Icon(
            name="NA2000",
            title="Naughty Archiver 2000",
        )

    def refreshMenu(self):
        icon = self.icon
        if icon is not None:
            icon.update_menu()

    def __submenuExtractors(self):
        #   Base
        items = [
            pystray.MenuItem("Run all", lambda: self.main.General.ui.btn_StartStop.click()),
            pystray.MenuItem("Stop all", lambda: self.inv(lambda: self.main.extractorsManager.stopExtractors())),
            pystray.Menu.SEPARATOR,
        ]

        #   Extractor submenu
        extractors = self.main._getExtractors(False)
        for extractor in extractors:
            ext = extractor["ext"]
            if ext.loopRunning:
                items.append(self.___stopitem(ext))
            else:
                items.append(self.___startitem(ext))

        return items

    def __submenuTables(self):
        #   Base
        items = [pystray.Menu.SEPARATOR]

        #   Extractor submenu
        extractors = self.main._getExtractors(False)
        for extractor in extractors:
            ext = extractor["ext"]
            items.append(self.___tableitem(ext))

        return items

    def ___startitem(self, ext):
        return pystray.MenuItem(f"Start {ext.fullName}", lambda: self.inv(lambda: ext.startExtraction()))

    def ___stopitem(self, ext):
        return pystray.MenuItem(f"Stop {ext.fullName}", lambda: self.inv(lambda: ext.stop()))

    def ___tableitem(self, ext):
        return pystray.MenuItem(f"Show {ext.fullName}", lambda: self.inv(lambda: ext.showUsersTable()))

    def initTray(self):
        try:
            image = Image.open(self.iconPath)

            #   Create menu with setup handler to refresh each time
            menu = pystray.Menu(
                lambda: (
                    pystray.MenuItem("Extractor tables", pystray.Menu(*self.__submenuTables())),
                    pystray.MenuItem("Extractor actions", pystray.Menu(*self.__submenuExtractors())),
                    pystray.Menu.SEPARATOR,
                    pystray.MenuItem("Show window", self._optTogglewindow),
                    pystray.MenuItem("Exit", self._optExit),
                )
            )

            self.icon = pystray.Icon(name="NA2000", icon=image, title="Naughty Archiver 2000", menu=menu)
            self.icon.run()
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(self.main.General.logger.error(f"Failed to initialize the tray: {e}"))

    def _optExit(self):
        QMetaObject.invokeMethod(self.main, "close", Qt.ConnectionType.QueuedConnection)  # type: ignore

    def _optTogglewindow(self):
        self.inv(self.main.tray_showWindow)

    def stop(self):
        self.main.cmd.info(f"[{datetime.now()}] Stopping tray...")
        self.icon.stop()
