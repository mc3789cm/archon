# MIT License
#
# Copyright (c) Ethan Kenneth Davies
__version__ = '0.1.0'

import discord
from discord.ext.commands import AutoShardedBot

from .database_manager import *
from .embed_manager import *
from .logging_prefixes import *

__all__ = ['__version__', 'EventManager']


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
