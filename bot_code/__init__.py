# MIT License
#
# Copyright (c) Ethan Kenneth Davies
__version__ = "0.1.1"

from sys import hexversion as sys_version
from discord import __version__ as discord_version
from aiosqlite import __version__ as sqlite_version

from .database_manager import *
from .embed_manager import *
from .event_manager import *
from .logging_manager import *
from .logging_prefixes import *

VERSIONS = (f"Sys: {sys_version}\n"
            f"Discord.py: {discord_version}\n"
            f"SQLite: {sqlite_version}\n"
            f"Bot: {__version__}\n")

print(f"{VERSIONS}")