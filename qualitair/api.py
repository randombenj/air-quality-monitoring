from aiohttp import web

from qualitair.db import Measurement


routes = web.RouteTableDef()


@routes.get('/')
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


async def start():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()
    return runner
