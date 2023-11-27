"""Implementation of object representing the half-chess board."""

from __future__ import annotations
from itertools import chain, product
from copy import deepcopy
import numpy as np
from typing import Optional, NamedTuple


class Move(NamedTuple): 
    """Represents a move from [old_r, old_c] to [new_r, new_c], possibly taking out the piece at [prom_r, prom_c]."""
    old_r: int
    old_c: int
    new_r: int
    new_c: int
    prom_r: Optional[int] = None
    prom_c: Optional[int] = None

    def is_promotion(self):
        return self.prom_r is not None and self.prom_c is not None

    def __repr__(self):
        if self.is_promotion():
            return f"({self.old_r}{self.old_c}, {self.new_r}{self.new_c}, {self.prom_r}{self.prom_c})"
        return f"({self.old_r}{self.old_c}, {self.new_r}{self.new_c})"

class HalfChessBoard:
    """Class representing the board's state. Also provides legal moves in position."""

    WHITE_PIECES = 'RNKBP'
    BLACK_PIECES = 'rnkbp'
    point_values = {'R': 5,
                    'N': 3,
                    'B': 3,
                    'P': 1, 
                    'K': 0,
                    'r': -5,
                    'n': -3,
                    'b': -3,
                    'p': -1,
                    'k': 0,
                    ' ': 0}

    def __init__(self, board=None, white_to_move=True, ignore_pins=False):
        if board is None:
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
        else:
            self.board = board
        self.white_to_move = white_to_move
        self.ignore_pins = ignore_pins
        self.legal_moves = []
        self.legal_moves = self.__get_legal_moves()

    def __repr__(self) -> str:
        return '\n'.join('|' + '|'.join(row) + '|' for row in self.board) + '\n'

    def __is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 4

    def __get_legal_moves(self) -> list[Move]:
        """Gives array of legal moves in position.
        Each move is formatted (old_row, old_col, new_row, new_col).
        """
        moves = []
        if self.white_to_move:
            for r, c in product(range(8), range(4)):
                if self.board[r, c] == 'P':
                    moves += self.__legal_moves_P(r, c)
                elif self.board[r, c] == 'N':
                    moves += self.__legal_moves_N(r, c)
                elif self.board[r, c] == 'R':
                    moves += self.__legal_moves_R(r, c)
                elif self.board[r, c] == 'B':
                    moves += self.__legal_moves_B(r, c)
                elif self.board[r, c] == 'K':
                    moves += self.__legal_moves_K(r, c)
        else:
            for r, c in product(range(8), range(4)):
                if self.board[r, c] == 'p':
                    moves += self.__legal_moves_p(r, c)
                elif self.board[r, c] == 'n':
                    moves += self.__legal_moves_n(r, c)
                elif self.board[r, c] == 'r':
                    moves += self.__legal_moves_r(r, c)
                elif self.board[r, c] == 'b':
                    moves += self.__legal_moves_b(r, c)
                elif self.board[r, c] == 'k':
                    moves += self.__legal_moves_k(r, c)
        if self.ignore_pins:
            return moves
        return [m for m in moves if not self.__in_check_after_move(m)]

    def make_move(self, move: Move, future=False) -> HalfChessBoard:
        """NOT IN-PLACE; RETURNS NEW BOARD.
        Input move should be formatted as (old_row, old_col, new_row, new_col).
        Piece from [old_row, old_col] is moved to [new_row, new_col], leaving a space in its place.
        Player to move is switched. Move validity is checked."""

        old_r, old_c, r, c, prom_r, prom_c = move

        if self.legal_moves:
            if move not in self.legal_moves:
                raise ValueError('invalid move')

        state = deepcopy(self.board)
        if old_r == r and old_c == c:
            return HalfChessBoard(state, not self.white_to_move, ignore_pins=future)
        state[r, c] = state[old_r, old_c]
        state[old_r, old_c] = ' '

        if r == 0 and state[r, c] == 'P' or r == 7 and state[r, c] == 'p':
            state[r, c] = ' '
            if prom_r is not None and prom_c is not None:
                state[prom_r, prom_c] = ' '

        new_board = HalfChessBoard(state, not self.white_to_move, ignore_pins=future)
        return new_board

    def __in_check(self) -> bool:
        return self.__in_check_after_move(Move(0, 0, 0, 0))

    def result(self) -> Optional[int]:
        """Returns result of game.
        None if the game is still ongoing,
        0 for stalemate,
        -1 for black win,
        1 for white win."""
        if self.legal_moves != []:
            if self.__draw_by_insufficient_material():
                return 0
            return None
        if not self.__in_check():
            return 0
        if self.white_to_move:
            return -1
        return 1

    def __in_check_after_move(self, move: Move) -> bool:
        post_board = self.make_move(move, future=True)
        king = 'k' if post_board.white_to_move else 'K'
        for legal_move in post_board.legal_moves:
            if post_board.board[legal_move.new_r, legal_move.new_c] == king:
                return True
        return False

    def __legal_moves_P(self, row: int, col: int) -> list[Move]:
        if row == 0:
            return []
        moves = []

        capturable_coords = []
        if row == 1:
            for r, c in product(range(8), range(4)):
                if self.board[r, c] in self.BLACK_PIECES and self.board[r, c] not in 'Kk':
                    capturable_coords.append((r, c))

        if self.board[row - 1, col] == ' ':
            flag = True
            for cap_r, cap_c in capturable_coords:
                flag = False
                moves.append(Move(row, col, row - 1, col, cap_r, cap_c))
            if flag:
                moves.append(Move(row, col, row - 1, col))

        if col != 0 and self.board[row - 1, col - 1] in self.BLACK_PIECES:
            flag = True
            for cap_r, cap_c in capturable_coords:
                if cap_r != row - 1 and cap_c != col - 1:
                    flag = False
                    moves.append(Move(row, col, row - 1, col - 1, cap_r, cap_c))
            if flag:
                moves.append(Move(row, col, row - 1, col - 1))

        if col != 3 and self.board[row - 1, col + 1] in self.BLACK_PIECES:
            flag = True
            for cap_r, cap_c in capturable_coords:
                if cap_r != row - 1 and cap_c != col + 1:
                    flag = False
                    moves.append(Move(row, col, row - 1, col + 1, cap_r, cap_c))
            if flag:
                moves.append(Move(row, col, row - 1, col + 1))

        return moves
    
    def __legal_moves_p(self, row: int, col: int) -> list[Move]:
        if row == 7:
            return []
        moves = []

        capturable_coords = []
        if row == 6:
            for r, c in product(range(8), range(4)):
                if self.board[r, c] in self.WHITE_PIECES and self.board[r, c] not in 'Kk':
                    capturable_coords.append((r, c))

        if self.board[row + 1, col] == ' ':
            flag = True
            for cap_r, cap_c in capturable_coords:
                flag = False
                moves.append(Move(row, col, row + 1, col, cap_r, cap_c))
            if flag:
                moves.append(Move(row, col, row + 1, col))

        if col != 0 and self.board[row + 1, col - 1] in self.WHITE_PIECES:
            flag = True
            for cap_r, cap_c in capturable_coords:
                if cap_r != row + 1 and cap_c != col - 1:
                    flag = False
                    moves.append(Move(row, col, row + 1, col - 1, cap_r, cap_c))
            if flag:
                moves.append(Move(row, col, row + 1, col - 1))

        if col != 3 and self.board[row + 1, col + 1] in self.WHITE_PIECES:
            flag = True
            for cap_r, cap_c in capturable_coords:
                if cap_r != row + 1 and cap_c != col + 1:
                    flag = False
                    moves.append(Move(row, col, row + 1, col + 1, cap_r, cap_c))
            if flag:
                moves.append(Move(row, col, row + 1, col + 1))

        return moves

    def __legal_moves_K(self, row: int, col: int) -> list[Move]:
        moves = []
        for r, c in product((-1, 0, 1), (-1, 0, 1)):
            if (r != 0 or c != 0) \
                and self.__is_valid(row + r, col + c) \
                and self.board[row + r, col + c] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row + r, col + c))
        return moves
    
    def __legal_moves_k(self, row: int, col: int) -> list[Move]:
        moves = []
        for r, c in product((-1, 0, 1), (-1, 0, 1)):
            if (r != 0 or c != 0) \
                and self.__is_valid(row + r, col + c) \
                and self.board[row + r, col + c] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row + r, col + c))
        return moves

    def __legal_moves_N(self, row: int, col: int) -> list[Move]:
        moves = []
        for r, c in chain(product((1, -1), (2, -2)), product((2, -2), (1, -1))):
            if self.__is_valid(row + r, col + c) and \
                self.board[row + r, col + c] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row + r, col + c))
        return moves
    
    def __legal_moves_n(self, row: int, col: int) -> list[Move]:
        moves = []
        for r, c in chain(product((1, -1), (2, -2)), product((2, -2), (1, -1))):
            if self.__is_valid(row + r, col + c) and \
                self.board[row + r, col + c] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row + r, col + c))
        return moves

    def __legal_moves_R(self, row: int, col: int) -> list[Move]:
        moves = []
        # Downward moves
        for r in range(row + 1, 8):
            if self.board[r, col] not in self.WHITE_PIECES:
                moves.append(Move(row, col, r, col))
            if self.board[r, col] != ' ':
                break
        # Upward moves
        for r in range(row - 1, -1, -1):
            if self.board[r, col] not in self.WHITE_PIECES:
                moves.append(Move(row, col, r, col))
            if self.board[r, col] != ' ':
                break
        # Rightward moves
        for c in range(col + 1, 4):
            if self.board[row, c] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row, c))
            if self.board[row, c] != ' ':
                break
        # Leftward moves
        for c in range(col - 1, -1, -1):
            if self.board[row, c] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row, c))
            if self.board[row, c] != ' ':
                break
        return moves
    
    def __legal_moves_r(self, row: int, col: int) -> list[Move]:
        moves = []
        # Downward moves
        for r in range(row + 1, 8):
            if self.board[r, col] not in self.BLACK_PIECES:
                moves.append(Move(row, col, r, col))
            if self.board[r, col] != ' ':
                break
        # Upward moves
        for r in range(row - 1, -1, -1):
            if self.board[r, col] not in self.BLACK_PIECES:
                moves.append(Move(row, col, r, col))
            if self.board[r, col] != ' ':
                break
        # Rightward moves
        for c in range(col + 1, 4):
            if self.board[row, c] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row, c))
            if self.board[row, c] != ' ':
                break
        # Leftward moves
        for c in range(col - 1, -1, -1):
            if self.board[row, c] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row, c))
            if self.board[row, c] != ' ':
                break
        return moves

    def __legal_moves_B(self, row: int, col: int) -> list[Move]:
        moves = []
        # Down right
        i = 1
        while self.__is_valid(row + i, col + i):
            if self.board[row + i, col + i] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row + i, col + i))
            if self.board[row + i, col + i] != ' ':
                break
            i += 1
        # Down left
        i = 1
        while self.__is_valid(row + i, col - i):
            if self.board[row + i, col - i] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row + i, col - i))
            if self.board[row + i, col - i] != ' ':
                break
            i += 1
        # Up right
        i = 1
        while self.__is_valid(row - i, col + i):
            if self.board[row - i, col + i] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row - i, col + i))
            if self.board[row - i, col + i] != ' ':
                break
            i += 1
        # Up left
        i = 1
        while self.__is_valid(row - i, col - i):
            if self.board[row - i, col - i] not in self.WHITE_PIECES:
                moves.append(Move(row, col, row - i, col - i))
            if self.board[row - i, col - i] != ' ':
                break
            i += 1
        return moves
    
    def __legal_moves_b(self, row: int, col: int) -> list[Move]:
        moves = []
        # Down right
        i = 1
        while self.__is_valid(row + i, col + i):
            if self.board[row + i, col + i] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row + i, col + i))
            if self.board[row + i, col + i] != ' ':
                break
            i += 1
        # Down left
        i = 1
        while self.__is_valid(row + i, col - i):
            if self.board[row + i, col - i] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row + i, col - i))
            if self.board[row + i, col - i] != ' ':
                break
            i += 1
        # Up right
        i = 1
        while self.__is_valid(row - i, col + i):
            if self.board[row - i, col + i] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row - i, col + i))
            if self.board[row - i, col + i] != ' ':
                break
            i += 1
        # Up left
        i = 1
        while self.__is_valid(row - i, col - i):
            if self.board[row - i, col - i] not in self.BLACK_PIECES:
                moves.append(Move(row, col, row - i, col - i))
            if self.board[row - i, col - i] != ' ':
                break
            i += 1
        return moves

    def material_advantage(self) -> int:
        """Returns white's material advantage; negative if black is up."""
        ret = 0
        for r, c in product(range(8), range(4)):
            ret += self.point_values[self.board[r, c]]
        return ret

    def __material(self) -> str:
        mat = ''
        for r, c in product(range(8), range(4)):
            if self.board[r, c] not in ' Kk':
                mat += self.board[r, c]
        return mat

    def __draw_by_insufficient_material(self) -> bool:
        return self.__material() in ['N', 'n', 'B', 'b', '']
        # The case of a dead position with two opposing same-colored bishops is impossible,
        # since there are no same-colored bishops in half-chess.
