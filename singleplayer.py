from gameboard import ConnectFour
from copy import deepcopy
import numpy as np
import pygame
import sys
import time
import random
import math
import json

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
FONT = pygame.font.Font('assets/RockSalt-Regular.ttf', 23)
FONT_TITLE = pygame.font.Font('assets/RockSalt-Regular.ttf', 50)


blackCircle = pygame.image.load('assets/blackCircle.png').convert_alpha()
blackCircle = pygame.transform.scale(blackCircle, (100, 100))

redCircle = pygame.image.load('assets/redCircle.png').convert_alpha()
redCircle = pygame.transform.scale(redCircle, (100, 100))

main_menu_button = pygame.Rect((0, 0, 200, 100))
main_menu_button.center = main_width, main_height = (100, 750)
main_menu = FONT.render("Main Menu", True, (0, 0, 0))

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

pygame.display.update()


class SPGame:
    def __init__(self):
        self.c4 = ConnectFour()
        self.historyDict = None
        self.difficulty = 5
        self.difficultyDict = {
            2: "easy",
            3: "normal",
            5: "hard"
        }

        self.noSkip = True
        self.waiting = False

        self.preScreen()

    @staticmethod
    def getAllOpenColumns(board) -> list:
        gameBoardCopy = np.transpose(deepcopy(board))
        possibleMoves = [col for col, row in enumerate(gameBoardCopy) if 0 in row]
        return possibleMoves

    @staticmethod
    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    @staticmethod
    def score_position(board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += SPGame.evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += SPGame.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += SPGame.evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += SPGame.evaluate_window(window, piece)

        return score

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
                    return count

    @staticmethod
    def miniMax(board, depth, alpha, beta, isMaximizer):
        c4 = ConnectFour()
        c4.gameBoard = deepcopy(board)
        board_copy = deepcopy(board)

        if c4.check(2):
            return None, 100000000000
        elif c4.check(1):
            return None, -100000000000
        elif c4.check(1) == "TIE":
            return None, 0
        elif depth == 0:
            return None, SPGame.score_position(c4.gameBoard, AI_PIECE)

        openCols = SPGame.getAllOpenColumns(c4.gameBoard)
        random.shuffle(openCols)
        if isMaximizer:
            value = -math.inf
            column = random.choice(openCols)
            for col in openCols:
                col += 1  # Index starts at 1
                c4.place(col, 2)
                new_score = SPGame.miniMax(c4.gameBoard, depth - 1, alpha, beta, False)[1]
                c4.gameBoard = deepcopy(board_copy)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = math.inf
            column = random.choice(openCols)
            for col in openCols:
                col += 1
                c4.place(col, 1)
                new_score = SPGame.miniMax(c4.gameBoard, depth - 1, alpha, beta, True)[1]
                c4.gameBoard = deepcopy(board_copy)

                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def draw(self):
        def createSquare():
            return pygame.Rect(x, y, width, width)

        width = 100
        offset = -50
        y = (HEIGHT - 600) // 2

        pygame.draw.line(screen, (0, 0, 0), (0, 48), (WIDTH, 48), width=2)

        for ind1, row in enumerate(self.c4.gameBoard):
            x = (WIDTH - 700) // 2
            for ind2, item in enumerate(row):
                rect = createSquare()
                pygame.draw.rect(screen, (0, 0, 0), rect, width=2)
                if item == 1:
                    screen.blit(blackCircle, (rect.center[0] - 50, rect.center[1] - 50))
                elif item == 2:
                    screen.blit(redCircle, (rect.center[0] + offset, rect.center[1] + offset))
                x += width
            y += width

        file = open('assets/history.json', 'r')
        self.historyDict = json.load(file)
        file.close()

        tieHistory = FONT.render(f"Tie(s): {self.historyDict[self.difficultyDict[self.difficulty]]['tie']}",
                                 True, (0, 0, 0))
        screen.blit(tieHistory, (WIDTH-200, 0))

        scoreHistory = FONT.render(f" Wins: {self.historyDict[self.difficultyDict[self.difficulty]]['player1']}",
                                   True, (0, 0, 0))
        screen.blit(scoreHistory, (0, 0))

        scoreHistoryAI = FONT.render(f"Losses: {self.historyDict[self.difficultyDict[self.difficulty]]['player2']}",
                                     True, (0, 0, 0))
        screen.blit(scoreHistoryAI, scoreHistory.get_rect(center=(screen.get_width()//2, 25)))

        difficultyBox = FONT.render(f"Difficulty: {self.difficultyDict[self.difficulty]}", True, (0, 0, 0))
        screen.blit(difficultyBox, (150, 50))

        if self.waiting:
            waitingText2 = FONT.render("Opponent (AI) is calculating next move . . .", True, (0, 0, 0))
            screen.blit(waitingText2, waitingText2.get_rect(center=(screen.get_width() // 2, HEIGHT - 75)))
        else:
            yourTurn = FONT.render("Player's Turn . . .", True, (0, 0, 0))
            screen.blit(yourTurn, yourTurn.get_rect(center=(screen.get_width() // 2, HEIGHT - 75)))

    def preScreen(self):
        isExit = False
        rectYes = pygame.Rect((0, 0, 200, 100))
        rectYes.center = (screen.get_width() // 2, HEIGHT - 300)

        rectNo = pygame.Rect((0, 0, 200, 100))
        rectNo.center = (screen.get_width() // 2, HEIGHT - 400)

        yes = FONT.render("YES", True, (0, 0, 0))
        no = FONT.render("NO", True, (0, 0, 0))
        message = FONT_TITLE.render("Go first?", True, (0, 0, 0))
        while True:
            clicked = False
            pos_x, pos_y = pygame.mouse.get_pos()
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    sys.exit()
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            screen.fill('white')

            if HEIGHT - 350 < pos_y < HEIGHT - 250 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                pygame.draw.rect(screen, (120, 120, 120), rectYes)
                if clicked:
                    self.noSkip = False
                    isExit = self.setDifficulty()
            else:
                pygame.draw.rect(screen, (255, 255, 255), rectYes)

            if HEIGHT - 450 < pos_y < HEIGHT - 350 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                pygame.draw.rect(screen, (120, 120, 120), rectNo)
                if clicked:
                    isExit = self.setDifficulty()
            else:
                pygame.draw.rect(screen, (255, 255, 255), rectNo)

            if main_width - 100 < pos_x < main_width + 100 and main_height - 100 < pos_y < main_height + 100:
                pygame.draw.rect(screen, (120, 120, 120), main_menu_button)
                if clicked:
                    break

            screen.blit(yes, yes.get_rect(center=(screen.get_width() // 2, HEIGHT - 400)))
            screen.blit(no, no.get_rect(center=(screen.get_width() // 2, HEIGHT - 300)))

            screen.blit(message, message.get_rect(center=(screen.get_width() // 2, 200)))
            screen.blit(main_menu, main_menu.get_rect(center=(100, 750)))

            if isExit:
                break

            pygame.display.update()

    def setDifficulty(self):
        isExit = False
        easy = pygame.Rect((0, 0, 200, 100))
        easy.center = (screen.get_width() // 2, HEIGHT - 300)

        normal = pygame.Rect((0, 0, 200, 100))
        normal.center = (screen.get_width() // 2, HEIGHT - 400)

        hard = pygame.Rect((0, 0, 200, 100))
        hard.center = (screen.get_width() // 2, HEIGHT - 200)

        while True:
            pos_x, pos_y = pygame.mouse.get_pos()
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    sys.exit()
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    if HEIGHT - 450 < pos_y < HEIGHT - 350 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                        self.difficulty = 2
                        isExit = self.start()
                    elif HEIGHT - 350 < pos_y < HEIGHT - 250 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                        self.difficulty = 3
                        isExit = self.start()
                    elif HEIGHT - 250 < pos_y < HEIGHT - 150 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                        self.difficulty = 5
                        isExit = self.start()

            if isExit:
                return True

            screen.fill('white')

            if HEIGHT - 350 < pos_y < HEIGHT - 250 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                pygame.draw.rect(screen, (120, 120, 120), easy)
            else:
                pygame.draw.rect(screen, (255, 255, 255), easy)

            if HEIGHT - 450 < pos_y < HEIGHT - 350 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                pygame.draw.rect(screen, (120, 120, 120), normal)
            else:
                pygame.draw.rect(screen, (255, 255, 255), normal)

            if HEIGHT - 250 < pos_y < HEIGHT - 150 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                pygame.draw.rect(screen, (120, 120, 120), hard)

            easyFont = FONT.render("EASY", True, (0, 0, 0))
            screen.blit(easyFont, easyFont.get_rect(center=(screen.get_width() // 2, HEIGHT - 400)))

            normalFont = FONT.render("NORMAL", True, (0, 0, 0))
            screen.blit(normalFont, normalFont.get_rect(center=(screen.get_width() // 2, HEIGHT - 300)))

            hardFont = FONT.render("HARD", True, (0, 0, 0))
            screen.blit(hardFont, hardFont.get_rect(center=(screen.get_width() // 2, HEIGHT - 200)))

            message = FONT_TITLE.render("Select Difficulty", True, (0, 0, 0))
            screen.blit(message, message.get_rect(center=(screen.get_width() // 2, 200)))

            pygame.display.update()

    def start(self):
        rand = True
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    sys.exit()

            self.updateScreen()

            if self.noSkip:
                # Player's Turn
                userPlace = self.waitKey()
                if userPlace == "exit":  # Exits to main menu
                    return True
                attempt = False
                while not attempt:
                    attempt = self.c4.place(userPlace, 1)
                    if attempt is False:
                        print("Column is already full.")
                        userPlace = self.waitKey()

                self.updateScreen()
                isExit = self.checkWin(1)

            # AI's turn
            self.waiting = True
            self.updateScreen()

            if rand:
                time.sleep(1)
                col = random.choice(range(1, 8))
                rand = False
            else:
                col, _score = SPGame.miniMax(self.c4.gameBoard, self.difficulty, -math.inf, math.inf, True)

            self.c4.place(col, 2)
            self.waiting = False

            self.updateScreen()
            isExit = self.checkWin(2)

            self.noSkip = True

            if isExit:
                return True

    def updateScreen(self):
        screen.fill((255, 255, 255))
        self.draw()
        pygame.display.update()

    def checkWin(self, playerNumber):
        isExit = False
        state = self.c4.check(playerNumber)
        screen.blit(transparentScreen, (0, 0))

        if state is True:
            file = open("assets/history.json", 'w')
            self.historyDict[self.difficultyDict[self.difficulty]]['player'+str(playerNumber)] += 1
            file.write(json.dumps(self.historyDict))
            file.close()

            win = FONT.render(f'Player {playerNumber} wins!', True, (0, 0, 0))
            screen.blit(win, win.get_rect(center=(screen.get_width() // 2, HEIGHT - 500)))
            pygame.display.update()

            isExit = self.playAgain()

        elif state == "TIE":
            file = open("assets/history.json", 'w')
            self.historyDict[self.difficultyDict[self.difficulty]]["tie"] += 1
            file.write(json.dumps(self.historyDict))
            file.close()

            tied = FONT.render("A Tie!", True, (0, 0, 0))
            screen.blit(tied, tied.get_rect(center=(screen.get_width() // 2, HEIGHT - 500)))
            pygame.display.update()

            isExit = self.playAgain()

        return isExit

    def waitKey(self):
        while True:
            screen.fill("white")
            clicked = False
            result = None
            pos_x, pos_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    result = SPGame.contain('box')

            if result and clicked:
                return result

            if main_width - 100 < pos_x < main_width + 100 and main_height - 100 < pos_y < main_height + 100:
                pygame.draw.rect(screen, (120, 120, 120), main_menu_button)
                if clicked:
                    return "exit"

            SPGame.contain()
            screen.blit(main_menu, main_menu.get_rect(center=(100, 750)))
            self.draw()
            pygame.display.update()

    def playAgain(self):
        rect = pygame.Rect((0, 0, 200, 100))
        rect.center = (screen.get_width() // 2, HEIGHT - 400)
        while True:
            pos_x, pos_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if HEIGHT - 450 < pos_y < HEIGHT - 350 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                        self.c4.resetBoard()
                        self.preScreen()
                        return True  # If user clicks main menu, it breaks all while loops

            if HEIGHT - 450 < pos_y < HEIGHT - 350 and WIDTH // 2 - 100 < pos_x < WIDTH // 2 + 100:
                pygame.draw.rect(screen, (200, 200, 200), rect)
            else:
                pygame.draw.rect(screen, (240, 240, 240), rect)

            playAgain = FONT.render("Play Again", True, (0, 0, 0))
            screen.blit(playAgain, playAgain.get_rect(center=(screen.get_width() // 2, HEIGHT - 400)))

            pygame.display.update()


if __name__ == "__main__":
    SPGame()
