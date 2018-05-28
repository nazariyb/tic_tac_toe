from board import Board, CellIsNotEmpty
import os

from bot import Bot


def player_step(board):
    """help to check player's input and make step"""
    while True:
        inp = input().strip()
        try:
            board.set_cross(int(inp[0]), int(inp[-1]))
        except (IndexError, CellIsNotEmpty):
            print('your input was bad, try again')
            continue
        else:
            break


def play():
    """imitate game with computer"""
    board = Board()
    bot = Bot()
    winner = board.check_status()
    os.system('cls')
    print(board)
    while winner is None:
        print('human, your turn...')
        print('enter number of row and number of column in one row')
        player_step(board)
        os.system('cls')
        print(board)
        winner = board.check_status()
        if winner != None:
            break
        board = bot.make_step(board)
        os.system('cls')
        print(board)
        winner = board.check_status()
    if winner == board.CROSS:
        print('congrats, human!\nyou won!')
    elif winner == board.ZERO:
        print('oh human, you lost')
    else:
        print('draw, let\'s try next time')


if __name__ == '__main__':
    play()
