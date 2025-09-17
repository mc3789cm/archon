# MIT License
#
# Copyright (c) Ethan Kenneth Davies
__version__ = '0.1.0'

from datetime import datetime
from typing import Optional

import discord
import aiosqlite
from unidecode import unidecode

from .logging_prefixes import *

__all__ = ['__version__', 'DatabaseManager']


class DatabaseManager:
    def __init__(self, db_path: str = "../storage/database.sqlite3"):
        self.db_path: str = db_path
        self.db: Optional[aiosqlite.Connection] = None
        self.current_date = datetime.now().strftime("%Y-%m-%d | %H-%M-%S")

    async def initialize(self):
        self.db = await aiosqlite.connect(self.db_path)
        try:
            await self.db.executescript(
                """
                CREATE TABLE IF NOT EXISTS "Statistics" (
                    "Server Name" TEXT,
                    "Server ID" INTEGER NOT NULL UNIQUE,
                    "Join Date" TEXT,
                    PRIMARY KEY("Server ID")
                );
                
                CREATE TABLE IF NOT EXISTS "General Configuration" (
                    "Server ID" INTEGER NOT NULL UNIQUE,
                    "Admin Role ID" INTEGER,
                    PRIMARY KEY("Server ID")
                );
                """
            )
            await self.db.commit()
            print(f"{INFO_LOG} Database successfully initialized.")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to initialize database: {error}")

    async def add_guild(self, guild: discord.Guild):
        try:
            await self.db.execute(
                'INSERT INTO "Statistics" ("Server Name", "Server ID", "Join Date") VALUES (?, ?, ?)',
                (unidecode(guild.name), guild.id, self.current_date)
            )
            await self.db.execute(
                'INSERT INTO "General Configuration" ("Server ID") VALUES (?)',
                (guild.id,)
            )
            await self.db.commit()
            print(f"{INFO_LOG} Added guild '{unidecode(guild.name)}' to the database.")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to add guild '{unidecode(guild.name)}'/({guild.id}) to the database: {error}")

    async def remove_guild(self, guild: discord.Guild):
        try:
            await self.db.execute(
                'DELETE FROM "Statistics" WHERE "Server ID" = ?',
                (guild.id,)
            )
            await self.db.execute(
                'DELETE FROM "General Configuration" WHERE "Server ID" = ?',
                (guild.id,)
            )
            await self.db.commit()
            print(f"{INFO_LOG} Removed guild '{unidecode(guild.name)}' from the database.")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to remove guild '{guild.name}'/({guild.id}) from the database: {error}")

    async def set_admin_role(self, role: discord.Role, guild: discord.Guild):
        try:
            await self.db.execute(
                'UPDATE "General Configuration" SET "Admin Role ID" = ? WHERE "Server ID" = ?',
                (role.id, guild.id)
            )
            await self.db.commit()
            print(f"{INFO_LOG} Set admin role for '{guild.name}'/({guild.id}).")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to set admin role for '{guild.name}'/({guild.id}): {error}")

    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None
            print(f"{INFO_LOG} Database connection closed.")


if __name__ == "__main__":
    try:
        from asyncio import run
        dbm = DatabaseManager()
        run(dbm.initialize())
    except KeyboardInterrupt:
        print(f"{WARN_LOG} Forced shutdown with Ctrl+C.")