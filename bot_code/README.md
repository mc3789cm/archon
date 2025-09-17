<!---
MIT License

Copyright (c) Ethan Kenneth Davies
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
from bot_code.logging_manager import LoggingManager

log_mgr = LoggingManager(default_log_level=20, # Information
               log_level=30, # Warning
               loggers=["discord.client", "discord.gateway", "discord.http"]) # These are already the default.

log_mgr.initialize()
```