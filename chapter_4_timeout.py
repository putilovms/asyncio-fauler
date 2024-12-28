import asyncio
from aiohttp import ClientSession
from util import async_timed, fetch_status


@async_timed()
async def main():
    async with ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        # Сгенерировать список сопрограмм для каждого запроса, который мы
        # хотим отправить
        requests = [fetch_status(session, url) for url in urls]
        # Ждать завершения всех запросов
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

asyncio.run(main())
