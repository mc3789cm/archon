# Database Schema
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

# Logging
There is plans for integrating all console output with the `logging` module. For now, you can set the following attributes for `logging_manager.LoggingManager`:

| Attribute           | Description                                                                                                         |
|:--------------------|:--------------------------------------------------------------------------------------------------------------------|
| `default_log_level` | Set's the default log level. Used when the user prompted returns nothing.                                           |
| `log_level`         | The log level to use on each runtime. Recommended to leave as `None` if you want to prompt the user for a log level |
| `loggers`           | The loggers to apply logging settings to. Default loggers: `discord.client, discord.gateway, discord.http`          |

### Valid Log Level Entries (Integer):
| Entry |    Level    |
|:-----:|:-----------:|
| `10`  |    Debug    |
| `20`  | Information |
| `30`  |   Warning   |
| `40`  |    Error    |
| `50`  |  Critical   |

### Example:
```python
from ..bot_code.logging_manager import LoggingManager

log_mgr = LoggingManager(default_log_level=20, # Information
               log_level=30, # Warning
               loggers=["discord.client", "discord.gateway", "discord.http"])

log_mgr.initialize()
```