import asyncio
import logging
from asyncio import StreamReader, StreamWriter


class ServerState:
    def __init__(self):
        self._writers = []

    # Добавить клиента в состояние сервера и создать задачу эхо-копирования
    async def add_client(self, reader: StreamReader, writer: StreamWriter):
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    # После подключения нового клиента сообщить ему, сколько клиентов
    # подключено, и уведомить остальных о новом пользователе
    async def _on_connect(self, writer: StreamWriter):
        writer.write(
            f'Добро пожаловать! Число подключенных пользователей: {len(self._writers)}!\n'.encode())
        await writer.drain()
        await self._notify_all('Подключился новый пользователь!\n')

    # Обработать эхо-копирование ввода при отключении клиента
    # и уведомить остальных пользователей об отключении
    async def _echo(self, reader: StreamReader, writer: StreamWriter):
        try:
            while (data := await reader.readline()) != b'':
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(f'Клиент отключился. Осталось пользователей: {len(self._writers)}!\n')
        except Exception as e:
            logging.exception('Ошибка чтения данных от клиента.', exc_info=e)
            self._writers.remove(writer)

    # Вспомогательный метод для отправки сообщения всем остальным пользователям. Если
    # отправить сообщение не удалось, удалить данного пользователя
    async def _notify_all(self, message: str):
        for writer in self._writers:
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionError as e:
                logging.exception('Ошибка записи данных клиенту.', exc_info=e)
                self._writers.remove(writer)


async def main():

    # При подключении нового клиента добавить его в состояние сервера
    async def client_connected(reader: StreamReader, writer:
                               StreamWriter) -> None:
        await server_state.add_client(reader, writer)

    server_state = ServerState()
    # Запустить сервер и обслуживать запросы бесконечно
    server = await asyncio.start_server(client_connected, '127.0.0.1', 8000)
    async with server:
        await server.serve_forever()

asyncio.run(main())
