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

import json
import sys
import datetime
from typing import List, Union

import requests

from .exceptions import *
from .prefixes import *

__all__ = (
    'VALUES',
)


def load_json_config(file_path: str = "/opt/archon/etc/discord_bot_config.json"):
    """Loads and parses the values in the configuration file while testing for exceptions along the way.

    :param file_path: The path to the configuration file.

    :return: A dictionary of the parsed configuration values loaded from the given JSON file.

    :raise FileNotFoundError:
    :raise IsADirectoryError:
    :raise PermissionError:
    :raise JSONDecodeError: Raised if there is invalid JSON formatting. Subclass of ``ValueError``.
    """
    try:
        with open(file_path) as config_file:
            return json.load(config_file)

    except (FileNotFoundError, IsADirectoryError):
        raise ConfigError("file_path", message=f"'{file_path}' not found or is a directory")

    except PermissionError:
        raise ConfigError("file_path", message=f"Permission denied for '{file_path}'")

    except json.JSONDecodeError as json_error:
        raise ConfigError("file_path", message=f"Invalid JSON format: {json_error}")


def validate_token(enable_token_validation: bool, token: str):
    """Checks the authenticatable validity of a Discord token by using the Discord API.

    :param enable_token_validation: Skips token authentication if ``False``. This may be desired if you're completely
    affirmative with the validity of your token and would like to reduce API overhead and/or risk of getting rate
    limited by the API.
    :param token: The actual token used  to authenticate with the Discord API.

    :return: ``token``

    :raises ConfigError:
    """
    if not isinstance(enable_token_validation, bool):
        raise ConfigError("enable_token_validation", message=f"Must be a boolean (true/false)")

    if not enable_token_validation:
        print(f"{WARN_LOG} Skipping token authentication validation")
        return token

    if enable_token_validation:
        response = requests.get(url="https://discord.com/api/v10/users/@me", headers={"Authorization": f"Bot {token}"})

        if response.status_code == 200:
            return token

        elif response.status_code == 401:
            raise ConfigError("token", message=f"Token will not connect to the Discord API")

        else:
            raise ConfigError("token", message=f"Unexpected HTTP response during token authentication: {response.status_code} - {response.text}")

    return None


def validate_database_path(database_path: str):
    """Checks the validity of the database path and database file itself.

    The binary header is read and compared to the binary header of what would be a valid SQLite3 file. If the header is
    not equal to that of a valid SQLite3, raise ``ConfigError``.

    :param database_path:

    :return: ``database_path``

    :except FileNotFoundError:
    :except IsADirectoryError:
    :except PermissionError:

    :raises ConfigError:
    """
    try:
        with open(database_path, "rb") as binary_database_file:
            binary_header = binary_database_file.read(16)

            if binary_header != b'SQLite format 3\x00':
                raise ConfigError("database_path", message=f"Not an SQLite3 database ({binary_header})")

    except (FileNotFoundError, IsADirectoryError):
        raise ConfigError("database_path", message=f"'{database_path}' not found or is a directory")

    except PermissionError:
        raise ConfigError("database_path", message=f"Cannot access '{database_path}': Permission denied")

    return database_path


def validate_command_prefix(command_prefix: str):
    """Checks the validity of the command prefix (used in the ``PrefixCommands`` class at ``commands.py``).

    If the length of the prefix is greater than ``1``, has whitespace, or is alphanumeric (composed of a letter or
    number), raise ``ConfigError`` with its respective error message for context.

    :param command_prefix:

    :return: ``command_prefix``

    :raises ConfigError:
    """
    command_prefix_length = len(command_prefix)

    if command_prefix_length > 1:
        raise ConfigError("command_prefix", message=f"Command prefix is longer than one character")

    if not command_prefix.strip():
        raise ConfigError("command_prefix", message=f"Command prefix cannot be empty or just whitespace")

    if command_prefix.isalnum():
        raise ConfigError("command_prefix", message=f"Command prefix should not be a number or letter")

    return command_prefix


def validate_owner_ids(owner_ids: List[Union[int, str, None]]) -> List[int]:
    """Iterates through each owner id in the list of owner ids (``owner_ids``) and running checks for validity.

    The validity is calculated by ensuring the user id is indeed a Discord id and created within a reasonable timespan.

    -----
    Discord uses Snowflake IDs, which are 64-bit unsigned integers containing a timestamp. The timestamp portion is the
    number (milliseconds) since the Discord epoch (2015-01-01).

   1-bit         41-bits              10-bits       12-bits
    ┌┴┐ ┌────────────┴─────────────┐ ┌───┴────┐ ┌──────┴───────┐
     0   Timestamp (ms since epoch)   Worker ID     Sequence

    1-bit: Unused/always 0 (sign bit - ensures it's positive).

    41-bits: Milliseconds since Discord epoch.

    10-bits: Internal Discord unique identifier.

    12-bits: Incremented for every ID generated in the same millisecond.
    -----

    The timestamp is extracted by shifting the snowflake 22 bits to the right. This shifts the top 42 bits into place.
    Add the Discord epoch to get the real time and convert it to datetime for comparison with date creation validity. If
    the creation date was in the future (impossible) or created before the Discord epoch (also impossible),
    ``ConfigError`` will be raised.

    :param owner_ids:

    :return:

    :raises ConfigError:
    """
    DISCORD_EPOCH = 1420070400000

    now = datetime.datetime.now(datetime.timezone.utc)

    CUTOFF_DATE = datetime.datetime(2015, 1, 1, tzinfo=datetime.timezone.utc)

    for owner_id in owner_ids:
        # Allows for only one id to be specified in the list, leaving the second (optional) entry as null.
        if owner_id is None:
            continue

        if not isinstance(owner_id, (str, int)):
            raise ConfigError("owner_id", message=f"User IDs must be numeric values in a string or integer, got: {type(owner_id).__name__}")

        owner_id = int(owner_id)

        owner_id_length = len(str(owner_id))

        if not (17 <= owner_id_length <= 20):
            raise ConfigError("owner_ids", message="User IDs must be between 17 and 20 digits long (inclusive).")

        real_timestamp = (owner_id >> 22) + DISCORD_EPOCH

        creation_date = datetime.datetime.fromtimestamp(real_timestamp / 1000, tz=datetime.UTC)

        if creation_date > now or creation_date < CUTOFF_DATE:
            raise ConfigError("owner_ids", message="Invalid Discord user ID: unreasonable creation timestamp.")

    return owner_ids


def validate_print_intro(print_intro: bool):
    if not isinstance(print_intro, bool):
        raise ConfigError("print_intro", message="Must be a boolean (true/false)")

    else:
        return print_intro


class Values:
    def __init__(self):
        try:
            json_config = load_json_config()

            self.TOKEN: str = validate_token(json_config["enable_token_validation"], json_config["token"])
            self.DATABASE_PATH: str = validate_database_path(json_config["database_path"])
            self.COMMAND_PREFIX: str = validate_command_prefix(json_config["command_prefix"])
            self.OWNER_IDS: list = validate_owner_ids(json_config["owner_ids"])
            self.PRINT_INTRO: bool = validate_print_intro(json_config["print_intro"])

        except ConfigError as error:
            print(f"{EROR_LOG} Invalid configuration: {error.faulty_key}: {error.message}")

            # For POSIX-compliance.
            sys.exit(78)


VALUES = Values()
