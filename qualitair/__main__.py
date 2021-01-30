import sys
import logging
import asyncio
import signal

import qualitair.db as db
import qualitair.api as api
from qualitair.data_daemon import DataDaemon


async def main():
    logging.info("initializing database")
    await db.init()

    logging.info("starting api")
    runner = await api.start()

    logging.info("starting data gathering daemon")
    daemon = DataDaemon()
    asyncio.create_task(daemon.run())

    #  handle app shutdown
    event = asyncio.Event()  # the termination event
    asyncio.get_event_loop().add_signal_handler(
        signal.SIGINT,
        lambda: [
            daemon.quit(),
            asyncio.ensure_future(runner.cleanup()),
            event.set()
        ]
    )

    # wait until application shutdown
    await event.wait()
    await db.quit()

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    asyncio.run(main())
