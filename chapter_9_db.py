import asyncpg
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg import Record
from asyncpg.pool import Pool
from typing import List, Dict
from db import const

routes = web.RouteTableDef()
DB_KEY = 'database'

# Создать пул подключений к базе данных и сохранить его в экземпляре приложения
async def create_database_pool(app: Application):
    print('Создается пул подключений.')
    pool: Pool = await asyncpg.create_pool(**const.DB)
    app[DB_KEY] = pool


# Уничтожить пул в экземпляре приложения
async def destroy_database_pool(app: Application):
    print('Уничтожается пул подключений.')
    pool: Pool = app[DB_KEY]
    await pool.close()


@routes.get('/brands')
# Запросить все марки и вернуть результаты клиенту
async def brands(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(brand) for brand in results]
    return web.json_response(result_as_dict)

app = web.Application()
# Добавить сопрограммы создания и уничтожения пула в обработчики
# инициализации и очистки
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)
app.add_routes(routes)
web.run_app(app)
