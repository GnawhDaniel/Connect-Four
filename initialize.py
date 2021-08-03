import numpy as np


class ConnectFour:
    def __init__(self):
        self.gameBoard = np.zeros((6, 7), dtype=int)

    def place(self, col, playerNum) -> bool:
        """
        :param col: column number
        :param playerNum: int (1 or 2)
        :return: boolean
        """
        col = int(col)
        self.gameBoard = np.flip(self.gameBoard, axis=0)
        for row in self.gameBoard:
            if row[col-1] == 0:
                row[col-1] = playerNum
                self.gameBoard = np.flip(self.gameBoard, axis=0)
                return True
        else:
            print('Game Board is full')
            self.gameBoard = np.flip(self.gameBoard, axis=0)
            return False

    def check(self, playerNum):
        """
        :param playerNum: An integer - 1 or 2
        :return: boolean
        """
        assert playerNum in [1, 2], "playerNum is not an integer (1 or 2)"

        def helper(r):
            count = 0
            for i in r:
                if i == playerNum:
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

        return False

    def resetBoard(self):
        self.gameBoard = np.zeros((6, 7), dtype=int)

