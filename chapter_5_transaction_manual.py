import asyncio
import asyncpg
from asyncpg.transaction import Transaction
from db import const


async def main():
    connection = await asyncpg.connect(**const.DB)
    # Создать экземпляр транзакции
    transaction: Transaction = connection.transaction()
    # Начать транзакцию
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Ошибка, транзакция откатывается!')
        # Если было исключение, откатить
        await transaction.rollback()
    else:
        print('Ошибки нет, транзакция фиксируется!')
        # Если исключения не было, зафиксировать
        await transaction.commit()
    query = """SELECT brand_name FROM brand
               WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)
    await connection.close()
asyncio.run(main())
