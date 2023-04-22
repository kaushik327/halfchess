"""Module providing tools to make nested for loops easier to read"""
from itertools import chain, product

from copy import deepcopy
import numpy as np

class Board():
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

    def __init__(self, board=None, white_to_move=True, future=False):
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

        self.legal_moves = self.__get_legal_moves(ignore_pins = future)

    def __repr__(self):
        return '\n'.join('|' + '|'.join(row) + '|' for row in self.board) + '\n'

    def __is_valid(self, row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 4

    def __get_legal_moves(self, ignore_pins = False):
        """Gives array of legal moves in position.
        Each move is formatted (old_row, old_col, new_row, new_col).
        """
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
        return moves if ignore_pins else [m for m in moves if not self.__in_check_after_move(m)]

    def make_move(self, move: tuple[int, int, int, int], future=False):
        """NOT IN-PLACE; RETURNS NEW BOARD.
        Input move should be formatted as (old_row, old_col, new_row, new_col).
        Piece from [old_row, old_col] is moved to [new_row, new_col], leaving a space in its place.
        Player to move is switched. Move validity is NOT checked."""
        old_r, old_c, r, c = move
        state = deepcopy(self.board)
        state[r, c] = state[old_r, old_c]
        state[old_r, old_c] = ' '

        # TODO: upside down pawns
        if r == 0 and state[r, c] == 'P':
            state[r, c] = 'R'
        if r == 7 and state[r, c] == 'p':
            state[r, c] = 'r'

        new_board = Board(state, not self.white_to_move, future=future)
        return new_board

    def __in_check(self):
        return self.__in_check_after_move((0, 0, 0, 0))

    def result(self):
        """Returns result of game.
        2 if the game is still ongoing,
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

    def __in_check_after_move(self, move: tuple[int, int, int, int]):
        post_board = self.make_move(move, future=True)
        for _, _, r, c in post_board.legal_moves:
            if post_board.board[r, c] == ('k' if post_board.white_to_move else 'K'):
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
            if self.__is_valid(row + r, col + c) and \
                self.board[row + r, col + c] not in cannot_capture:
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

    def material_advantage(self):
        """Returns white's material advantage; negative if black is up."""
        ret = 0
        for r, c in product(range(8), range(4)):
            ret += self.point_values[self.board[r, c]]
        return ret

    def __material(self):
        mat = ''
        for r, c in product(range(8), range(4)):
            if self.board[r, c] not in ' Kk':
                mat += self.board[r, c]
        return mat

    def __draw_by_insufficient_material(self):
        return self.__material() in ['N', 'n', 'B', 'b']
        # The case of a dead position with two opposing same-colored bishops is impossible,
        # since there are no same-colored bishops in half-chess.
