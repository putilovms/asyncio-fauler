import asyncio
import logging
from typing import Callable, Awaitable


class TooManyRetries(Exception):
    pass


async def retry(coro: Callable[[], Awaitable],
                max_retries: int,
                timeout: float,
                retry_interval: float):
    for retry_num in range(0, max_retries):
        try:
            # Ждать ответа, пока не истечет заданный таймаут
            return await asyncio.wait_for(coro(), timeout=timeout)
        except Exception as e:
            # Если получено исключение, протоколировать его и ждать
            # в течение заданного интервала перед повторной попыткой
            logging.exception(
                f'Во время ожидания произошло исключение(попытка {retry_num})), пробую еще раз.',
                exc_info=e)
            await asyncio.sleep(retry_interval)
    # Если было слишком много неудачных попыток, возбудить исключение, уведомляющее об этом
    raise TooManyRetries()
