"""Main file"""

import board
import numpy as np

if __name__ == '__main__':
    b = board.HalfChessBoard(
        board=np.array([
            [' ', 'b', ' ', ' '],
            ['P', ' ', ' ', ' '],
            [' ', 'K', ' ', ' '],
            [' ', ' ', 'N', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', 'r', ' '],
            [' ', 'k', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]),
        white_to_move=True)

    while b.result() is None:
        print(b)
        print('Material:', b.material_advantage())
        print(b.legal_moves)
        move = (int(i) for i in input().split())
        b = b.make_move(*move)
    print(b)
    print('Result:', b.result())
