class CellIsNotEmpty(IndexError):
    pass


class Board:
    BLANK = '░░'
    CROSS = ' ×'
    ZERO = ' ○'
    def __init__(self):
        self._board = [[Board.BLANK for i in range(3)] for j in range(3)]
        self.last_step = {'coor': None, 'sign': None}
        self._empty = set(((i, j) for i in range(3)) for j in range(3))

    def check_status(self):
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
        assert 0 <= row <= 2 and 0 <= col <= 2, IndexError
        assert (row, col) in self._empty, CellIsNotEmpty

    def set_cross(self, row, col):
        self._cell_is_valid(row, col)
        self._board[row][col] = Board.CROSS

    def set_zero(self, row, col):
        self._cell_is_valid(row, col)
        self._board[row][col] = Board.ZERO

    def __str__(self):
        # self._board[1][0] = Board.CROSS
        # self._board[1][1] = Board.ZERO
        # self._board[1][2] = Board.CROSS
        # self._board[2][0] = Board.ZERO
        # self._board[2][1] = Board.CROSS
        # self._board[2][2] = Board.ZERO
        board = '   0  1  2\n'
        for n, row in enumerate(self._board):
            # board += str(n) + ' ' + ' '.join(row) + '\n'
            board += '%d %s\n' % (n, ' '.join(row))
        return board

if __name__ == '__main__':
    board = Board()
    print(board)
