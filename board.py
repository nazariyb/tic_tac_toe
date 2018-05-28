class CellIsNotEmpty(IndexError):
    pass


class Board:
    BLANK = '░░'
    CROSS = ' ×'
    ZERO = ' ○'

    def __init__(self):
        self._board = [[Board.BLANK for i in range(3)] for j in range(3)]
        self.last_step = {'coor': None, 'sign': None}
        self.empty = [(i, j) for i in range(3) for j in range(3)]

    def check_status(self):
        """return winner of game if it is else false if draw and none
        otherwise"""
        if self._board[0][0] == self._board[1][1] == self._board[2][2] \
                != Board.BLANK:
            return self._board[1][1]
        if self._board[0][2] == self._board[1][1] == self._board[2][0] \
                != Board.BLANK:
            return self._board[1][1]
        for i in range(3):
            if self._board[i][0] == self._board[i][1] == self._board[i][2] \
                    != Board.BLANK:
                return self._board[i][0]
            if self._board[0][i] == self._board[1][i] == self._board[2][i] \
                    != Board.BLANK:
                return self._board[0][i]
        for i in range(3):
            if Board.BLANK in self._board[i]:
                break
        else:
            return False
        return None

    def _cell_is_valid(self, row, col):
        """check whether coordinates are relevant"""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            raise IndexError
        if self._board[row][col] in (Board.CROSS, Board.ZERO):
            raise CellIsNotEmpty

    def set_cross(self, row, col):
        """mark blank place as 'cross'"""
        self._cell_is_valid(row, col)
        self._board[row][col] = Board.CROSS
        self.last_step['coor'] = (row, col)
        self.last_step['sign'] = Board.CROSS
        if (row, col) in self.empty:
            self.empty.remove((row, col))

    def set_zero(self, row, col):
        """mark blank place as 'zero'"""
        self._cell_is_valid(row, col)
        self._board[row][col] = Board.ZERO
        self.last_step['coor'] = (row, col)
        self.last_step['sign'] = Board.ZERO
        if (row, col) in self.empty:
            self.empty.remove((row, col))

    def __str__(self):
        board = '   0  1  2\n'
        for n, row in enumerate(self._board):
            board += '%d %s\n' % (n, ' '.join(row))
        return board

    def __repr__(self):
        return self._board


if __name__ == '__main__':
    board = Board()
    print(board)
