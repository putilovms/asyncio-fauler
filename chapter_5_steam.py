import asyncpg
import asyncio
import asyncpg
from db import const


async def async_for():
    connection = await asyncpg.connect(**const.DB)
    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)
    await connection.close()

# asyncio.run(async_for())


async def fetch():
    connection = await asyncpg.connect(**const.DB)
    async with connection.transaction():
        query = 'SELECT product_id, product_name FROM product'
        # Создать курсор для запроса
        cursor = await connection.cursor(query)
        # Сдвинуть курсор вперед на 500 записей
        await cursor.forward(500)
        # Получить следующие 100 записей
        products = await cursor.fetch(100)
        for product in products:
            print(product)
    await connection.close()

asyncio.run(fetch())
