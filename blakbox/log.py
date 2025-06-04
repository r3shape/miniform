from .utils import box_path
from .globals import os, datetime

# ------------------------------------------------------------ #
class BOXlogger:
    COLORS = {
        "INFO": "\033[92m",     # Green
        "ERROR": "\033[91m",    # Red
        "DEBUG": "\033[94m",    # Blue
        "WARNING": "\033[93m",  # Yellow
        "RESET": "\033[0m"      # Reset
    }

    @staticmethod
    def _log(message: str, level: str = "INFO", out: bool = False) -> None:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fmt = f"[{time}] [{level}] {message}"
        msg = f"{BOXlogger.COLORS.get(level, '')}{fmt}{BOXlogger.COLORS['RESET']}"
        print(msg)

    @staticmethod
    def info(message, out: bool = False) -> None: BOXlogger._log(message, "INFO", out)

    @staticmethod
    def error(message, out: bool = False) -> None: BOXlogger._log(message, "ERROR", out)

    @staticmethod
    def debug(message, out: bool = False) -> None: BOXlogger._log(message, "DEBUG", out)

    @staticmethod
    def warning(message, out: bool = False) -> None: BOXlogger._log(message, "WARNING", out)
# ------------------------------------------------------------ #