from miniform.imports import os, datetime

# ------------------------------------------------------------ #
class MiniLogger:
    COLORS = {
        "INFO": "\033[92m",     # Green
        "ERROR": "\033[91m",    # Red
        "DEBUG": "\033[94m",    # Blue
        "WARNING": "\033[93m",  # Yellow
        "RESET": "\033[0m"      # Reset
    }

    DEBUG_MODE: bool = True

    @staticmethod
    def _log(message: str, level: str = "INFO", out: bool = False) -> None:
        if not MiniLogger.DEBUG_MODE and level != "ERROR": return
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fmt = f"[{time}] [{level}] {message}"
        msg = f"{MiniLogger.COLORS.get(level, '')}{fmt}{MiniLogger.COLORS['RESET']}\n"
        print(msg)

    @staticmethod
    def info(message, out: bool = False) -> None: MiniLogger._log(message, "INFO", out)

    @staticmethod
    def error(message, out: bool = False) -> None: MiniLogger._log(message, "ERROR", out)

    @staticmethod
    def debug(message, out: bool = False) -> None: MiniLogger._log(message, "DEBUG", out)

    @staticmethod
    def warning(message, out: bool = False) -> None: MiniLogger._log(message, "WARNING", out)
# ------------------------------------------------------------ #
