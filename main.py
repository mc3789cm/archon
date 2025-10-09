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

import asyncio
import signal

import bot_code as bc


async def print_intro(run_print_intro: bool = bc.VALUES.PRINT_INTRO):
    """Prints the program intro ASCII and metadata if enabled in config."""
    if not run_print_intro:
        return

    print(bc.__title__, bc.__version__)

    await asyncio.sleep(0.25)

    for line in bc.__ARCHON_ASCII__:
        print(line)
        await asyncio.sleep(0.25)

    print(bc.__copyright__)


async def main():
    await print_intro()

    loop = asyncio.get_running_loop()

    stop_event = asyncio.Event()

    def shutdown():
        print(f"{bc.WARN_LOG} Received shutdown signal...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    try:
        await bc.start_bot()
        await stop_event.wait()
    except KeyboardInterrupt:
        print(f"{bc.WARN_LOG} Received KeyboardInterrupt")
    finally:
        await bc.stop_bot(bot_instance=bc.default_bot, database_instance=bc.default_database)
        print(f"{bc.INFO_LOG} Shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
