import logging
import asyncio
from aiohttp import web

from qualitair.db import init
from qualitair.api import get_app
from qualitair.data_daemon import DataDaemon


async def main():
    logging.info("initializing database")
    await init()

    logging.info("starting data gathering daemon")
    daemon = DataDaemon()
    asyncio.create_task(daemon.run())

    logging.info("starting api")
    app = get_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()

    # wait forever
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
