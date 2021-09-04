import socket
import pygame
import sys

HEADER = 64
PORT = 8080
DISCONNECT_MSG = "!!!DISCONNECT!!!"
SERVER = "45.51.92.164"
PLAYERCOUNT = "!!!COUNT!!!"
PLAYAGAIN = "!!!PLAYAGAIN!!!"
NOSPACE = "!!!NOSPACE!!!"

ADDR = (SERVER, PORT)
pygame.init()


class Connect:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(False)
        self.connect()
        self.s.setblocking(True)
        self.player_number = int(self.s.recv(1024).decode('UTF-8')[-1])

    def connect(self):
        """ Attempts to connect to server address (ADDR) with sockets. """
        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                self.s.connect(ADDR)
                break
            except OSError as e:
                # [WinError 10056] A connect request was made on an already connected socket
                if '10056' in str(e):
                    print(e)
                    break

    def send(self, msg):
        """
        :param msg: string to send to server
        :return:
        """
        message = msg.encode('UTF-8')
        msg_len = len(message)
        send_len = str(msg_len).encode('UTF-8')
        send_len += b' ' * (HEADER - len(send_len))
        self.s.send(send_len)
        self.s.send(message)

    def receive(self, again=False):
        """
        Receives message from another client through server.py.
        :param again: boolean
        :return:
        """
        self.s.setblocking(False)
        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.leave()
                        sys.exit()

                instruction = self.s.recv(1024).decode('utf-8')

                if instruction:
                    self.s.setblocking(True)
                    return instruction

            except BlockingIOError:
                if again:
                    return ""
                else:
                    pass

    def playerCount(self):
        """
        :return: 1 or 2 (representing player number)
        """
        self.send(PLAYERCOUNT)
        return self.s.recv(1024).decode('utf-8')

    def leave(self):
        self.send(DISCONNECT_MSG)
