from typing import TYPE_CHECKING, Any, Callable

from PySide6.QtCore import QMetaObject
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QWidget

from lib.ui.Download_ui import Ui_Form
from lib.Enums import MessageType, QMessageBox
from lib.ui.UserTable_manager import QKeySequence
from PySide6.QtGui import QShortcut


if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.ui.GeneralTab import General

import os
import requests
import zipfile
import shutil
from datetime import datetime
import threading
import time


class Downloader(QWidget):
    def __init__(self, main: "MainApp", safeTrash: Callable, toolsPath: str, General: "General"):
        super().__init__(None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Tools Downloader")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self).activated.connect(self.close)

        self.main = main
        self.inv = main._inv
        self.safeTrash = safeTrash
        self.toolsPath = toolsPath
        self.downloadStartTime = 0
        self.downloadedBytes = 0
        self.loading = main.loadingBar
        self.updateGdlOnly = False
        self.running = False

        #   Reference to General tab for config access
        self.settings = General.config.settings
        self.logger = General.logger

        self.latestGdlVersion = self.getToolsData()[0]["version"][0]  # Use int version for comparison
        self.currentGdlVersion = self.settings["Downloader"].get("gallery-dl", [0, "0"])[0]  # Use int version for comparison
        self.everDownloaded = self.settings["Downloader"].get("everdownloaded", False)

        self.main.qtHelper.setIcon(self.ui.btn_download, "inetcpl_4486.ico")
        self.main.qtHelper.setIcon(self, "odbcint_1439.ico")
        self.ui.btn_download.clicked.connect(self.setup)
        self.checkForPrompts()

        self.checkboxes = [self.ui.cfg_gdl, self.ui.cfg_ffmpeg, self.ui.cfg_mkvmerge]
        self.setupVersionLabels()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def getToolsData(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "gallery-dl",
                "url": "https://github.com/mikf/gallery-dl/releases/download/v1.30.5/gallery-dl_x86.exe",
                "targets": ["gallery-dl_x86.exe"],
                "renameTargets": ["gallery-dl.exe"],
                "filename": "gallery-dl.exe",
                "sha256": "e0693e86552ac7bae79ba6f382e6a26e38a3c7e7c491fa33a810f69e71d15edb",
                "version": [1305, "1.30.5"],
                "unzip": False,
            },
            {
                "name": "ffmpeg",
                "url": "https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2025-09-05-13-15/ffmpeg-N-120990-gf6bcd661f0-win64-gpl.zip",
                "targets": ["ffmpeg.exe"],
                "renameTargets": ["ffmpeg.exe"],
                "filename": "tmp_ffmpeg.zip",
                "version": [120990, "25-09-01"],
                "sha256": "fb0880736a858aa92585094738803835dad5354d1e5a9142f876d27c3d469708",
                "unzip": True,
            },
            {
                "name": "mkvmerge",
                "url": "https://mkvtoolnix.download/windows/releases/94.0/mkvtoolnix-32-bit-94.0.zip",
                "targets": ["mkvmerge.exe"],
                "renameTargets": ["mkvmerge.exe"],
                "filename": "tmp_mkvtoolnix.zip",
                "version": [94, "94.0"],
                "sha256": "8ce566bc6489899c65ba5cd36089f343a46adf9a3312801029f9af6ab458ae94",
                "unzip": True,
            },
        ]

    def setupVersionLabels(self):
        """Setup version labels for each tool"""
        tools = self.getToolsData()

        #   Prepare label pairs (current, latest), to be used in the loop
        labels = [(getattr(self.ui, f"cfg_c{i + 1}"), getattr(self.ui, f"cfg_l{i + 1}")) for i in range(3)]

        for i, tool in enumerate(tools):
            if i < len(labels):
                current, latest = labels[i]

                #   Get current version from config
                currentVer = self.settings["Downloader"].get(tool["name"], [0, "0"])
                latestVer = tool["version"]

                if currentVer[0] >= latestVer[0]:
                    current.setStyleSheet("color: rgb(58, 138, 80);")
                else:
                    current.setStyleSheet("color: rgb(138, 58, 58);")

                current.setText(f"{currentVer[1]}")
                latest.setText(f"{latestVer[1]}")

    def checkForPrompts(self):
        doPrompt = self.everDownloaded and (self.latestGdlVersion > self.currentGdlVersion)
        self.main.debuggy(
            f"doPrompt: {doPrompt}, downloaded: {self.everDownloaded}, current ver: {self.currentGdlVersion}, latest: {self.latestGdlVersion}",
            self,
        )
        if doPrompt:
            currentVerStr = self.settings["Downloader"].get("gallery-dl", [0, "0"])[1]
            latestVerStr = self.getToolsData()[0]["version"][1]

            reply = QMessageBox.question(
                None,
                "Update Available",
                f"A new version of gallery-dl is available.\n\n"
                f"Current: {currentVerStr}\n"
                f"Latest: {latestVerStr}\n\n"
                "Do you want to download it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.updateGdlOnly = True
                self.setup()
            else:
                self.settings["Downloader"]["gdlprompt"] = False

    def getRequestFileSize(self, url):
        try:
            response = requests.head(url, allow_redirects=True)
            if "content-length" in response.headers:
                return int(response.headers["content-length"])
        except:
            pass
        return None

    def download(self, url, dest, filename):
        #   Download an url and activate the loading bar
        try:
            size = self.getRequestFileSize(url)
            chunkSize = 8192

            if size:
                totalKbSize = size // 1024
                self.inv(lambda: self.loading.start(totalKbSize, f"Downloading {filename}", 50, "KB", 50))
            else:
                self.inv(lambda: self.loading.start(1000, f"Downloading {filename}", 50, "chunks", 50))

            self.downloadStartTime = time.time()
            self.downloadedBytes = 0

            response = requests.get(url, stream=True)
            response.raise_for_status()

            #   Write to file
            with open(dest, "wb") as f:
                chunkCount = 0
                lastKb = 0

                for chunk in response.iter_content(chunk_size=chunkSize):
                    if chunk:
                        f.write(chunk)
                        self.downloadedBytes += len(chunk)
                        chunkCount += 1

                        if size:
                            currentKb = self.downloadedBytes // 1024
                            increment = currentKb - lastKb
                            if increment > 0:
                                self.inv(lambda: self.loading.increase(increment))
                                lastKb = currentKb
                        else:
                            if chunkCount % 10 == 0:
                                self.inv(lambda: self.loading.increase(10))

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Failed to download {url}: {e}")
            raise

    def compareSha256(self, fpath, expectedHash):
        """Compare the SHA256 hash of a file with the expected hash
        Returns True if they match, False otherwise"""
        import hashlib

        sha256 = hashlib.sha256()
        try:
            with open(fpath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            fileHash = sha256.hexdigest()
            return fileHash.lower() == expectedHash.lower()
        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Failed to compute SHA256 for {fpath}: {e}")
            return False

    def unzip(self, zipFPath, dest):
        try:
            with zipfile.ZipFile(zipFPath, "r") as z:
                fileList = z.infolist()
                totalFiles = len(fileList)

                self.inv(
                    lambda: self.loading.start(
                        maximum=totalFiles,
                        message="Extracting files",
                        name="files",
                        interval=50,
                        minimum=1,
                    )
                )

                for file in fileList:
                    z.extract(file, dest)
                    self.inv(lambda: self.loading.increase(1))

                self.inv(lambda: self.loading.terminate())

            self.safeTrash(zipFPath)
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.qtHelper.Throw(f"Failed to extract {zipFPath}: {e}")
            self.logger.error(f"Failed to extract: {e}")

    def findAndMove(self, search_dir, targets, renameTargets):
        """
        Find and move files from the search directory to the target directory.
        """

        try:
            items = 0
            for root, dirs, files in os.walk(search_dir):
                items += len(files) + len(dirs)

            self.inv(lambda: self.loading.start(maximum=items, interval=50, message="Processing files", name="items", minimum=1))

            movedCount = 0
            for root, dirs, files in os.walk(search_dir):
                for i, target in enumerate(targets):
                    if target in files:
                        sourceFPath = os.path.join(root, target)
                        name = renameTargets[i] if i < len(renameTargets) else target
                        destFPath = os.path.join(self.toolsPath, name)

                        #   Move the file to tools root
                        if os.path.exists(destFPath):
                            self.safeTrash(destFPath)
                        shutil.move(sourceFPath, destFPath)
                        self.main.debuggy(f"Moved {target} to {name}", self)
                        movedCount += 1

                itemsInDir = len(files) + len(dirs)
                self.inv(lambda: self.loading.increase(itemsInDir))

            #   Clean up extracted directory (everything except our moved targets)
            count = 0
            for item in os.listdir(search_dir):
                itemPath = os.path.join(search_dir, item)
                if os.path.isdir(itemPath):
                    self.safeTrash(itemPath)
                    count += 1

            self.inv(lambda: self.loading.terminate())
            return movedCount

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Failed to find, remove or rename the file: {e}")
            return 0

    def getSelectedTools(self) -> list[dict[str, Any]]:
        """Get list of tools that are selected via checkboxes"""
        tools = self.getToolsData()
        if self.updateGdlOnly:
            return [tools[0]]

        selectedTools = []

        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked() and i < len(tools):
                selectedTools.append(tools[i])

        return selectedTools

    def hashMismatchQuestion(self, filename, result):
        reply = QMessageBox.question(
            self.main,
            "Hash Mismatch",
            f"The downloaded file '{filename}' has a different hash than expected.\n"
            "This could mean the file is corrupted or has been modified.\n\n"
            "Do you want to skip this file?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        result[0] = reply == QMessageBox.StandardButton.Yes

    def downloadWorker(self):
        try:
            self.running = True

            tools = self.getSelectedTools()

            if not tools:
                self.main.debuggy("No tools selected for download", self)
                self.inv(lambda: self.loading.terminate())
                return

            toolsAmount = len(tools)

            self.inv(lambda: self.loading.start(maximum=toolsAmount, interval=50, message="Setting up tools", name="tools", minimum=1))

            for tool in tools:
                #   Naming
                fileFPath = os.path.join(self.toolsPath, tool["filename"])
                filename = tool["filename"]

                self.main.debuggy(f"Downloading {filename}", self)
                self.download(tool["url"], fileFPath, f"{filename}")

                if not self.compareSha256(fileFPath, tool["sha256"]):
                    self.inv(
                        lambda: self.main.qtHelper.Throw(
                            f"SHA256 mismatch for {filename}, file may be modified or corrupted", type=MessageType.INFO
                        )
                    )

                    self.main.debuggy(f"SHA256 mismatch for {filename}", self)
                    self.logger.info(f"SHA256 mismatch for {filename}, continuing anyway")

                if tool["unzip"]:
                    self.main.debuggy(f"Extracting {filename}", self)

                    extractionDPath = os.path.join(self.toolsPath, f"tmp_extract_{filename}")
                    self.unzip(fileFPath, extractionDPath)

                    movedCount = self.findAndMove(extractionDPath, tool["targets"], tool["renameTargets"])

                    if movedCount > 0:
                        self.main.debuggy(f"Successfully moved {movedCount} files", self)

                    self.safeTrash(extractionDPath)

                else:
                    #   For direct downloads, just rename if needed
                    if tool["renameTargets"][0] != tool["filename"]:
                        newPath = os.path.join(self.toolsPath, tool["renameTargets"][0])
                        os.rename(fileFPath, newPath)
                        self.main.debuggy(f"Renamed {filename} to {tool['renameTargets'][0]}", self)

                #   Save whole version array to config after successful download
                self.settings["Downloader"][tool["name"]] = tool["version"]

                self.inv(lambda: self.loading.increase(1))

            self.inv(lambda: self.loading.terminate())
            self.logger.info("Downloads completed")

            self.updateGdlOnly = False
            self.setupVersionLabels()

        except Exception as e:
            self.main.varHelper.exception(e)
            self.logger.error(f"Failed to start download: {e}")
            self.inv(lambda: self.loading.terminate())
        finally:
            self.running = False

    def setup(self):
        os.makedirs(self.toolsPath, exist_ok=True)
        self.settings["Downloader"]["everdownloaded"] = True

        if self.running:
            return

        downloadThread = threading.Thread(target=self.downloadWorker)
        downloadThread.daemon = True
        downloadThread.start()
