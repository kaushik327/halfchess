"""Modules providing implementation of half-chess board, with legal moves and results."""
import numpy as np
import board

if __name__ == '__main__':
    b = board.Board(np.array([
        [' ', ' ', 'k', ' '],
        [' ', ' ', 'P', ' '],
        [' ', 'K', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', 'B', ' '],
    ]), white_to_move=True)

    while b.result() == 2:
        print(b)
        print('Material:', b.material_advantage())
        print(b.legal_moves)
        r, c, R, C = (int(i) for i in input().split())
        b = b.make_move((r, c, R, C))
    print(b)
    print('Result:', b.result())
