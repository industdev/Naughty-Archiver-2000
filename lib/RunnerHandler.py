import json
from typing import TYPE_CHECKING

from lib.Enums import EventNames, Handlers, HandlersActions, LogLevel, MessageType, Return
from lib.RunnerEvents import RunnerEvents
from lib.VarHelper import VarHelper

if TYPE_CHECKING:
    from na2000 import MainApp
    from lib.RunnerManager import RunnerManager
    from lib.runners.RunnerInterface import RunnerInterface
import re
import time


class RunnerHandler:
    def __init__(
        self,
        main: "MainApp",
        runnerManager: "RunnerManager",
        errorBoxesEnabled: bool,
        extErroredConfig,
        stopTrigger: int,
        runner: "RunnerInterface",
    ):
        start = time.perf_counter()
        self.main = main
        self.inv = main._inv

        self.gallery = runnerManager
        self.runner = runner
        self.extractor = self.gallery.extractor

        self.errorBoxesEnabled = errorBoxesEnabled
        self.extErroredConfig = extErroredConfig
        self.errorCounter = 0
        self.stopTrigger = stopTrigger

        #   Track how many times each pattern has occurred
        #   Track the line number when each pattern last occurred
        #   Track total lines for resetAt functionality
        self.patternCounters = {}
        self.totalLinesProcessed = 0
        self.lastPatternLine = {}

        self.lastErrorID = ""
        self.currentErrorID = ""
        self.compiledPatterns = []
        self.gallery.reloadPatterns = True
        self.compiledExtPatterns = []
        toCompile = self.extractor.settings.getOutputHandlingCases()
        if len(toCompile) > 0:
            self.main.debuggy("Compiling extractor patterns", self.extractor.configName)
            self.compiledExtPatterns: list[tuple[re.Pattern[str], dict]] = self.main.General.runnerHandlerCreator.compile(
                toCompile=toCompile, classe=self.extractor
            )
        self._compileErrorPatterns()
        self.main.cmd.debug(f" :{__name__}::__init__ ->{(time.perf_counter() - start) * 1000:.6f}ms")

        # threading.Timer(2.0, self.levelChanger, args=("[g-dl][debug] Cursor: DAAFCgABGyTMlmw__9ULAAIAAABcRW1QQzZ3QUFBZlEvZ0dKTjB2R3AvQUFBQUFZYkkydm5GWnFRWUJzaWhyck5taEh3R3lLR2w3dFdVTDRiSXh6UFJwc2hCUnNpbllBNldtQWNHeUtISkNKV2tZZz0IAAMAAAACAAA",)).start()

    def newRun(self):
        self.lastErrorID = self.currentErrorID
        self.currentErrorID = ""
        self.errorBoxesEnabled = self.main.General.config.settings["errorboxes"]

    def reloadPatterns(self):
        try:
            compiledPatterns: list[tuple[re.Pattern[str], dict]] = self.main.General.runnerHandlerCreator.compile()
            compiledRunnerPatterns: list[tuple[re.Pattern[str], dict]] = self.runner.getCompiledPatterns()
            self.compiledPatterns: list[tuple[re.Pattern[str], dict]] = self.compiledExtPatterns + compiledPatterns + compiledRunnerPatterns
            self.main.debuggy(VarHelper.prettyJson(self.compiledPatterns), self.extractor.configName)
            self.inv(lambda: self.extractor.logger.info("Reloaded output patterns"))
        except Exception as e:
            ext = e
            self.main.varHelper.exception(ext)
            self.inv(lambda: self.extractor.logger.error(f"Failed to reload output patterns: {ext}"))
            raise

    #   Used to compile any errored url pattern that is in the extractor's configuration
    def _compileErrorPatterns(self):
        self.errorPatterns = []
        if self.extErroredConfig:
            for pattern in self.extErroredConfig[1]:
                try:
                    compiled_pattern = re.compile(pattern, re.IGNORECASE)
                    self.errorPatterns.append(compiled_pattern)
                except re.error as e:
                    self.inv(lambda err=e, pat=pattern: self.extractor.logger.warning(f"Failed to compile error pattern '{pat}': {err}"))

    def _checkErrorPatterns(self, rawline):
        try:
            if not self.extErroredConfig or not self.errorPatterns:
                return False

            for pattern in self.errorPatterns:
                match = pattern.search(rawline.lower())
                if match:
                    #   Call RunnerEvents.addERRORED_URL with the matched line
                    data, error = RunnerEvents.addErroredUrl(
                        self.main.debuggy, rawline, self.extErroredConfig, self.extractor.user.get("UserHandle", "unknown")
                    )

                    if data:
                        self.inv(lambda url=data.get("url", "unknown"): self.extractor.logger.debug(f"Errored: {url}"))
                    elif error != "duplicate":
                        self.inv(lambda: self.extractor.logger.debug(f"Error adding errored URL data: {error}"))
                    return True

            return False
        except Exception as e:
            self.main.varHelper.exception(e)
            self.inv(lambda: self.extractor.logger.error(f"Faulty line: {rawline}"))
            self.inv(lambda: self.extractor.logger.error(f"_checkErrorPatterns Exception: {e}"))
            return False

    def _handleIds(self, id: EventNames | str, rawline: str):
        try:
            #   API Stat
            if id == EventNames.API_CALL.name:
                self.inv(lambda: RunnerEvents.apicall(self.main.debuggy, self.main))
            #   Updates the user cursor to the output of extractCursorValue
            elif id == EventNames.UPDATE_CURSOR.name:
                if self.extractor.cursorExtractionEnabled and not self.extractor.inhibitCursorUpdate:
                    value = self.extractCursorValue(rawline)
                    if value != None and value != "None":
                        self.inv(lambda v=value: RunnerEvents.updateCursor(self.main.debuggy, self.extractor, v, self.gallery))
            #   Sets the user cursor to an empty string
            elif id == EventNames.RESET_CURSOR.name:
                if self.extractor.cursorExtractionEnabled:
                    self.inv(lambda: RunnerEvents.updateCursor(self.main.debuggy, self.extractor, "", self.gallery))
                    self.extractor.resetConfigCursor = True

                    if self.setAndCheckErrorID("RESET_CURSOR_FAIL"):
                        self.extractor.logger.warning("Skipping job as resetting the cursor didn't fix the problem")
                        self.gallery.skip()
                    else:
                        self.gallery._stop(Return.ERR_GALLERY_RETRY)

            elif id == EventNames.USER_NOTFOUND.name:
                self.inv(lambda: RunnerEvents.setUserToSkip(self.main.debuggy, self.gallery))
            elif id == EventNames.CONVERT_TO_GIF.name:
                self.inv(lambda: RunnerEvents.convertToGif(self.main.debuggy, self.main, self.extractor, rawline))
            elif id == EventNames.TIMESTAMP.name:
                self.inv(lambda: RunnerEvents.updateTimestamp(self.main.debuggy, self.main, self.extractor, rawline))

        except Exception as e:
            raise Exception(f"_handleIds -> {e}")

    def _updatePatternCounter(self, patternName, config):
        #   Initialize counter if it doesn't exist
        if patternName not in self.patternCounters:
            self.patternCounters[patternName] = 0

        self.patternCounters[patternName] += 1
        self.lastPatternLine[patternName] = self.totalLinesProcessed

        #   Handle resetAt logic for all patterns
        resetAt: int = config.get(Handlers.RESET_AT.name)
        if resetAt is not None:
            #   Check if enough lines have passed since this pattern last occurred
            linesSinceOccurrence: int = self.totalLinesProcessed - self.lastPatternLine.get(patternName, 0)
            if linesSinceOccurrence >= resetAt:
                self.patternCounters[patternName] = 0
                self.lastPatternLine[patternName] = self.totalLinesProcessed
                self.inv(lambda: self.extractor.logger.debug(f"Counters reset for pattern: {patternName}"))
            self.main.debuggy(f"patternCounters for {patternName}: {self.patternCounters[patternName]}", self)
            self.main.debuggy(f"lastPatternLine for {patternName}: {self.lastPatternLine[patternName]}", self)

    def _shouldTriggerAction(self, patternName, actionValue):
        #   If action is boolean True, always trigger
        if actionValue is True:
            return True

        #   If action is boolean False or None, never trigger
        if actionValue is False or actionValue is None:
            return False

        #   If action is an integer, check if the counter has reached the threshold
        if isinstance(actionValue, int):
            current = self.patternCounters.get(patternName, 0)
            self.main.debuggy(f"_shouldTriggerAction -> {current} >= {actionValue}: {current >= actionValue}", self)
            return current >= actionValue

        #   Return False for any other type
        return False

    def levelChanger(self, rawline: str) -> str:
        # start = time.perf_counter()
        try:
            self.totalLinesProcessed += 1
            #   First check for error patterns and trigger RunnerEvents.addERRORED_URL
            self._checkErrorPatterns(rawline)

            #   Check merged patterns
            pIdentifier = None
            for pattern, config in self.compiledPatterns:
                if pattern.search(rawline):
                    #   Check mask, continue if the mask doesn't match the current extractor operation or runner type
                    stateMask = config.get(Handlers.STATEMASK.name)
                    runnerMask = config.get(Handlers.RUNNERMASK.name)

                    if self.main.debug:
                        self.debugPrint(config, rawline, pattern)

                    if stateMask:
                        if not any(stateMask == enum.name for enum in self.extractor.currentOperations):
                            continue

                    if runnerMask:
                        if runnerMask != self.gallery.runnerPrefix:
                            continue

                    pIdentifier = pattern.pattern
                    break

            if not pIdentifier:
                short = (rawline[:35] + "...") if len(rawline) > 60 else rawline
                self.main.debuggy(f"{short} -> Did not match anything", self)
                return LogLevel.WHITE.name

            #   Read pattern configuration
            level = config.get(Handlers.LINE_LEVEL.name)
            messageOnAction = config.get(Handlers.MESSAGE_ON_ACTION.name)
            messageOnLine = config.get(Handlers.MESSAGE_ON_LINE.name)
            inhibitBox = config.get(Handlers.INHIBIT_BOX.name)
            action: list = config.get(Handlers.ACTION.name, [None, None])
            rAction = config.get(Handlers.REPEATED_ACTION.name)
            if not rAction:
                rAction = action[0]

            id = config.get(Handlers.EVENT.name)

            if level is None:
                return LogLevel.WHITE.name

            if level == LogLevel.RED.name:
                self.inv(lambda: self.extractor.scrollingLabel.errorTrigger())
                self.increaseErrorCounter()

            #   Update pattern counter to handle resetAt logic
            self._updatePatternCounter(pIdentifier, config)

            #   Show message every time pattern is encountered
            if messageOnLine and not inhibitBox:
                if self.errorBoxesEnabled and not inhibitBox:
                    if level == "RED":
                        self.main.qtHelper.Throw(self.boxReplace(messageOnLine), logger=self.extractor.logger, type=MessageType.CRITICAL)
                    elif level == "YELLOW":
                        self.main.qtHelper.Throw(self.boxReplace(messageOnLine), logger=self.extractor.logger, type=MessageType.WARNING)
                    elif level == "WHITE":
                        self.main.qtHelper.Throw(self.boxReplace(messageOnLine), logger=self.extractor.logger, type=MessageType.INFO)
                else:
                    self.inv(lambda: self.extractor.logger.log(messageOnLine.replace("\n", "").replace("\r", ""), level))

            if id:
                self._handleIds(id, rawline)

            #   Check if we should stop/skip based on counter and track if any action was taken
            actionTaken = False

            if action:
                actionType, actionTrigger = action

                #   Check if the conditions are met to trigger this action
                if self._shouldTriggerAction(pIdentifier, actionTrigger):
                    current = self.patternCounters.get(pIdentifier, 0)
                    actionTaken = True

                    #   Same identifier if it's the same pattern
                    id = json.dumps(config, separators=(",", ":"))
                    #   If we set the id before this job and this returns true, the action will change so we change actionType
                    if self.setAndCheckErrorID(id):
                        actionType = rAction

                    #   Perform the specific action based on its type
                    if actionType == HandlersActions.STOP.name:
                        self.inv(lambda: self.extractor.logger.debug(f"Stopping extraction based on output (occurrence #{current})"))
                        self.gallery._stop("Error during the extraction")

                    elif actionType == HandlersActions.SKIP_JOB.name:
                        self.inv(lambda: self.extractor.logger.debug(f"Skipping job based on output (occurrence #{current})"))
                        self.gallery.skip()

                    elif actionType == HandlersActions.SKIP_USER.name:
                        self.inv(lambda: self.extractor.logger.debug(f"Skipping user based on output (occurrence #{current})"))
                        self.gallery.skipUser()

                    elif actionType == HandlersActions.RETRY_JOB.name:
                        self.inv(lambda: self.extractor.logger.debug(f"Retrying job based on output (occurrence #{current})"))
                        self.gallery._stop(Return.ERR_GALLERY_RETRY)
                    else:
                        self.inv(lambda: self.extractor.logger.warning(f"Action not take as it was unavailable -> {actionType}"))
                        actionTaken = False

            #   Show message only when an action was taken
            if messageOnAction and actionTaken:
                if self.errorBoxesEnabled and not inhibitBox:
                    self.main.qtHelper.Throw(self.boxReplace(messageOnAction), self.extractor.logger)
                else:
                    self.inv(lambda: self.extractor.logger.log(messageOnAction.replace("\n", "").replace("\r", ""), level))

            return level
        except Exception as e:
            raise Exception(f"GalleryOutputHandler::levelChanger -> Error while handling the output: {e}")
        # finally:
        #    end = time.perf_counter()
        #    elapsed = end - start
        #    print(f'{elapsed*1000:.6f} ms')

    def extractCursorValue(self, line: str):
        pattern = re.compile(
            r"(?:\[g-dl\]\[info\]\s*Use\s+'-o\s+cursor=(\d+)"
            r"|\[g-dl\]\[debug\]\s*cursor:\s*([^\s]+))",
            flags=re.IGNORECASE,
        )

        match = pattern.search(line)
        if match:
            return match.group(1) or match.group(2)
        return None

    def increaseErrorCounter(self):
        self.errorCounter += 1
        self.main.debuggy(f"increaseErrorCounter -> {self.errorCounter} {self.stopTrigger} {self.extractor.configName}", self)
        if self.errorCounter >= self.stopTrigger:
            self.gallery._stop("Too many errors happened in 1 minute, please report if anything is broken")
            self.main.qtHelper.Throw(
                "Too many errors happened in 1 minute, please report if anything is broken",
                title=f"{self.extractor.fullName} Forced stop",
            )

    def debugPrint(self, config, rawline, pattern):
        extMask = ", ".join([enu.name for enu in self.extractor.currentOperations])
        stateMask = config.get(Handlers.STATEMASK.name)
        runnerMask = config.get(Handlers.RUNNERMASK.name)
        short = rawline.replace("[g-dl]", "")
        short = (short[:35] + "...") if len(short) > 60 else short

        if runnerMask or stateMask:
            self.main.debuggy(f"{short} ->  runnerMask: {runnerMask} stateMask: {stateMask} extractor: {extMask}", self)
        self.main.debuggy(
            f"{short} -> {config[Handlers.LINE_LEVEL.name]}::{pattern.pattern}, MSG: {config.get(Handlers.MESSAGE_ON_LINE.name)} EVT: {config.get(Handlers.EVENT.name)} ACT: {config.get(Handlers.ACTION.name)}",
            self,
        )

    def setAndCheckErrorID(self, error):
        """
        Checks if last and new current error, passed as string, is the same
        If it's the same then return true otherwise false
        Only run this function if you then change job
        """
        self.main.debuggy(f"setAndCheckErrorID -> set {self.currentErrorID}", self)
        self.currentErrorID = error
        if self.lastErrorID == self.currentErrorID:
            return True
        else:
            return False

    def boxReplace(self, str):
        str = str.replace("{user}", self.extractor.user.get("UserHandle"))
        str = str.replace("{runner}", self.runner.getName())
        str = str.replace("{extractor}", self.extractor.name)
        return str
