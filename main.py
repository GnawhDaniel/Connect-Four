import pygame
import sys
from client import Connect
from gameboard import ConnectFour
import time

pygame.init()
pygame.font.init()

size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")
screen.fill((255, 255, 255))

transparentScreen = pygame.Surface(size)
transparentScreen.set_alpha(225)
transparentScreen.fill((200, 200, 200))

highlightColor = pygame.Color(115, 115, 115, a=50)

FONT = pygame.font.SysFont(None, 48)

blackCircle = pygame.image.load('assets/blackCircle.png').convert_alpha()
blackCircle = pygame.transform.scale(blackCircle, (100, 100))

redCircle = pygame.image.load('assets/redCircle.png').convert_alpha()
redCircle = pygame.transform.scale(redCircle, (100, 100))

PLAYAGAIN = "!!!PLAYAGAIN!!!!"


class Game:
    def __init__(self):
        self.c4 = ConnectFour()
        self.client = Game.login()

        self.player_number = self.client.player_number
        self.playerCount = int(self.client.playerCount())

        self.waiting = False

        self.updateScreen()

        try:
            self.main()
        except Exception:
            self.client.leave()
            sys.exit()

    @staticmethod
    def contain(mode=None):
        width = (WIDTH - 700) // 2
        height = (HEIGHT - 600) // 2
        for count, i in enumerate(range(width, width + 700, 100), 1):
            pos = pygame.mouse.get_pos()
            if i < pos[0] < i + 100 and height < pos[1] < height + 600:
                if mode is None:
                    pygame.draw.rect(screen, 'white', pygame.Rect((0, 0, WIDTH, HEIGHT)))
                    r = pygame.Rect((i, height, 100, 600))
                    pygame.draw.rect(screen, highlightColor, r)
                elif mode == 'box':
                    print("Column:", count)
                    return count

    @staticmethod
    def login():
        try:
            log = Connect()
        except Exception:
            user = input('An error has occurred. Type any key to retry or EXIT: ')
            if user.lower() == "exit":
                exit()
            log = Game.login()
        return log

    def main(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.leave()
                    sys.exit()

            while (playerCount := int(self.client.playerCount())) == 2:
                self.playerCount = playerCount
                for evt in pygame.event.get():
                    if evt.type == pygame.QUIT:
                        self.client.leave()
                        sys.exit()

                self.updateScreen()
                print(screen)

                if self.player_number == 1:
                    print('\nPlayer One\'s Turn')

                    userPlace = self.waitKey()
                    attempt = False
                    while not attempt:
                        attempt = self.c4.place(userPlace, 1)
                        if attempt is False:
                            print("Column is already full.")
                            userPlace = self.waitKey()

                    self.client.send(str(userPlace))
                    self.updateScreen()
                    self.checkWin(1)

                    print(f"\nWaiting for player 2's move . . .\n")
                    self.waiting = True
                    self.updateScreen()
                    opponent_move = self.client.receive()

                    self.c4.place(opponent_move, 2)
                    self.waiting = False

                    self.updateScreen()

                    self.checkWin(2)

                elif self.player_number == 2:
                    print('Waiting for player 1\'s move')
                    self.waiting = True
                    self.updateScreen()

                    opponent_move = self.client.receive()
                    self.c4.place(int(opponent_move), 1)
                    self.waiting = False
                    self.updateScreen()

                    self.checkWin(1)

                    print('\nPlayer Two\'s Turn')
                    userPlace = self.waitKey()
                    attempt = False
                    while not attempt:
                        attempt = self.c4.place(userPlace, 2)
                        if attempt is False:
                            print("Column is already full.")
                            userPlace = self.waitKey()

                    self.client.send(str(userPlace))
                    self.updateScreen()
                    self.checkWin(2)

                pygame.draw.rect(screen, 'white', pygame.Rect((0, 0, WIDTH, HEIGHT)))
                self.draw()
                self.updateScreen()
                pygame.display.update()

            # Time buffer to avoid spam on server
            time.sleep(5)

    def draw(self):
        def createSquare():
            return pygame.Rect(x, y, width, width)

        width = 100
        offset = -50
        y = (HEIGHT - 600) // 2
        for ind1, row in enumerate(self.c4.gameBoard):
            x = (WIDTH-700) // 2
            for ind2, item in enumerate(row):
                rect = createSquare()
                pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
                if item == 1:
                    screen.blit(blackCircle, (rect.center[0]-50, rect.center[1]-50))
                elif item == 2:
                    screen.blit(redCircle, (rect.center[0]+offset, rect.center[1]+offset))
                x += width
            y += width

        playerNumBox = FONT.render(f"Player {self.player_number} (You)", True, (0, 0, 0))
        screen.blit(playerNumBox, playerNumBox.get_rect(center=(screen.get_width()//2, 75)))

        if self.playerCount != 2:
            waitingText1 = FONT.render("Waiting for new challenger . . .", True, (0, 0, 0))
            screen.blit(waitingText1, waitingText1.get_rect(center=(screen.get_width()//2, HEIGHT-75)))
        elif self.waiting:
            waitingText2 = FONT.render("Waiting for next player's move . . .", True, (0, 0, 0))
            screen.blit(waitingText2, waitingText2.get_rect(center=(screen.get_width()//2, HEIGHT-75)))
        else:
            yourTurn = FONT.render("Your Turn . . .", True, (0, 0, 0))
            screen.blit(yourTurn, yourTurn.get_rect(center=(screen.get_width()//2, HEIGHT-75)))

    def waitKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.leave()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result = Game.contain('box')
                    if result:
                        return result

            pygame.draw.rect(screen, 'white', pygame.Rect((0, 0, WIDTH, HEIGHT)))
            Game.contain()
            self.draw()
            pygame.display.update()

    def updateScreen(self):
        screen.fill((255,255,255))
        self.draw()
        pygame.display.update()

    def checkWin(self, playerNumber):
        state = self.c4.check(playerNumber)

        screen.blit(transparentScreen, (0, 0))
        # if state is not False:
        #     rect = pygame.Rect((0, 0, 200, 100))
        #     rect.center = (screen.get_width()//2, HEIGHT-300)
        #     pygame.draw.rect(screen, (240, 240, 240), rect)
        #
        #     playAgain = FONT.render("Play Again", True, (0, 0, 0))
        #     screen.blit(playAgain, playAgain.get_rect(center=(screen.get_width()//2, HEIGHT-300)))

        if state is True:
            time.sleep(1)

            win = FONT.render(f'Player {playerNumber} wins!', True, (0,0,0))
            screen.blit(win, win.get_rect(center=screen.get_rect().center))
            pygame.display.update()
            self.playAgain()

        elif state == "TIE":
            time.sleep(1)

            tied = FONT.render("A Tie!", True, (0, 0, 0))
            screen.blit(tied, tied.get_rect(center=screen.get_rect().center))
            pygame.display.update()
            self.playAgain()

    def playAgain(self):
        rect = pygame.Rect((0, 0, 200, 100))
        rect.center = (screen.get_width() // 2, HEIGHT - 300)

        option1 = False
        option2 = False
        option3 = False

        self_again = False
        opponent_again = False

        while True:
            pos_x, pos_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('test')
                    self.client.leave()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos_x, pos_y)
                    if HEIGHT-350 < pos_y < HEIGHT-250 and WIDTH//2-100 < pos_x < WIDTH//2+100:
                        self_again = True
                        self.client.send(PLAYAGAIN)

            if opponent_again is False:
                opponent = self.client.receive(again=True)
                if opponent == PLAYAGAIN:
                    opponent_again = True

            if opponent_again is False:
                playRequest = self.client.receive(again=True)
                if playRequest == "!!!PLAYAGAIN!!!":
                    opponent_again = True

            if self_again and not opponent_again and not option1:
                msg = FONT.render("Sent play again request to opponent. Please wait or exit.", True, (0,0,0))
                screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2-150)))
                option1 = True
            elif self_again and opponent_again and not option2:
                self.c4.resetBoard()
                self.main()
                option2 = True
            elif not self_again and opponent_again and not option3:
                msg = FONT.render("Opponent wants to play again.", True, (0, 0, 0))
                screen.blit(msg, (0, 0))
                option3 = True
            else:
                # For highlighting box while hovering
                if HEIGHT-350 < pos_y < HEIGHT-250 and WIDTH//2-100 < pos_x < WIDTH//2+100:
                    pygame.draw.rect(screen, (200, 200, 200), rect)
                else:
                    pygame.draw.rect(screen, (240, 240, 240), rect)

                playAgain = FONT.render("Play Again", True, (0, 0, 0))
                screen.blit(playAgain, playAgain.get_rect(center=(screen.get_width()//2, HEIGHT-300)))

            pygame.display.update()


if __name__ == '__main__':
    Game()
