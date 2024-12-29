import asyncio
import asyncpg
import logging
from db import const


async def main():
    connection = await asyncpg.connect(**const.DB)
    # Начать транзакцию базы данных
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            # Команда insert завершится неудачно из-за дубликата
            # первичного ключа
            await connection.execute(insert_brand)
    except Exception:
        # Если было исключение, протоколировать ошибку
        logging.exception('Ошибка при выполнении транзакции')
    finally:
        query = """SELECT brand_name FROM brand
                   WHERE brand_name LIKE 'big_%'"""
        # Выбрать марки и убедиться, что ничего не вставлено
        brands = await connection.fetch(query)
        print(f'Результат запроса: {brands}')
        await connection.close()

asyncio.run(main())
