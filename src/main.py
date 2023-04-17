import board
if __name__ == '__main__':
    b = board.Board()
    b.make_move((6, 2, 5, 2))
    b.make_move((1, 2, 2, 2))

    print(b)
    print(b.legal_moves())
    print(b.legal_moves_piece(7, 3))
