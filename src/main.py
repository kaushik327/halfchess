import board
import numpy as np

if __name__ == '__main__':
    b = board.Board()
    b.set_board(np.array([
        [' ', ' ', 'k', ' '],
        [' ', ' ', 'P', ' '],
        [' ', 'K', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', 'B', ' '],
    ]))

    while lm := b.legal_moves():
        print(b)
        print(lm)
        r, c, R, C = (int(i) for i in input().split())
        b.make_move((r, c, R, C))
    print(b)
    print('Result:', b.result())

    