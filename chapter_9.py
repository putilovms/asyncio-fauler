from aiohttp import web
from datetime import datetime
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()


@routes.get('/time')
# Создать оконечную GET-точку time; когда клиент обратится к ней, будет
# вызвана сопрограмма time
async def time(request: Request) -> Response:
    today = datetime.today()
    result = {
        'month': today.month,
        'day': today.day,
        'time': str(today.time())
    }
    # Взять словарь result и преобразовать его в формат JSON
    return web.json_response(result)

# Создать веб-приложение, зарегистрировать маршруты и запустить его
app = web.Application()
app.add_routes(routes)
web.run_app(app)
