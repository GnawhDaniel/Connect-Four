import socket
import threading
import time


class Server:
    def __init__(self):
        self.client_list = []
        self.messages = []
        self.start()

    def handle_client(self, conn, addr):
        """
        Handles individual connections.
        :param conn:
        :param addr:
        :return:
        """

        print(f"[NEW CONNECTION] {addr} connected.")
        conn.send(f'[Connection] Connected. Player {len(self.client_list)}'.encode('utf-8'))
        connected = True

        while connected:

            msg_len = conn.recv(HEADER).decode('UTF-8')

            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode('UTF-8')

                if msg == DISCONNECT_MSG:
                    connected = False
                    self.client_list.remove(conn)

                elif msg == PLAYERCOUNT:
                    conn.send(str(threading.activeCount() - 1).encode('utf-8'))

                elif msg == PLAYAGAIN:
                    for c in self.client_list:
                        if c != conn:
                            c.send(PLAYAGAIN.encode('utf-8'))

                elif threading.activeCount() - 1 == 2:
                    for c in self.client_list:
                        if c != conn:
                            c.send(msg.encode('utf-8'))

                print(f"[{addr}] {msg}")

        conn.close()

    def start(self):
        """
        Initializes server and accepts new connections.
        """
        print("[STARTING] Server is starting.")
        s.listen(2)
        print(f"[LISTENING] Listening on {SERVER}")
        while True:
            if threading.activeCount() - 1 < 2:
                conn, addr = s.accept()
                self.client_list.append(conn)
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == '__main__':
    HEADER = 64
    PORT = 8080
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)

    DISCONNECT_MSG = "!!!DISCONNECT!!!"
    PLAYERCOUNT = "!!!COUNT!!!"
    PLAYAGAIN = "!!!PLAYAGAIN!!!"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)

    try:
        serv = Server()
    except Exception:
        s.close()

    s.close()
