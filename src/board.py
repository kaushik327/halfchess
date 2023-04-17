from itertools import chain, product
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

    def __repr__(self):
        return np.array2string(self.board)

    def __is_valid(self, row: int, col: int):
        return 0 <= row < 8 and 0 <= col < 4

    def make_move(self, move: tuple[int, int, int, int]):
        r, c, R, C = move
        self.board[R, C] = self.board[r, c]
        self.board[r, c] = ' '
        self.white_to_move = not self.white_to_move

    def legal_moves(self):
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
        return moves

    def legal_moves_piece(self, row: int, col: int):
        if self.white_to_move:
            if self.board[row, col] == 'P':
                return self.__legal_moves_pawn(row, col, True)
            if self.board[row, col] == 'N':
                return self.__legal_moves_knight(row, col, True)
            if self.board[row, col] == 'R':
                return self.__legal_moves_rook(row, col, True)
            if self.board[row, col] == 'B':
                return self.__legal_moves_bishop(row, col, True)
            if self.board[row, col] == 'K':
                return self.__legal_moves_king(row, col, True)
        else:
            if self.board[row, col] == 'p':
                return self.__legal_moves_pawn(row, col, False)
            if self.board[row, col] == 'n':
                return self.__legal_moves_knight(row, col, False)
            if self.board[row, col] == 'r':
                return self.__legal_moves_rook(row, col, False)
            if self.board[row, col] == 'b':
                return self.__legal_moves_bishop(row, col, False)
            if self.board[row, col] == 'k':
                return self.__legal_moves_king(row, col, False)
        return []

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

