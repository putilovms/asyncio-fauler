import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()
server_socket.setblocking(False)

selector.register(server_socket, selectors.EVENT_READ)

while True:
    # Создать селектор с тайм-аутом 1 с
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
    print(events)
    # Если ничего не произошло, сообщить об
    # этом. Такое возможно в случае тайм-аута
    if len(events) == 0:
        print('Событий нет, подожду еще!')
    for event, _ in events:
        # Получить сокет, для которого
        # произошло событие, он хранится в поле
        # fileobj
        event_socket = event.fileobj
        # Если событие произошло с серверным сокетом, значит,
        # была попытка подключения
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"Получен запрос на подключение от {address}")
            # Зарегистрировать клиент, подключившийся к сокету
            selector.register(connection, selectors.EVENT_READ)
        # Если событие произошло не с серверным сокетом,
        # получить данные от клиента и отправить их обратно
        else:
            data = event_socket.recv(1024)
            print(f"Получены данные: {data}")
            event_socket.send(data)
