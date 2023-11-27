from itertools import product
import numpy as np
import numpy.typing as npt
from half_chess_board import HalfChessBoard, Move

def encode_board(board: HalfChessBoard) -> npt.NDArray[np.int_]:
    state = board.board
    encoded = np.zeros([11, 8, 4]).astype(int)
    encoder_dict = {'R': 0, 'N': 1, 'B': 2, 'P': 3, 'K': 4,
                    'r': 5, 'n': 6, 'b': 7, 'p': 8, 'k': 9}
    for r, c in product(range(8), range(4)):
        if state[r, c] != ' ':
            encoded[encoder_dict[state[r, c]]][r][c] = 1
    if board.white_to_move:
        encoded[10, :, :] = 1
    return encoded

def decode_board(encoded: npt.NDArray[np.int_]) -> HalfChessBoard:
    state = np.full([8, 4], ' ')
    decoder_dict = 'RNBPKrnbpk'
    for piece, r, c in product(range(10), range(8), range(4)):
        if encoded[piece, r, c] == 1:
            state[r, c] = decoder_dict[piece]
    return HalfChessBoard(
        board = state,
        white_to_move = encoded[10, 0, 0] == 1
    )

def encode_action(move: Move) -> int:
    old_row, old_col, new_row, new_col, prom_row, prom_col = move

    if prom_row is None or prom_col is None:
        encoded = new_col
        encoded = encoded * 8 + new_row
        encoded = encoded * 4 + old_col
        encoded = encoded * 8 + old_row
        return encoded

    color = old_row % 2 # old_row must be 1 or 6 for promotions;
    column_shift = new_col - old_col + 1
    encoded = prom_col
    encoded = encoded * 8 + prom_row
    encoded = encoded * 4 + old_col
    encoded = encoded * 3 + column_shift
    encoded = encoded * 2 + color

    return encoded + 1024


def decode_action(encoded: int) -> Move:
    if encoded < 1024:
        encoded, old_row = divmod(encoded, 8)
        encoded, old_col = divmod(encoded, 4)
        encoded, new_row = divmod(encoded, 8)
        encoded, new_col = divmod(encoded, 4)
        return Move(old_row, old_col, new_row, new_col)
    encoded -= 1024
    encoded, color = divmod(encoded, 2)
    encoded, column_shift = divmod(encoded, 3)
    encoded, old_col = divmod(encoded, 4)
    encoded, prom_row = divmod(encoded, 8)
    encoded, prom_col = divmod(encoded, 4)
    old_row, new_row = (6, 7) if color == 0 else (1, 0)
    new_col = old_col + column_shift - 1
    return Move(old_row, old_col, new_row, new_col, prom_row, prom_col)

if __name__ == '__main__':
    b = HalfChessBoard(
        board=np.array([
            [' ', 'b', ' ', ' '],
            ['P', ' ', ' ', ' '],
            [' ', 'K', ' ', ' '],
            [' ', ' ', 'N', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', 'r', ' '],
            ['k', ' ', ' ', 'p'],
            [' ', ' ', 'B', ' '],
        ]),
        white_to_move=False)

    print(b)
    print(encode_board(b))

    for lm in b.legal_moves:
        assert(lm == decode_action(encode_action(lm)))