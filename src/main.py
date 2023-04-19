import board
import numpy as np

if __name__ == '__main__':
    b = board.Board()
    b.set_board(np.array([
        [' ', 'k', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', 'K', ' ', ' '],
        [' ', ' ', ' ', 'R'],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', 'b', ' '],
    ]))

    while True:
        print(b)
        print(b.legal_moves())
        r, c, R, C = (int(i) for i in input().split())
        b.make_move((r, c, R, C))
    
    