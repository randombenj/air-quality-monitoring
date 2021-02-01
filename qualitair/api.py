import asyncio
from pathlib import Path

from aiohttp import web
from tortoise.functions import Avg

from qualitair.db import Measurement, Interval


routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    content = await asyncio.get_event_loop().run_in_executor(
        None,
        (Path(__file__).parent / "static" / "index.html").read_text
    )
    return web.Response(
        text=content,
        content_type='text/html'
    )


@routes.get('/api/measurement')
async def hello(request):
    limit = int(request.rel_url.query.get("limit", 3600))  # ~ last hour
    offset = int(request.rel_url.query.get("offset", 0))

    return web.json_response({
        "measurements": [
            m.to_json()
            for m in (await Measurement
                .all()
                .offset(offset)
                .limit(limit)
                .order_by("-timestamp")
        )]
    })


@routes.get('/api/heatmap')
async def heatmap_data(request):
    return web.json_response({
        "data": [
            {
                "timestamp": m["interval"],
                "value": {
                    "voc": m["voc_avg"]
                }
            }
            for m in (await Measurement
                # Take the average of dat in a 15 min interval
                .annotate(
                    voc_avg=Avg("voc"),
                    interval=Interval("timestamp", 60 * 60)
                )
                .group_by("interval")
                .order_by("interval")
                .values(
                    "interval",
                    "voc_avg"
                )
            )]
    })


async def start():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()
    return runner
