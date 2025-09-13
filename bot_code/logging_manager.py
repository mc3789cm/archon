import logging

from .logging_prefixes import *


class LoggingManager:
    def __init__(self,
                 default_log_level: int = 20,
                 log_level: int = None,
                 loggers: list = None):
        self.default_logging_level = default_log_level
        self.log_level = log_level
        if loggers is None:
            loggers = ["discord.client", "discord.gateway", "discord.http"]
        self.loggers = loggers

    def initialize(self):
        log_levels = {
            10: logging.DEBUG,
            20: logging.INFO,
            30: logging.WARNING,
            40: logging.ERROR,
            50: logging.CRITICAL
        }
        
        while self.log_level is None:
            user_input = input(f"{QSTN_LOG} Select log level (10-50): ").strip()
            if user_input == "":
                self.log_level = self.default_logging_level
                break
            try:
                input_level = int(user_input)
                if input_level not in log_levels:
                    print(f"{EROR_LOG}: RangeError: Select a number (10-50)")
                    self.log_level = None
                else:
                    self.log_level = input_level
                    break
            except ValueError:
                print(f"{EROR_LOG}: ValueError: Select a number (10-50)")

        if self.log_level is not None:
            logging.basicConfig(level=self.log_level)
        for logger in self.loggers:
            logging.getLogger(logger).setLevel(self.log_level)

        print(f"{INFO_LOG} Logging set to {logging.getLevelName(self.log_level)}")


if __name__ == "__main__":
    try:
        LoggingManager().initialize()
    except KeyboardInterrupt:
        print(f"{WARN_LOG} Forced shutdown with Ctrl+C.")
