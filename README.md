# halfchess (WIP)

An engine for half-chess (a chess variant invented by my roommate in my dorm), in imitation of AlphaZero.

## Contents

1. src/half_chess_board.py - implementation of half-chess board
2. src/main.py - interface for self-playing half-chess in the command line
3. src/treevis.py - module for visualizing decision trees
4. src/mcts.py - monte carlo tree search algorithm. when run, outputs decision tree to src/graph.png
5. src/encoder_decoder.py - functions for encoding and decoding states and actions for interaction with neural network