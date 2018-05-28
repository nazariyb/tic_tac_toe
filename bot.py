from random import randint
from copy import deepcopy

from data_types.linkedbt import LinkedBT, BTNode
from board import Board


class Bot:
    """simulate player's steps"""

    def _predict_step(self, board):
        """chose the best step of two random variants"""
        game_tree = LinkedBT(board)
        winner = board.check_status()

        board_left = deepcopy(board)
        next_step = randint(0, len(board_left.empty) - 1)
        board_left.set_zero(*board_left.empty.pop(next_step))
        game_tree.insert_left(board_left)
        left_tree = LinkedBT(deepcopy(game_tree.get_root().left))
        l_t = deepcopy(left_tree)

        board_right = deepcopy(board)
        next_step = randint(0, len(board_right.empty) - 1)
        board_right.set_zero(*board_right.empty.pop(next_step))
        game_tree.insert_right(board_right)
        right_tree = LinkedBT(deepcopy(game_tree.get_root().right))
        r_t = deepcopy(right_tree)

        def build_tree(winner, node, board, bot=False):
            """build binary tree of two random possible variants
            of going of game"""
            if winner is None and board.empty:
                board_prev = deepcopy(board)
                if len(board.empty) == 1:
                    next_step = 0
                else:
                    next_step = randint(0, len(board.empty) - 1)
                if bot:
                    board.set_zero(*board.empty.pop(next_step))
                    bot = False
                else:
                    board.set_cross(*board.empty.pop(next_step))
                    bot = True
                winner = board.check_status()
                if node.left is None:
                    node.left = BTNode(deepcopy(board))
                    build_tree(winner, node, board_prev, bot)
                    build_tree(winner, node.right, board, bot)
                else:
                    node.right = BTNode(deepcopy(board))
                    build_tree(winner, node.left, board, bot)

        build_tree(winner, left_tree.get_root(), board_left)
        build_tree(winner, right_tree.get_root(), board_right)

        left = 0
        for b in left_tree.postorder():
            left += int(self._count_score(b))
        right = 0
        for b in right_tree.postorder():
            right += int(self._count_score(b))

        return {'left': (left, l_t.get_root().data),
                'right': (right, r_t.get_root().data)}

    @staticmethod
    def _count_score(board):
        """helpful func to recognize better step"""
        winner = board.check_status()
        if winner == board.ZERO:
            return 1
        elif winner == board.CROSS:
            return -1
        else:
            return 0

    def _where_to_go(self, board):
        """imitate human's step choosing"""
        pass

    def make_step(self, board):
        ways = self._predict_step(board)
        if ways['left'][0] > ways['right'][0]:
            return ways['left'][1]
        else:
            return ways['right'][1]


if __name__ == '__main__':
    bot = Bot()
    board = Board()
    board.set_cross(0, 0)
    board = bot.make_step(board)
    print('RESULT')
    print(board)
