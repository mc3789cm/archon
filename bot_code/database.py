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

from datetime import datetime
from typing import Optional

import discord
import aiosqlite
from unidecode import unidecode

from .prefixes import *

__all__ = (
    'DatabaseManager',
)


class DatabaseManager:
    def __init__(self, db_path: str):
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
            print(f"{INFO_LOG} Database successfully initialized")

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
            print(f"{INFO_LOG} Added guild '{unidecode(guild.name)}' to the database")

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
            print(f"{INFO_LOG} Removed guild '{unidecode(guild.name)}' from the database")

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
            print(f"{INFO_LOG} Set admin role for '{guild.name}' ({guild.id})")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to set admin role for '{guild.name}' ({guild.id}): {error}")

    async def close(self):
        if self.db:
            await self.db.close()
            self.db = None
            print(f"{WARN_LOG} Database connection closed")
