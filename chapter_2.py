import asyncio
import time
from asyncio import CancelledError, Future
import requests
from util import async_timed, delay

# пример демонстрирующий блокировку
# при исползовании async и await


async def add_one(number: int) -> int:
    return number + 1


async def hello_world_message() -> str:
    await delay(1)
    return 'Hello World!'


async def main() -> None:
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    print(one_plus_one)
    print(message)

# asyncio.run(main())


# пример работы с задачами


async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)

# asyncio.run(main())


# Пример рабоыт несколькоих задач

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))
    await sleep_for_three
    await sleep_again
    await sleep_once_more

# asyncio.run(main())


# пример выполнения кода пока другие операции работают


async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print("пока я жду, исполняется другой код!")


async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay

# asyncio.run(main())

# снятие задач


async def main():
    long_task = asyncio.create_task(delay(10))
    seconds_elapsed = 0
    while not long_task.done():
        print('Задача не закончилась, следующая проверка через секунду.')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()
    try:
        await long_task
    except CancelledError:
        print('Наша задача была снята')

# asyncio.run(main())

# снятие задач при помощи wait_for()


async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Тайм-аут!')
    print(f'Задача была снята? {delay_task.cancelled()}')

# asyncio.run(main())

# Защита задачи от снятия


async def main():
    task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Задача заняла более 5 с, скоро она закончится!")
        result = await task
        print(result)

# asyncio.run(main())

# объекты будущего


def future_func():
    my_future = Future()
    print(f'my_future готов? {my_future.done()}')
    my_future.set_result(42)
    print(f'my_future готов? {my_future.done()}')
    print(f'Какой результат хранится в my_future? {my_future.result()}')


# future_func()

# измерение времени выполнения сопрограммы


async def main():
    start = time.time()
    await asyncio.sleep(1)
    end = time.time()
    print(f'Сон занял {end - start} с')

# asyncio.run(main())

# Пример блокировки цикла событий счётной операцией


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter


@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))
    await task_one
    await task_two
    await delay_task

# asyncio.run(main())

# Пример блокирующего вызова API


@async_timed()
async def get_example_status() -> int:
    return requests.get('http://www.example.com').status_code


@async_timed()
async def main():
    task_1 = asyncio.create_task(get_example_status())
    task_2 = asyncio.create_task(get_example_status())
    task_3 = asyncio.create_task(get_example_status())
    await task_1
    await task_2
    await task_3

# asyncio.run(main())

# Создание цикла событий вручную


async def main():
    await asyncio.sleep(1)

loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

# Получение доступа к циклу событий


def call_later():
    print("Меня вызовут в ближайшем будущем!")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)

asyncio.run(main())
