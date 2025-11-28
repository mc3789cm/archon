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
# Archon
<sup>/ˈɑːr.kɒn/ -> “AR-kon”, "Ark-on", "Ar-chon"</sup>

![Python Version](https://img.shields.io/badge/Python-3.13.7-blue)
![License](https://img.shields.io/badge/License-MIT-purple)
![Library](https://img.shields.io/badge/Uses-Discord.py-red)

A modular, utility-focused Discord bot designed for control, customization, and
performance - inspired by the philosophy of Arch Linux.

> [!WARNING]
> Although I try my best to push production quality and battle tested code, 
> I'm still just learning Python and this project is still under development,
> so use any and all code at your own risk.

During my time as an admin for a few Discord servers, and as a perfectionist,
I always had the problem of not having enough customization, control, and/or
configuration when trying to use a bot for the server's needs. And, even if it
did, it would usually be behind a pay wall or the feature was limited to 
only a few uses/implementations.

I plan to make Archon a kind of *"power-tool"* with multitudes of 
configuration for all modules, no limits.

It's up to the user to configure and maintain it. Each module will be 
disabled by default, no bloat, no unnecessary defaults. Just a blank slate,
everything greyed out for the task of whatever configuration you have desired.

## Installation
> [!NOTE]
> I will not be supporting Windows or MacOS. WSL might work.

I do plan on making packages for a few major Linux distros in the near 
future. These packages are:
- `.pkg.tar.zst`
- `.deb`
- `.rpm`
- `.flatpakref`

But, for now, we'll just have to install manually.

### Prerequisites:
*Make* sure you have:
- `sqlite3`
- `make`
- `Python`
    Might work with older versions, but try to use version 3.13.7 or newer.

### Clone the Repository:
```bash
git clone https://github.com/mc3789cm/archon

cd ./archon
```

### Configure:
Open the `example.discord_bot_config.json` in your text editor and configure 
the following values:

#### token
This is your bot's secret **Discord bot token.** Obtain this token at the 
[Discord Developer Portal](https://discord.com/developers/applications). Do 
not share this token as anyone with access to it will be able to control 
your bot (including any servers it's in).

Must be a valid string provided by Discord.

#### enable_token_validation
This value determines if the given token should be validated before runtime. 
You may set this to `false` if you wish to reduce API calls to the Discord API.

Must be a boolean.

#### database_path
This value is the **absolute** path to the SQLite3 database file. You should 
leave this as the default, but you may set it to another location, like 
`/var/db/database.sqlite3`.

Must be a string to a real SQLite3 database file.

#### owner_ids
If you do not wish to specify multiple user ID's, and only want to use yours,
set the second value after your user ID to `null`. Only enter one `null` 
value after your user ID.

Must be a valid **Discord Snowflake ID** (17-20 digit integer).

#### command_prefix
This value is used to recognize commands (e.g., `?help`, `!ping`, `$shutdown`).

Must be a single, non-alphanumeric, non-whitespace character.

#### print_intro
This value is used to determine if the program should print the title, ASCII 
art, and copyright on startup.

Set to `false` to skip this output for a faster startup.

Must be a boolean.

### Rename the Configuration File
Rename the JSON configuration file to `discord_bot_config.json`

```bash
mv ./example.discord_bot_config.json discord_bot_config.json
```

### Compile into an Executable:
The source code is packaged along with its dependencies and Python interpreter
into a standalone executable.

This means you don't need to keep Python (or make) installed in your system 
after installation (make is still required for uninstallation).
```bash
make build
```

### Install to `/opt`:
```bash
sudo make install
```

### Uninstall:
```bash
sudo make uninstall
```

### Execution:
A symlink to the executable in `/opt` should be present in PATH, but you need to add yourself to the `archon` group, or execute Archon with sudo.

Use the `archon` group (recommended):
```bash
sudo usermod -aG archon your-username

archon
```

Or just use sudo:
```bash
sudo archon
```

## Planned Features
- [ ] Website
  - [ ] Domain name
  - [ ] Dashboard
  - [ ] Visual customization/themes
- [ ] Advanced, user-friendly, and intuitive custom reaction roles</br>
  *Inspiration from Tech's [Reaction Roles](https://reactionroles.mtdv.me/) 
  bot.*
- [ ] Leveling
- [ ] Starboard
- [ ] Custom embed builder</br>
  *Inspiration from the Discohook Team's
  [Discohook Utils](https://discohook.app).*
- [ ] Permissions and role-based command management
- [ ] Custom logging modules

Much, much more...

## Philosophy
Archon's philosophy gravitates alongside that of what the name is relative 
to - Arch Linux, not just the literal meaning of the word.

Much like Arch, Archon empowers users through responsibility, offers flexibility
with its modular design, as configurable as Arch, and independently
maintainable. At the same time, handing out transparency and user control with
this GitHub repository, clear documentation (yet to be written), and encouraged
manual configuration.

Anyway, about the literal meaning of the word. The word *Archon* comes from 
ancient Greek (ἄρχων), meaning “ruler” or “magistrate”. In Classical Athens, an
archon was a high-ranking official who had administrative, judicial, and
sometimes military authority. The term literally conveys leadership, control,
and authority.

### Colors
| Role           |     Hex      |          RGB          |
|:---------------|:------------:|:---------------------:|
| Primary        |  `#1793D1`   |  `rgb(23, 147, 209)`  |
| Secondary      |  `#1ABC9C`   |  `rgb(26, 188, 156)`  |
| Background     |  `#1E1E1E`   |   `rgb(30, 30, 30)`   |
| Primary Text   |  `#ECECEC`   | `rgb(236, 236, 236)`  |
| Secondary Text |  `#A0A0A0`   | `rgb(160, 160, 160)`  |

## See Also
- [Archon - Wikipedia](https://en.wikipedia.org/wiki/Archon)
- [Discord.py - Rapptz](https://github.com/Rapptz/discord.py)
- Discord user: `vykefanatic`

Add me on Discord if you are interested in contributing, translating, or 
even just have some suggestions/ideas. I'm open to any and all
feedback/criticisms.

Malloc. Malice. Malaise. Malign. Malinger. Malaria. Malkin. Malcontent. Malevolent. Malloc.

## License

MIT License. See [`LICENSE`](./LICENSE).
