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

__author__ = 'Ethan Kenneth Davies'
__title__ = 'Archon'
__version__ = '0.1.2'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2025 Ethan Kenneth Davies'

import os
import asyncio
from typing import NamedTuple, Literal

from .commands import *
from .config import *
from .database import *
from .embeds import *
from .events import *
from .prefixes import *
from .set_logging import *
from .start import *
from .stop import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    release_rating: Literal['bronze', 'silver', 'gold']


version_info: VersionInfo = VersionInfo(major=0, minor=1, patch=2, release_rating="silver")

ARCHON_ASCII = [
    f"{__title__} v{__version__}\n"
    r"  __   ____   ___  _  _   __   __ _  ",
    r" / _\ (  _ \ / __)/ )( \ /  \ (  ( \ ",
    r"/    \ )   /( (__ ) __ ((  O )/    / ",
    r"\_/\_/(__\_) \___)\_)(_/ \__/ \_)__) ",
    f"{__copyright__}\n",
]


async def print_intro(run: bool = False):
    if run:

        os.system("clear")
        print("\n")

        for line in ARCHON_ASCII:
            await asyncio.sleep(0.325)
            print(line)

    if not run:
        pass

asyncio.run(print_intro(config.PRINT_INTRO))
