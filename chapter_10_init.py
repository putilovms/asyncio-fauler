import asyncio
import asyncpg
from db import const


async def main():
    # chart
    connection = await asyncpg.connect(**const.DB_CART)
    statements = [
        const.DROP_CART,
        const.USER_CART_CREATE,
        const.USER_CART_INSERT,
    ]
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('Таблица user_cart наполнена')
    await connection.close()

    # favorites
    connection = await asyncpg.connect(**const.DB_FAVORITES)
    statements = [
        const.DROP_FAVORITE,
        const.USER_FAVORITE_CREATE,
        const.USER_FAVORITE_INSERT,
    ]
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('Таблица user_favorite наполнена')
    await connection.close()


asyncio.run(main())
