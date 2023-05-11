import socket
import time
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
main_socket.bind(("192.168.31.29", 10000))  # IP и порт привязываем к порту
main_socket.setblocking(False)  # Непрерывность, не ждём ответа
main_socket.listen(5)  # Прослушка входящих соединений, 5 одновременных подключений
print("Сокет создался")

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()


def find(raw: str):
    first = None
    for num, sign in enumerate(raw):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = list(raw[first + 1:second].split(","))
            return result
    return ""


# Декларативный класс таблицы игроков
class Player(Base):
    __tablename__ = "gamers"
    name = Column(String, primary_key=True)
    password = Column(String(250))
    score = Column(Integer, default=0)

    def __init__(self, name, passw):
        self.name = name
        self.password = passw


Base.metadata.create_all(engine)

players = []
run = True
while run:
    try:
        new_socket, addr = main_socket.accept()  # принимаем входящие
        print('Подключился', addr)
        new_socket.setblocking(False)
        players.append(new_socket)

    except BlockingIOError:
        pass

    for sock in players:
        try:
            data = sock.recv(1024).decode()
            data = find(data)
            if data:
                player = Player(data[0], data[1])
                s.add(player)
                s.commit()
                sock.send("<0>".encode())
            print("Получил", data)
            run = False
            break
        except sqlalchemy.exc.IntegrityError:
            s.rollback()
            player = s.get(Player, data[0])
            if data[1] == player.password:
                sock.send(f"<{player.score}>".encode())
            else:
                sock.send("<-1>".encode())
            break
        except BlockingIOError:
            pass


    time.sleep(1)
