import numpy as np


class ConnectFour:
    def __init__(self):
        self.gameBoard = np.zeros((6, 7), dtype=int)

    def place(self, col, playerNum) -> bool:
        """
        Places an integer (representing the player) into the game board.

        :param col: column number
        :param playerNum: int (1 or 2)
        :return: boolean
        """
        col = int(col)
        self.gameBoard = np.flip(self.gameBoard, axis=0)
        for row in self.gameBoard:
            if row[col - 1] == 0:
                row[col - 1] = playerNum
                self.gameBoard = np.flip(self.gameBoard, axis=0)
                return True
        else:
            self.gameBoard = np.flip(self.gameBoard, axis=0)
            return False

    def check(self, player_num):
        """
        Checks if playerNum has won the game.

        :param player_num: An integer - 1 or 2
        :return: boolean
        """
        assert player_num in [1, 2], "playerNum is not an integer (1 or 2)"

        def helper(r):
            """
            Checks if any player (1 or 2) has four in the given row.

            :param r: 1 x n vector
            :return: boolean
            """
            count = 0
            for i in r:
                if i == player_num:
                    count += 1
                else:
                    count = 0
                if count == 4:
                    return True
            return False

        # Horizontal Check
        for row in self.gameBoard.copy():
            if helper(row):
                return True

        # Vertical Check
        for col in np.transpose(self.gameBoard).copy():
            if helper(col):
                return True

        # Diagonal Check
        for num in range(-2, 4):
            if helper(np.diag(self.gameBoard, k=num)):
                return True
            if helper(np.diag(np.fliplr(self.gameBoard), k=num)):
                return True

        if 0 not in self.gameBoard:
            return "TIE"

        return False

    def playableCol(self):
        """
        :return: a list of empty, playable columns of the current game board.
        """
        gameBoardCopy = np.transpose(self.gameBoard.copy())
        possibleMoves = [col for col, row in enumerate(gameBoardCopy) if 0 in row]
        return possibleMoves

    def resetBoard(self):
        """Resets self.gameboard into a matrix of zeros."""
        self.gameBoard = np.zeros((6, 7), dtype=int)
