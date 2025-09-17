import asyncio
from sys import exit
from os import getenv
from time import monotonic

import discord
from discord import app_commands
from discord.ext.commands import AutoShardedBot

import bot_code
from bot_code import EmbedManager, EventManager
from bot_code.logging_prefixes import *

intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.messages = True

bot = AutoShardedBot(
    owner_ids={1117890340867809340,
               1394001075547148530},
    intents=intents,
    command_prefix="?",
    case_insensitive=True,
    help_command=None,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Activity(type=discord.ActivityType.watching,
                              name="?help"),
    status=discord.Status.online)

db_mgr = bot_code.DatabaseManager(db_path="./storage/database.sqlite3")
eb_mgr = EmbedManager(bot_name="Archon")
ev_mgr = EventManager(bot_instance=bot, database_instance=db_mgr, embed_instance=eb_mgr)
# ----------------
# Prefix Commands
# ----------------
context = discord.ext.commands.Context


@bot.command()
async def help(ctx: context):
    try:
        await ctx.message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

    msg = await ctx.send(embed=eb_mgr.help_embed())

    await asyncio.sleep(120)
    try:
        await msg.delete()
    except (discord.Forbidden, discord.NotFound):
        pass


@bot.command()
async def ping(ctx: context):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    ws_latency = round(bot.latency * 1000)

    before = monotonic()
    msg = await ctx.send(embed=eb_mgr.ping_embed())
    after = monotonic()
    api_latency = round((after - before) * 1000)

    await msg.edit(embed=eb_mgr.pong_embed(
        ws_latency=ws_latency,
        api_latency=api_latency,
        sent_by=ctx.author))

    await asyncio.sleep(30)
    try:
        await msg.delete()
    except discord.Forbidden:
        pass


@bot.command()
async def shutdown(ctx: context):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    if ctx.author.id not in bot.owner_ids:
        await ctx.send(embed=eb_mgr.error_forbidden())
        return print(f"{WARN_LOG} Shutdown command called by unauthorized user: {ctx.author}")

    print(f"{INFO_LOG} Received shutdown signal from {ctx.author}.")
    await ctx.send(embed=eb_mgr.shutdown_embed(sent_by=ctx.author))
    return await stop_bot()


# ---------------
# Slash Commands
# ---------------
@bot.tree.command(name="set_admin",
                  description="Set the server-wide admin role.")
@app_commands.describe(role="The role to set as admin.")
async def set_admin(interaction: discord.Interaction, role: discord.Role):
    if interaction.guild is None:
        return await interaction.response.send_message(embed=eb_mgr.error_guild_only(),
                                                       ephemeral=True)

    if interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message(embed=eb_mgr.error_forbidden(),
                                                       ephemeral=True)

    await db_mgr.set_admin_role(role=role, guild=interaction.guild)
    return await interaction.response.send_message(embed=eb_mgr.admin_role_set(role=role.mention),
                                                   ephemeral=True)


# -----------------
# Runtime Handling
# -----------------
async def start_bot():
    token = getenv("DISCORD_TOKEN", "").strip()
    if not token:
        raise RuntimeError(f"{EROR_LOG} DISCORD_TOKEN environment variable is not set.")
    try:
        bot_code.LoggingManager(default_log_level=30, log_level=30).initialize()
        await db_mgr.initialize()
        await bot.start(token)
    except (KeyboardInterrupt, asyncio.CancelledError):
        await stop_bot()


async def stop_bot():
    print(f"{INFO_LOG} Stopping bot...")
    await bot.close()
    await db_mgr.close()
    exit(0)


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print(f"{WARN_LOG} Forced shutdown with Ctrl+C.")
