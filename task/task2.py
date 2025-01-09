import asyncio
import time


async def print_with_delay(num):
    await asyncio.sleep(1)
    print(f'Coroutine {num} is done')


async def main():
    start = time.time()

    tasks = [asyncio.create_task(print_with_delay(num)) for num in range(10)]
    _, broken = await asyncio.wait(tasks, timeout=15)
    if broken:
        [task.cancel() for task in broken]
        print(f'Прервано задач - {len(broken)} шт')

            
    print(f'Заняло {time.time() - start:.1f} с')


asyncio.run(main())
