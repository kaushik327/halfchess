"""Main file"""

import numpy as np
from half_chess_board import HalfChessBoard, Move

if __name__ == '__main__':
    b = HalfChessBoard(
        board=np.array([
            [' ', 'k', ' ', ' '],
            [' ', ' ', ' ', 'B'],
            [' ', 'K', ' ', ' '],
            [' ', ' ', 'N', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
        ]),
        white_to_move=True)

    while b.result() is None:
        print(b)
        print('Material:', b.material_advantage())
        print(b.legal_moves)
        move = Move(*(int(i) for i in input().split()))
        print(move)
        b = b.make_move(move)
        
    print(b)
    print('Result:', b.result())
