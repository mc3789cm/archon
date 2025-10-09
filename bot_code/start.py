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
from .exceptions import *
from .prefixes import *
from .set_logging import *

__all__ = (
    'start_bot',
    'default_bot',
    'default_database',
)

intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.messages = True

# AutoShardedBot is used for better scaling.
default_bot = commands.AutoShardedBot(
    owner_ids=VALUES.OWNER_IDS,
    intents=intents,
    command_prefix=VALUES.COMMAND_PREFIX,
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="?help"),
    status=discord.Status.online
)

default_database = Database()

embeds_default = Embeds()


async def start_bot(bot_instance: commands.AutoShardedBot = default_bot, database_instance: Database = default_database,
                    embeds_instance: Embeds = embeds_default):
    set_logging(log_level=30, default_log_level=20)

    print(f"{INFO_LOG} Starting bot...")

    prefix_cmds = PrefixCommands(bot_instance=bot_instance,
                                 embed_instance=embeds_instance,
                                 database_instance=database_instance)

    slash_cmds = SlashCommands(bot_instance=bot_instance,
                               embed_instance=embeds_instance,
                               database_instance=database_instance)

    events = Events(bot_instance=bot_instance,
                    embed_instance=embeds_instance,
                    database_instance=database_instance)

    try:
        async with database_instance as db:
            await db.create_db()

    except DatabaseError as error:
        print(f"{EROR_LOG} {error}")

    await bot_instance.add_cog(slash_cmds)

    await bot_instance.start(VALUES.TOKEN)
