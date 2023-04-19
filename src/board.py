from itertools import chain, product
from copy import deepcopy
import numpy as np

class Board():

    WHITE_PIECES = 'RNKBP'
    BLACK_PIECES = 'rnkbp'

    def __init__(self):
        self.board = np.array([
            ['r', 'n', 'k', 'b'],
            ['p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P'],
            ['R', 'N', 'K', 'B'],
        ])
        self.white_to_move = True

    def set_board(self, board, white_to_move = True):
        self.board = board
        self.white_to_move = white_to_move

    def __repr__(self):
        return np.array2string(self.board)

    def __is_valid(self, row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 4

    def legal_moves(self, post = False):
        moves = []
        if self.white_to_move:
            for r, c in product(range(8), range(4)):
                if self.board[r, c] == 'P':
                    moves += self.__legal_moves_pawn(r, c, True)
                elif self.board[r, c] == 'N':
                    moves += self.__legal_moves_knight(r, c, True)
                elif self.board[r, c] == 'R':
                    moves += self.__legal_moves_rook(r, c, True)
                elif self.board[r, c] == 'B':
                    moves += self.__legal_moves_bishop(r, c, True)
                elif self.board[r, c] == 'K':
                    moves += self.__legal_moves_king(r, c, True)
        else:
            for r, c in product(range(8), range(4)):
                if self.board[r, c] == 'p':
                    moves += self.__legal_moves_pawn(r, c, False)
                elif self.board[r, c] == 'n':
                    moves += self.__legal_moves_knight(r, c, False)
                elif self.board[r, c] == 'r':
                    moves += self.__legal_moves_rook(r, c, False)
                elif self.board[r, c] == 'b':
                    moves += self.__legal_moves_bishop(r, c, False)
                elif self.board[r, c] == 'k':
                    moves += self.__legal_moves_king(r, c, False)
        return moves if post else [m for m in moves if not self.__in_check_after_move(m)]

    def legal_moves_piece(self, row: int, col: int, post = False):
        moves = []
        if self.white_to_move:
            if self.board[row, col] == 'P':
                moves = self.__legal_moves_pawn(row, col, True)
            elif self.board[row, col] == 'N':
                moves = self.__legal_moves_knight(row, col, True)
            elif self.board[row, col] == 'R':
                moves = self.__legal_moves_rook(row, col, True)
            elif self.board[row, col] == 'B':
                moves = self.__legal_moves_bishop(row, col, True)
            elif self.board[row, col] == 'K':
                moves = self.__legal_moves_king(row, col, True)
        else:
            if self.board[row, col] == 'p':
                moves = self.__legal_moves_pawn(row, col, False)
            elif self.board[row, col] == 'n':
                moves = self.__legal_moves_knight(row, col, False)
            elif self.board[row, col] == 'r':
                moves = self.__legal_moves_rook(row, col, False)
            elif self.board[row, col] == 'b':
                moves = self.__legal_moves_bishop(row, col, False)
            elif self.board[row, col] == 'k':
                moves = self.__legal_moves_king(row, col, False)
        return moves if post else [m for m in moves if not self.__in_check_after_move(m)]

    def make_move(self, move: tuple[int, int, int, int]):
        r, c, R, C = move
        self.board[R, C] = self.board[r, c]
        self.board[r, c] = ' '
        self.white_to_move = not self.white_to_move

    def __in_check(self):
        return self.__in_check_after_move((0, 0, 0, 0))

    def result(self):
        if self.legal_moves() != []:
            # TODO: the game isn't over; throw an exception?
            return 2
        if not self.__in_check():
            return 0
        if self.white_to_move:
            return -1
        return 1

    def __in_check_after_move(self, move: tuple[int, int, int, int]):
        post_board = deepcopy(self)
        post_board.make_move(move)
        for a, b, A, B in post_board.legal_moves(post = True):
            if post_board.board[A, B] == ('k' if post_board.white_to_move else 'K'):
                return True
        return False

    def __legal_moves_pawn(self, row: int, col: int, is_white: bool):
        if row == 0 and is_white or row == 7 and not is_white:
            return []
        moves = []
        can_capture = self.BLACK_PIECES if is_white else self.WHITE_PIECES
        r = -1 if is_white else 1
        if self.board[row + r, col] == ' ':
            moves.append((row, col, row + r, col))
        if col != 0 and self.board[row + r, col - 1] in can_capture:
            moves.append((row, col, row + r, col - 1))
        if col != 3 and self.board[row + r, col + 1] in can_capture:
            moves.append((row, col, row + r, col + 1))
        return moves

    def __legal_moves_king(self, row: int, col: int, is_white: bool):
        moves = []
        cannot_capture = self.WHITE_PIECES if is_white else self.BLACK_PIECES
        for r, c in product((-1, 0, 1), (-1, 0, 1)):
            if (r != 0 or c != 0) \
                and self.__is_valid(row + r, col + c) \
                and self.board[row + r, col + c] not in cannot_capture:
                moves.append((row, col, row + r, col + c))
        return moves

    def __legal_moves_knight(self, row: int, col: int, is_white: bool):
        moves = []
        cannot_capture = self.WHITE_PIECES if is_white else self.BLACK_PIECES
        for r, c in chain(product((1, -1), (2, -2)), product((2, -2), (1, -1))):
            if self.__is_valid(row + r, col + c) and self.board[row + r, col + c] not in cannot_capture:
                moves.append((row, col, row + r, col + c))
        return moves

    def __legal_moves_rook(self, row: int, col: int, is_white: bool):
        moves = []
        cannot_capture = self.WHITE_PIECES if is_white else self.BLACK_PIECES
        # Downward moves
        for r in range(row + 1, 8):
            if self.board[r, col] not in cannot_capture:
                moves.append((row, col, r, col))
            if self.board[r, col] != ' ':
                break
        # Upward moves
        for r in range(row - 1, -1, -1):
            if self.board[r, col] not in cannot_capture:
                moves.append((row, col, r, col))
            if self.board[r, col] != ' ':
                break
        # Rightward moves
        for c in range(col + 1, 4):
            if self.board[row, c] not in cannot_capture:
                moves.append((row, col, row, c))
            if self.board[row, c] != ' ':
                break
        # Leftward moves
        for c in range(col - 1, -1, -1):
            if self.board[row, c] not in cannot_capture:
                moves.append((row, col, row, c))
            if self.board[row, c] != ' ':
                break
        return moves

    def __legal_moves_bishop(self, row: int, col: int, is_white: bool):
        moves = []
        cannot_capture = self.WHITE_PIECES if is_white else self.BLACK_PIECES
        # Down right
        i = 1
        while self.__is_valid(row + i, col + i):
            if self.board[row + i, col + i] not in cannot_capture:
                moves.append((row, col, row + i, col + i))
            if self.board[row + i, col + i] != ' ':
                break
            i += 1
        # Down left
        i = 1
        while self.__is_valid(row + i, col - i):
            if self.board[row + i, col - i] not in cannot_capture:
                moves.append((row, col, row + i, col - i))
            if self.board[row + i, col - i] != ' ':
                break
            i += 1
        # Up right
        i = 1
        while self.__is_valid(row - i, col + i):
            if self.board[row - i, col + i] not in cannot_capture:
                moves.append((row, col, row - i, col + i))
            if self.board[row - i, col + i] != ' ':
                break
            i += 1
        # Up left
        i = 1
        while self.__is_valid(row - i, col - i):
            if self.board[row - i, col - i] not in cannot_capture:
                moves.append((row, col, row - i, col - i))
            if self.board[row - i, col - i] != ' ':
                break
            i += 1
        return moves

