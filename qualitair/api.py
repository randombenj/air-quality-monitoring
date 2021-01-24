from aiohttp import web

from qualitair.db import Measurement


routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.json_response({
        "measurements": [m.value for m in await Measurement.all()]
    })


def get_app():
    app = web.Application()
    app.add_routes(routes)
    return app
