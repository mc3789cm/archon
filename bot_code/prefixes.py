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

__all__ = (
    'QSTN_LOG',
    'INFO_LOG',
    'WARN_LOG',
    'EROR_LOG',
    'CRIT_LOG',
)

QSTN_LOG = "[ \033[1;37mQSTN\033[0m ]"
"""- QSTN_LOG: Waiting for user input."""
INFO_LOG = "[ \033[0;32mINFO\033[0m ]"
"""- INFO_LOG: Routine information."""
WARN_LOG = "[ \033[0;33mWARN\033[0m ]"
"""- WARN_LOG: Unexpected, but non-breaking event."""
EROR_LOG = "[ \033[0;31mEROR\033[0m ]"
"""- EROR_LOG: Error that stops a function."""
CRIT_LOG = "[ \033[1;31mCRIT\033[0m ]"
"""- CRIT_LOG: Critical error that stops the entire program."""

if __name__ == "__main__":
    print(QSTN_LOG, INFO_LOG, WARN_LOG, EROR_LOG, CRIT_LOG)
