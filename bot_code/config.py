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

import os
import sys
import json
import dataclasses

import requests

from .prefixes import *

__all__ = (
    'config',
)


class ConfigError(Exception):
    def __init__(self, faulty_key: str, message: str | None):
        self.faulty_key = faulty_key
        self.message = message


def load_json_config(file_path: str = "/etc/bot_config.json"):
    try:
        with open(file_path) as config_file:
            return json.load(config_file)

    except (FileNotFoundError, IsADirectoryError):
        raise ConfigError("file_path", message=f"'{file_path}' not found or is a directory")

    except PermissionError:
        raise ConfigError("file_path", message=f"Permission denied for '{file_path}'")

    except json.JSONDecodeError as json_error:
        raise ConfigError("file_path", message=f"Invalid JSON format: {json_error}")


json_config = load_json_config()


def is_token_valid(token: str) -> str:
    headers = {
        "Authorization": f"Bot {token}"
    }

    response = requests.get(url="https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        return token

    elif response.status_code == 401:
        raise ConfigError("token", message=f"Token will not connect to Discord API")

    else:
        print(f"{WARN_LOG} Unexpected response during token authentication: {response.status_code} - {response.text}")
        raise ConfigError("token", message=None)


def is_database_path_valid(db_path: str) -> str:
    if os.path.isdir(db_path):
        raise ConfigError("database_path", message=f"Cannot access '{db_path}': Is a directory")

    if not os.path.exists(db_path):
        raise ConfigError("database_path", message=f"Cannot access '{db_path}': No such path")

    try:
        with open(db_path):
            pass
    except PermissionError:
        raise ConfigError("database_path", message=f"Cannot access '{db_path}': Permission denied")

    return db_path


def is_command_prefix_valid(cmd_prefix: str) -> str:
    command_prefix_length = len(cmd_prefix)

    if command_prefix_length >= 3:
        raise ConfigError("command_prefix", message=f"Command prefix is longer than three characters")

    if not cmd_prefix.strip():
        raise ConfigError("command_prefix", message=f"Command prefix cannot be empty or just whitespace")

    if cmd_prefix.isalnum():
        raise ConfigError("command_prefix", message=f"Command prefix should not be a number or letter")

    return cmd_prefix


def is_owner_ids_valid(owner_ids: list) -> list:
    for owner_id in owner_ids:

        owner_id_length = len(str(owner_id))

        if owner_id_length <= 15 or owner_id_length >= 20:
            raise ConfigError("owner_ids", message="Owner ID's cannot be shorter than 15 or greater than 20")

    return owner_ids


def is_print_intro_valid(print_intro: bool) -> bool:
    if not isinstance(print_intro, bool):
        raise ConfigError("print_intro", message="Print intro must be a boolean")

    return print_intro


class RawConfigValues:
    def __init__(self):
        self.TOKEN: str = json_config["token"]
        self.DB_PATH: str = json_config["database_path"]
        self.CMD_PREFIX: str = json_config["command_prefix"]
        self.OWNER_IDS: list = json_config["owner_ids"]
        self.PRINT_INTRO: bool = json_config["print_intro"]


raw_values = RawConfigValues()

validators = {
    "token": is_token_valid,
    "database_path": is_database_path_valid,
    "command_prefix": is_command_prefix_valid,
    "owner_ids": is_owner_ids_valid,
    "print_intro": is_print_intro_valid,
}

attr_map = {
    "token": "TOKEN",
    "database_path": "DB_PATH",
    "command_prefix": "CMD_PREFIX",
    "owner_ids": "OWNER_IDS",
    "print_intro": "PRINT_INTRO",
}

for key, validator in validators.items():
    value = getattr(raw_values, attr_map[key])
    try:
        validated = validator(value)
        globals()[attr_map[key]] = validated

    except ConfigError as error:
        print(f"{EROR_LOG} Invalid configuration: {error.faulty_key}: {error.message}")
        sys.exit(78)


@dataclasses.dataclass
class Config:
    TOKEN: str
    DB_PATH: str
    CMD_PREFIX: str
    OWNER_IDS: list
    PRINT_INTRO: bool


config = Config(
    TOKEN=is_token_valid(raw_values.TOKEN),
    DB_PATH=is_database_path_valid(raw_values.DB_PATH),
    CMD_PREFIX=is_command_prefix_valid(raw_values.CMD_PREFIX),
    OWNER_IDS=is_owner_ids_valid(raw_values.OWNER_IDS),
    PRINT_INTRO=is_print_intro_valid(raw_values.PRINT_INTRO)
)