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

import discord
from discord.ext import commands

from .commands import *
from .config import *
from .database import *
from .embeds import *
from .events import *
from .prefixes import *
from .set_logging import *
from .stop import *

__all__ = (
    'start_bot',
    'db_mgr',
    'bot',
)

intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.messages = True

bot = commands.AutoShardedBot(
    owner_ids=config.OWNER_IDS,
    intents=intents,
    command_prefix=config.CMD_PREFIX,
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="?help"),
    status=discord.Status.online
)

db_mgr = DatabaseManager(config.DB_PATH)

eb_mgr = EmbedManager(bot_name="Archon")


async def start_bot(bot_instance: commands.AutoShardedBot = bot, database_instance: DatabaseManager = db_mgr):
    set_logging(log_level=30, default_log_level=20)

    print(f"{INFO_LOG} Starting bot...")

    prefix_cmd_mgr = PrefixCommandsManager(bot_instance=bot_instance,
                                           embed_instance=eb_mgr,
                                           database_instance=db_mgr)

    slash_cmd_mgr = SlashCommandsManager(bot_instance=bot_instance,
                                         embed_instance=eb_mgr,
                                         database_instance=db_mgr)
    await db_mgr.initialize()
    await bot_instance.add_cog(slash_cmd_mgr)

    ev_mgr = EventManager(bot_instance=bot_instance,
                          embed_instance=eb_mgr,
                          database_instance=db_mgr)

    await bot_instance.start(config.TOKEN)
