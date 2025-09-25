"""
The MIT License (MIT)

Copyright (c) 2025 Ethan Kenneth Davies

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import logging

from .prefixes import *

__all__ = (
    'set_logging',
)

default_loggers = (
    "discord.client",
    "discord.gateway",
    "discord.http",
)

log_levels = {
    10: logging.DEBUG,
    20: logging.INFO,
    30: logging.WARNING,
    40: logging.ERROR,
    50: logging.CRITICAL,
}


def set_logging(default_log_level: int = 10,
                log_level: int = None,
                loggers: list = None):
    while log_level is None:
        user_input = input(f"{QSTN_LOG} Select log level (10-50): ").strip()

        if not user_input:
            print(f"{WARN_LOG} Using default log level")
            log_level = default_log_level

        else:
            user_input = int(user_input)

            if user_input not in log_levels:
                print(f"{EROR_LOG} Select a valid input (10, 20, 30, 40, 50)")
                log_level = None

            else:
                print(f"{INFO_LOG} Log level set to {log_level}")
                log_level = user_input

    if loggers is None:
        print(f"{WARN_LOG} Using default loggers")
        loggers = default_loggers

    logging.basicConfig(level=log_level)

    for logger in loggers:
        logging.getLogger(logger).setLevel(log_level)

    print(f"{INFO_LOG} Logging set to {logging.getLevelName(log_level)}")


if __name__ == "__main__":
    set_logging()
