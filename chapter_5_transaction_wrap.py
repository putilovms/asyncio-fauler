import asyncio
import asyncpg
import logging
from db import const

async def main():
    connection = await asyncpg.connect(**const.DB)
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")
        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as ex:
            logging.warning('Ошибка при вставке цвета товара игнорируется', exc_info=ex)
    await connection.close()
asyncio.run(main())