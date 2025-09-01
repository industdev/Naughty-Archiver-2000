from typing import TYPE_CHECKING, Callable

from lib.Enums import QMessageBox

if TYPE_CHECKING:
    from na2000 import MainApp

import os
import requests
import zipfile
import shutil
from datetime import datetime
import threading
import time


class Downloader:
    def __init__(self, main: "MainApp", safeTrash: Callable, toolsPath: str):
        self.main = main
        self.inv = main._inv
        self.safeTrash = safeTrash
        self.toolsPath = toolsPath
        self.downloadStartTime = 0
        self.downloadedBytes = 0
        self.loading = main.loadingBar
        self.forceGdlUpdate = False

        latestGdlVersion = "1.30.5"
        self.latestGdlVersion = int(latestGdlVersion.replace(".", ""))

        self.everDownloaded = self.main.General.config.settings["Downloader"]["everdownloaded"]

        currentGdlVersion = self.main.General.config.settings["Downloader"]["gdlversion"]
        self.currentGdlVersion = int(currentGdlVersion.replace(".", ""))

        self.checkForPrompts()

    def checkForPrompts(self):
        doPrompt = self.everDownloaded and (self.latestGdlVersion > self.currentGdlVersion)
        self.main.debuggy(
            f"doPrompt: {doPrompt}, downloaded: {self.everDownloaded}, current ver: {self.currentGdlVersion}, latest: {self.latestGdlVersion}",
            self,
        )
        if doPrompt:
            reply = QMessageBox.question(
                None,
                "Update Available",
                f"A new version of gallery-dl is available.\n\n"
                f"Current: {self.currentGdlVersion}\n"
                f"Latest: {self.latestGdlVersion}\n\n"
                "Do you want to download it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.forceGdlUpdate = True
                self.setup()
            else:
                self.main.General.config.settings["Downloader"]["gdlprompt"] = False

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
            chunk_size = 8192

            if size:
                totalKbSize = size // 1024
                self.inv(lambda: self.loading.start(totalKbSize, f"Downloading {filename}", 300, "KB", 50))
            else:
                self.inv(lambda: self.loading.start(1000, f"Downloading {filename}", 300, "chunks", 50))

            self.downloadStartTime = time.time()
            self.downloadedBytes = 0

            response = requests.get(url, stream=True)
            response.raise_for_status()

            #   Write to file
            with open(dest, "wb") as f:
                chunk_count = 0
                lastKb = 0

                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        self.downloadedBytes += len(chunk)
                        chunk_count += 1

                        if size:
                            currentKb = self.downloadedBytes // 1024
                            increment = currentKb - lastKb
                            if increment > 0:
                                self.inv(lambda: self.loading.increase(increment))
                                lastKb = currentKb
                        else:
                            if chunk_count % 10 == 0:
                                self.inv(lambda: self.loading.increase(10))

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.General.logger.error(f"Failed to download {url}: {e}")
            raise

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
                        interval=100,
                        minimum=1,
                    )
                )

                for i, file_info in enumerate(fileList):
                    z.extract(file_info, dest)
                    self.inv(lambda: self.loading.increase(1))

                self.inv(lambda: self.loading.terminate())

            self.safeTrash(zipFPath)
        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.General.logger.error(f"Failed to extract: {e}")

    def findAndMove(self, search_dir, targets, rename_targets):
        """
        Find and move files from the search directory to the target directory.
        """

        try:
            items = 0
            for root, dirs, files in os.walk(search_dir):
                items += len(files) + len(dirs)

            self.inv(lambda: self.loading.start(maximum=items, message="Processing files", name="items", minimum=1))

            movedCount = 0
            for root, dirs, files in os.walk(search_dir):
                for i, target in enumerate(targets):
                    if target in files:
                        sourceFPath = os.path.join(root, target)
                        name = rename_targets[i] if i < len(rename_targets) else target
                        destFPath = os.path.join(self.toolsPath, name)

                        #   Move the file to tools root
                        shutil.move(sourceFPath, destFPath)
                        self.main.debuggy(f"[{datetime.now()}] Moved {target} to {name}", self)
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
            self.main.General.logger.error(f"Failed to find, remove or rename the file: {e}")
            return 0

    def downloadWorker(self, toolsOverride=False):
        try:
            tools = [
                {
                    "url": "https://github.com/mikf/gallery-dl/releases/download/v1.30.5/gallery-dl_x86.exe",
                    "targets": ["gallery-dl_x86.exe"],
                    "renameTargets": ["gallery-dl.exe"],
                    "filename": "gallery-dl.exe",
                    "unzip": False,
                    "isGalleryDl": True,  # Add flag to identify gallery-dl
                },
                {
                    "url": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
                    "targets": ["ffmpeg.exe"],
                    "renameTargets": ["ffmpeg.exe"],
                    "filename": "tmp_ffmpeg.zip",
                    "unzip": True,
                    "isGalleryDl": False,
                },
                {
                    "url": "https://mkvtoolnix.download/windows/releases/94.0/mkvtoolnix-32-bit-94.0.zip",
                    "targets": ["mkvmerge.exe"],
                    "renameTargets": ["mkvmerge.exe"],
                    "filename": "tmp_mkvtoolnix.zip",
                    "unzip": True,
                    "isGalleryDl": False,
                },
            ]

            toolsAmount = len(tools)

            self.inv(lambda: self.loading.start(maximum=toolsAmount, message="Setting up tools", name="tools", minimum=1))

            #   Go through every tool and download it
            for i, tool in enumerate(tools, 1):
                dest = os.path.join(self.toolsPath, tool["filename"])

                #   Check if final renamed target already exists
                fName = tool["renameTargets"][0] if tool["renameTargets"] else tool["targets"][0]
                fPath = os.path.join(self.toolsPath, fName)

                #   Skip if file exists, UNLESS it's gallery-dl and we're forcing an update
                shouldSkip = os.path.exists(fPath) and not (tool.get("isGalleryDl", False) and self.forceGdlUpdate)

                if shouldSkip:
                    self.main.debuggy(f"[{datetime.now()}] Skipping {fName}", self)
                    self.main._inv(lambda: self.loading.increase(1))
                    continue

                #   If we're updating gallery-dl and it exists, remove the old version first
                if tool.get("isGalleryDl", False) and self.forceGdlUpdate and os.path.exists(fPath):
                    self.main.debuggy(f"[{datetime.now()}] Removing old {fName} for update", self)
                    self.safeTrash(fPath)

                self.main.debuggy(f"[{datetime.now()}] Downloading {tool['filename']}", self)

                self.download(tool["url"], dest, f"{tool['filename']}")

                if tool["unzip"]:
                    self.main.debuggy(f"[{datetime.now()}] Extracting {tool['filename']}", self)

                    extractrDPath = os.path.join(self.toolsPath, f"tmp_extract_{tool['filename']}")
                    self.unzip(dest, extractrDPath)

                    movedCount = self.findAndMove(extractrDPath, tool["targets"], tool["renameTargets"])

                    if movedCount > 0:
                        self.main.debuggy(f"[{datetime.now()}] Successfully moved {movedCount} files", self)

                    if os.path.exists(extractrDPath):
                        self.safeTrash(extractrDPath)

                else:
                    # For direct downloads, just rename if needed
                    if tool["renameTargets"] and tool["renameTargets"][0] != tool["filename"]:
                        newPath = os.path.join(self.toolsPath, tool["renameTargets"][0])
                        os.rename(dest, newPath)
                        self.main.debuggy(f"[{datetime.now()}] Renamed {tool['filename']} to {tool['renameTargets'][0]}", self)

                self.inv(lambda: self.loading.increase(1))

            self.inv(lambda: self.loading.terminate())
            self.main.General.logger.info("Downloads completed")
            self.main.debuggy(
                f"Gallery-dl update {self.currentGdlVersion} <- {self.latestGdlVersion}",
                self,
            )
            self.main.General.config.settings["Downloader"]["gdlversion"] = f"{self.latestGdlVersion}"

            # Reset the force update flag after completion
            self.forceGdlUpdate = False

        except Exception as e:
            self.main.varHelper.exception(e)
            self.main.General.logger.error(f"Failed to start download: {e}")
            self.inv(lambda: self.loading.terminate())

    def setup(self):
        os.makedirs(self.toolsPath, exist_ok=True)
        self.main.General.config.settings["Downloader"]["everdownloaded"] = True

        downloadThread = threading.Thread(target=self.downloadWorker)
        downloadThread.daemon = True
        downloadThread.start()
