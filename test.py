import pygame
import sys
from client import Connect
from initialize import ConnectFour
import time

pygame.init()
pygame.font.init()

size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))

highlightColor = pygame.Color(115, 115, 115, a=50)


# 6x7 grid
def drawGrid():

    def createSquare(x, y, width):
        return pygame.Rect(x, y, width, width)

    width = 100
    offset = -50
    y = 0
    for ind1, row in enumerate(c4.gameBoard):
        x = 0
        for ind2, item in enumerate(row):
            rect = createSquare(x,y,width)
            pygame.draw.rect(screen, (0, 0, 0), rect, width=1)
            if item == 1:
                screen.blit(blackCircle, (rect.center[0]-50, rect.center[1]-50))
            elif item == 2:
                screen.blit(redCircle, (rect.center[0]+offset, rect.center[1]+offset))
            x += width
        y += width


def contain(mode=None):
    for count, i in enumerate(range(0, 700, 100),1):
        pos = pygame.mouse.get_pos()
        if i < pos[0] < i+100 and 0 < pos[1] < 600:
            if mode is None:
                r = pygame.Rect((i, 0, 100, 600))
                pygame.draw.rect(screen, 'white', pygame.Rect((0,0,width,height)))
                pygame.draw.rect(screen, highlightColor, r)
            elif mode == 'box':
                print("Column:", count)
                return count


def login():
    try:
        log = Connect()
    except Exception:
        user = input('An error has occurred. Type any key to retry or EXIT: ')
        if user.lower() == "exit":
            exit()
        log = login()
    return log


def waitKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                result = contain('box')
                if result:
                    return result

        contain()
        drawGrid()

        pygame.display.update()


def updateScreen():
    pygame.draw.rect(screen, 'white', pygame.Rect((0, 0, width, height)))
    drawGrid()
    pygame.display.update()


def checkWin(player_number):
    if c4.check(player_number):
        print(f'Player {player_number} wins!')
        # TODO: V V V Fix play again option V V V
        input('Press enter to leave the game. . . ')
        client.leave()
        exit()


if __name__ == '__main__':
    c4 = ConnectFour()
    client = login()

    blackCircle = pygame.image.load('assets/blackCircle.png').convert_alpha()
    blackCircle = pygame.transform.scale(blackCircle, (100, 100))

    redCircle = pygame.image.load('assets/redCircle.png').convert_alpha()
    redCircle = pygame.transform.scale(redCircle, (100, 100))

    player_number = client.player_number
    print("You are player number", player_number)

    if int(client.playerCount()) != 2:
        print("Please wait for other player to join. . .")

    updateScreen()
    flag = True

    while flag:
        while int(client.playerCount()) == 2:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    sys.exit()

            updateScreen()

            if player_number == 1:
                print('\nPlayer One\'s Turn')
                userPlace = waitKey()
                c4.place(userPlace, 1)
                client.send(str(userPlace))
                updateScreen()
                checkWin(player_number)

                print(f"\nWaiting for player 2's move . . .\n")
                opponent_move = client.receive()
                c4.place(opponent_move, 2)
                checkWin(2)

            elif player_number == 2:
                print('Waiting for player 1\'s move')
                opponent_move = client.receive()
                c4.place(int(opponent_move), 1)

                updateScreen()

                checkWin(1)

                print('\nPlayer Two\'s Turn')
                userPlace = waitKey()
                c4.place(userPlace, player_number)
                client.send(str(userPlace))
                updateScreen()
                checkWin(player_number)

            pygame.draw.rect(screen, 'white', pygame.Rect((0, 0, width, height)))
            drawGrid()
            updateScreen()
            pygame.display.update()

        # Time buffer to avoid spam on server
        time.sleep(5)