import socket
import pygame
import sys

HEADER = 64
PORT = 8080
DISCONNECT_MSG = "!!!DISCONNECT!!!"
SERVER = "192.168.0.3"
PLAYERCOUNT = "!!!COUNT!!!"
ADDR = (SERVER, PORT)
pygame.init()


class Connect:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDR)
        self.player_number = int(self.s.recv(1024).decode('UTF-8')[-1])

    def send(self, msg):
        message = msg.encode('UTF-8')
        msg_len = len(message)
        send_len = str(msg_len).encode('UTF-8')
        send_len += b' ' * (HEADER - len(send_len))
        self.s.send(send_len)
        self.s.send(message)

    def receive(self):
        self.s.setblocking(False)
        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.leave()
                        sys.exit()
                player_move = self.s.recv(1024).decode('utf-8')
                if player_move:
                    self.s.setblocking(True)
                    return player_move
            except BlockingIOError:
                pass

    def playerCount(self):
        self.send(PLAYERCOUNT)
        return self.s.recv(1024).decode('utf-8')

    def leave(self):
        self.send(DISCONNECT_MSG)


