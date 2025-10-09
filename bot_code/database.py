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

from .exceptions import *

__all__ = (
    'Database',
)


class Database:
    def __init__(self, database_path: str = "/opt/archon/var/db/database.sqlite3"):
        """
        Usage::

            async with Database() as db:
                await db.func()
                    ...

        Where ``func()`` is any of the methods.

        :param database_path: Path to the SQLite3 database file.
        """
        self.db_path: str = database_path
        self.db_instance: Optional[aiosqlite.Connection] = None

    async def __aenter__(self) -> "Database":
        """Open the SQLite3 database connection and return the database object.

        :return: ``Database``
        """
        if not self.db_instance:
            self.db_instance = await aiosqlite.connect(self.db_path)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the SQLite3 database connection and clean up resources.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: ``None``
        """
        if self.db_instance:
            await self.db_instance.close()

            self.db_instance = None

    async def create_db(self):
        """Creates the database schema from the SQL script in .../etc/schema.sql.

        :return: ``None``

        :raises DatabaseError: IF a fatal SQLite error occurs.
        """
        try:
            with open("/opt/archon/etc/schema.sql", "r") as db_schema:
                schema = db_schema.read()

                await self.db_instance.executescript(schema)

                await self.db_instance.commit()

        except (aiosqlite.IntegrityError, aiosqlite.ProgrammingError, aiosqlite.OperationalError) as error:
            await self.db_instance.rollback()

            raise DatabaseError(f"A fatal error occurred during database creation: {error}")

        except aiosqlite.Error as error:
            await self.db_instance.rollback()

            raise DatabaseError(f"An error occurred during database creation: {error}")

    async def add_guild(self, guild: discord.Guild):
        """Adds a new guild to the database using the provided ``discord.Guild`` object.

        Inserts a row into both the `Statistics` and `General Configuration` tables. Also inserts the current date to
        'Statistics' in YYYY-MM-DD format.

        :param guild:

        :return: ``None``

        :raises DatabaseError: If the database operation fails.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")  # Example: 2025-10-22

        try:
            await self.db_instance.execute("BEGIN TRANSACTION")

            # Unidecode is used to cleanse the guild name for non-ASCII characters.
            await self.db_instance.execute(
                'INSERT INTO "Statistics" ("Server Name", "Server ID", "Join Date") VALUES (?, ?, ?)',
                (unidecode(guild.name), guild.id, current_date)
            )
                
            await self.db_instance.execute(
                'INSERT INTO "General Configuration" ("Server ID") VALUES (?)',
                (guild.id,)
            )

            await self.db_instance.commit()

        except aiosqlite.Error as error:
            await self.db_instance.rollback()

            raise DatabaseError(f"An error occurred when adding guild {guild.name} ({guild.id}) to the database: {error}")

    async def delete_guild(self, guild: discord.Guild):
        """Uses the ``discord.Guid`` class to delete a guild and its entire configuration data from the database (used
        in the ``on_guild_remove()`` event in ``events.py``).

        :param guild:
        :return:
        """
        try:
            await self.db_instance.execute("BEGIN TRANSACTION")

            await self.db_instance.execute(
                'DELETE FROM "Statistics" WHERE "Server ID" = (?)',
                (guild.id,)
            )

            await self.db_instance.execute(
                'DELETE FROM "General Configuration" WHERE "Server ID" = (?)',
                (guild.id,)
            )

            await self.db_instance.commit()

        except aiosqlite.Error as error:
            await self.db_instance.rollback()

            raise DatabaseError(f"An error occurred when deleting guild '{guild.name}' ({guild.id}) from the database: {error}")

    async def add_admin_role(self, role: discord.Role, guild: discord.Guild):
        """Takes the ``discord.Role`` object and adds it to the database according the guild id in the ``discord.Guild``
        object.

        :param role:
        :param guild:
        :return:
        """
        try:
            await self.db_instance.execute("BEGIN TRANSACTION")

            await self.db_instance.execute(
                'UPDATE "General Configuration" SET "Admin Role ID" = ? WHERE "Server ID" = ?',
                (role.id, guild.id)
            )

            await self.db_instance.commit()

        except aiosqlite.Error as error:
            await self.db_instance.rollback()

            raise DatabaseError(f"An error occurred when updating the admin role id for guild '{guild.name}' ({guild.id}): {error}")
