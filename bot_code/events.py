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
from discord.ext.commands import AutoShardedBot

from .database import *
from .embeds import *
from .prefixes import *

__all__ = (
    'EventManager',
)


class EventManager:
    def __init__(self,
                 bot_instance: AutoShardedBot,
                 database_instance: DatabaseManager,
                 embed_instance: EmbedManager):
        self.bot = bot_instance
        self.db_mgr = database_instance
        self.eb_mgr = embed_instance

        events = [self.on_ready, self.on_guild_join, self.on_guild_remove]

        for event in events:
            self.bot.add_listener(event)

    async def on_ready(self):
        print(f"----------")

        print(f"{INFO_LOG} Bot user: {self.bot.user}")
        print(f"{INFO_LOG} Status: {self.bot.status}")

        await self.bot.tree.sync()
        print(f"{INFO_LOG} Synchronized application commands")

        for shard_id in range(self.bot.shard_count):
            print(f"{INFO_LOG} Shard {shard_id} is online")

        print("----------")

    async def on_guild_join(self, guild: discord.Guild):
        await self.db_mgr.add_guild(guild)

        for channel in guild.text_channels:

            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=self.eb_mgr.join_embed())
                break

    async def on_guild_remove(self, guild: discord.Guild):
        await self.db_mgr.remove_guild(guild)
