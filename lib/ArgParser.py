from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from na2000 import MainApp

import argparse
import time


class ArgParser:
    def __init__(self, main: "MainApp"):
        start = time.perf_counter()

        name = main.name
        parser = argparse.ArgumentParser(description=f"{name} Commandline options")

        parser.add_argument("--hidden", action="store_true", help="Flag: Start the main window hidden")
        parser.add_argument("--runall", action="store_true", help="Flag: Start all enabled extractors when NA2000 opens")
        parser.add_argument("--debug", action="store_true", help="Flag: Output exceptions to fault.log for debugging")
        #   parser.add_argument('--runExt', nargs='+', help='Run specific extractors (e.g., --runExt Twitter Kemonoparty)')

        self.args = parser.parse_args()
        main.cmd.debug(f" :{__name__}::__init__ -> {(time.perf_counter() - start) * 1000:.6f}ms")
