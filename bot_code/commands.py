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

import asyncio
from time import monotonic

import discord
from discord.ext import commands

from .prefixes import *
from .database import *
from .embeds import *
from .exceptions import *
from .stop import *

__all__ = (
    'PrefixCommands',
    'SlashCommands',
)

Context = commands.Context


async def delete_message(ctx: Context, embed_instance: Embeds):
    try:
        await ctx.message.delete()

    except discord.NotFound:
        pass

    except discord.Forbidden:
        await ctx.send(embed=embed_instance.error_server_forbidden())


class PrefixCommands:
    def __init__(self, bot_instance: commands.AutoShardedBot, embed_instance: Embeds, database_instance: Database):
        """Prefix commands are commands initiated by using a prefix preceding the name of the command (no whitespace),
        i.e., ``?help``, ``!ping``, ``$shutdown``.

        The value of the prefix is dictated by the ``command_prefix`` value in the configuration file.

        :param bot_instance:
        :param embed_instance:
        :param database_instance:

        :return: None
        """
        self.bot = bot_instance
        self.embeds = embed_instance
        self.database = database_instance

        # Register each method as a command
        @self.bot.command()
        async def help(ctx: Context):
            await self.help(ctx)

        @self.bot.command()
        async def ping(ctx: Context):
            await self.ping(ctx)

        @self.bot.command()
        async def shutdown(ctx: Context):
            await self.shutdown(ctx)

    async def help(self, ctx: Context):
        """This command sends the help embed to the invoking user before deleting it after a delay.

        :param ctx: The context of the command invocation. This includes metadata like the user who invoked it and what
            channel it was invoked from.
        :type ctx: Context

        :return: None
        """
        await delete_message(ctx=ctx, embed_instance=self.embeds)

        msg = await ctx.send(embed=self.embeds.help_embed())

        await asyncio.sleep(120)
        await msg.delete()

    async def ping(self, ctx: Context):
        """This command sends the API and WebSocket latencies to the user, then deletes it after a delay.

        The API latency is calculated by recording a high-resolution timestamp before sending a placeholder embed, then
        another timestamp is stored. The difference between these timestamps represents the time taken to send the
        message while accounting for network and API overhead (API latency). This value is multiplied by 1000 and
        rounded to produce a human-readable latency in milliseconds.

        :param ctx: The context of the command invocation. This includes metadata like the user who invoked it and what
            channel it was invoked from.
        :type ctx: Context

        :return: None
        """
        await delete_message(ctx=ctx, embed_instance=self.embeds)

        before = monotonic()
        msg = await ctx.send(embed=self.embeds.ping_embed())
        after = monotonic()

        ws_latency = round(self.bot.latency * 1000)  # Milliseconds

        api_latency = round((after - before) * 1000)  # Milliseconds

        await msg.edit(embed=self.embeds.pong_embed(
            ws_latency=ws_latency,
            api_latency=api_latency,
            sent_by=ctx.author))

        await asyncio.sleep(120)
        await msg.delete()

    async def shutdown(self, ctx: Context):
        """This command checks if the invoking user ID matches one of the user ID's in the ``bot.owner_ids`` list. The
        values in this list are dictated by the ``owner_ids`` value in the configuration. If the user
        ID does match one of the entries in ``bot.owner_ids``, call the ``stop_bot()`` function (See ``stop.py``). If it
        doesn't, send an appropriate error message back to the invoking user.

        :param ctx: The context of the command invocation. This includes metadata like the user who invoked it and what
            channel it was invoked from.
        :type ctx: Context

        :return: None
        """
        await delete_message(ctx=ctx, embed_instance=self.embeds)

        if ctx.author.id not in self.bot.owner_ids:
            await ctx.send(embed=self.embeds.error_client_forbidden())

            print(f"{WARN_LOG} Shutdown command called by unauthorized user: {ctx.author}")

            return

        print(f"{INFO_LOG} Received shutdown signal from {ctx.author}")

        await ctx.send(embed=self.embeds.shutdown_embed(sent_by=ctx.author))

        await stop_bot(bot_instance=self.bot, database_instance=self.database)


class SlashCommands(commands.Cog):
    def __init__(self, bot_instance: commands.AutoShardedBot, database_instance: Database, embed_instance: Embeds):
        self.embeds = embed_instance
        self.bot = bot_instance
        self.database = database_instance

    @discord.app_commands.command(name="set_admin", description="Set the server-wide admin role.")
    @discord.app_commands.describe(role="The role to set as admin.")
    async def set_admin(self, interaction: discord.Interaction, role: discord.Role):
        """This command lets only the guild owner set the admin role for their guild-specific configuration in the
        database.

        :param interaction:
        :param role:

        :return: None

        :except DatabaseError:
        """

        send_message = interaction.response.send_message

        if interaction.guild is None:
            await send_message(embed=self.embeds.error_guild_only(), ephemeral=True)

            return

        if interaction.user.id != interaction.guild.owner_id:
            await send_message(embed=self.embeds.error_client_forbidden(), ephemeral=True)

            return
        try:
            async with self.database as db:
                await db.add_admin_role(role=role, guild=interaction.guild)

                print(f"{INFO_LOG} Updated the admin role for guild '{interaction.guild.name}' in the database")

        except DatabaseError as error:
            print(f"{EROR_LOG} {error}")

        await send_message(embed=self.embeds.admin_role_set(role=role.mention), ephemeral=True)

        return
