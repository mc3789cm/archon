<!---
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
--->
# DatabaseManager
## Attributes
| Attribute | Description                                                      |                 Default                 |
|:---------:|:-----------------------------------------------------------------|:---------------------------------------:|
| `db_path` | Path to the database file used by [SQLite](https://sqlite.org/). | `db_path="../storage/database.sqlite3"` |

## Tables
### Statistics:
|       Server Name        |      Server ID      | Join Date  |
|:------------------------:|:-------------------:|:----------:|
| Archon Community/Support | 1409173153250545725 | 2025-08-24 |

```sql
CREATE TABLE IF NOT EXISTS "Statistics" (
    "Server Name" TEXT,
    "Server ID" INTEGER NOT NULL UNIQUE,
    "Join Date" TEXT,
    PRIMARY KEY("Server ID")
);
```

### General Configuration:
|      Server ID      |     Admin Role      |
|:-------------------:|:-------------------:|
| 1409173153250545725 | 1409174702668120105 |

``` sql
CREATE TABLE IF NOT EXISTS "General Configuration" (
    "Server ID" INTEGER NOT NULL UNIQUE,
    "Admin Role ID" INTEGER,
    PRIMARY KEY("Server ID")
);
```

# EmbedManager
## Attributes
|    Attribute    |   Default   |
|:---------------:|:-----------:|
| `primary_color` | `"#1793d1"` |
|  `error_color`  | `"#dc143c"` |
|   `bot_name`    |   `"Bot"`   |

# EventManager
## Attributes
|      Attribute      |   Required Type   |
|:-------------------:|:-----------------:|
|   `bot_instance`    | `AutoShardedBot`  |
| `database_instance` | `DatabaseManager` |
|  `embed_instance`   |  `EmbedManager`   |

# LoggingManager
## Attributes
|      Attribute      |                                                     Description                                                     |
|:-------------------:|:-------------------------------------------------------------------------------------------------------------------:|
| `default_log_level` |                      Set's the default log level. Used when the user prompted returns nothing.                      |
|     `log_level`     | The log level to use on each runtime. Recommended to leave as `None` if you want to prompt the user for a log level |
|      `loggers`      |         The list of loggers to configure. Default loggers: `discord.client, discord.gateway, discord.http`          |

## Valid Log Level Entries (Integer):
| Entry |    Level    |
|:-----:|:-----------:|
| `10`  |    Debug    |
| `20`  | Information |
| `30`  |   Warning   |
| `40`  |    Error    |
| `50`  |  Critical   |

### Example:

```python
from bot_code.set_logging import LoggingManager

log_mgr = LoggingManager(default_log_level=20,  # Information
                         log_level=30,  # Warning
                         loggers=["discord.client", "discord.gateway",
                                  "discord.http"])  # These are already the default.

log_mgr.initialize()
```