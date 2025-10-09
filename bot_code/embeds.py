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

from discord import Embed, User

__all__ = (
    'Embeds',
)


class Embeds:
    def __init__(self, primary_color: str = "#1793d1", error_color: str = "#dc143c",
                 bot_name: str = "Bot"):

        # Convert hex color strings to integers
        self.primary_color: int = int(primary_color.lstrip("#"), 16)
        self.error_color: int = int(error_color.lstrip("#"), 16)
        self.bot_name = bot_name

    def join_embed(self) -> Embed:
        return Embed(
            title="Hey!",
            description=f"I'm {self.bot_name}, an all-in-one Discord utility, "
                        "being only as complex or as simple as you would like me to be. "
                        "Get started by running `?help`",
            color=int(self.primary_color,)
        )

    def help_embed(self) -> Embed:
        return Embed(
            title="Help Menu",
            description=f"{self.bot_name} is an all-in-one Discord utility, "
                        "being only as complex or as simple as the admin tailors it to be.",
            color=int(self.primary_color,)
        ).add_field(
            name="Prefix Commands: (\"?\")",
            value=f"`?help` - Displays this help message.\n"
                  f"`?ping` - Outputs {self.bot_name}'s websocket and API latencies in milliseconds (`ms`).",
            inline=False
        ).add_field(
            name="Slash Commands: (\"/\")",
            value="`/set_admin` - Sets the server *server-wide* admin role.\n"
                  "This is used to restrict all of the following commands to just "
                  "the set admin role:\n"
                  "   - `command_one`\n- `command_two`\n- `command_three`",
            inline=False
        )

    def ping_embed(self) -> Embed:
        return Embed(
            title="Pinging...",
            color=int(self.primary_color,)
        )

    def pong_embed(self, ws_latency: int, api_latency: int, sent_by: User) -> Embed:
        return Embed(
            title="Pong",
            description=f"**Websocket Latency:** `{ws_latency}ms`\n"
                        f"**API Latency:** `{api_latency}ms`",
            color=int(self.primary_color,)
        ).set_footer(text=f"Ping issued by: `{sent_by}`")

    def shutdown_embed(self, sent_by: User) -> Embed:
        return Embed(
            title="Shutting down...",
            description=f"{self.bot_name} is going to shut down now.",
            color=int(self.primary_color,)
        ).set_footer(text=f"Shutdown issued by: {sent_by}")

    def admin_role_set(self, role: str) -> Embed:
        return Embed(
            title="Admin Role Is Set",
            description=f"The admin role is set to {role}",
            color=int(self.primary_color,)
        )

    def error_client_forbidden(self) -> Embed:
        return Embed(
            title="Error: Client Forbidden",
            description="You do not have the required permissions to run this command.",
            color=int(self.error_color,)
        )

    def error_server_forbidden(self) -> Embed:
        return Embed(
            title="Error: Server Forbidden",
            description="I do not have the required permissions set. Missing permission(s): `Manage Messages`",
            color=int(self.error_color)
        )

    def error_guild_only(self) -> Embed:
        return Embed(
            title="Error: Guild Only",
            description="You can only run this command in a guild (server).",
            color=int(self.error_color,)
        )
