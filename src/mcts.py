# https://ai-boson.github.io/mcts/
# https://www.youtube.com/watch?v=HikhrP5sgQo

import board
import numpy as np


def dummy_model_predict(state):
    value_head = 0.5
    policy_head = {
        (4, 2, 4, 0): 0.5,
        (4, 2, 4, 3): 0.5
    }
    return value_head, policy_head

class Node:
    def __init__(self, prior, state: board.Board):
        self.prior = prior
        self.state = state # contains turn and state
        self.children = {}
        self.value = 0
    
    def expand(self, action_probs):
        """action_probs is a dictionary of moves to probabilities."""
        for move in self.state.legal_moves:
            if move in action_probs and action_probs[move] > 0:
                self.children[move] = Node(
                    prior = action_probs[move],
                    state = self.state.make_move(move)
                )


root = Node(
    prior = 0, 
    state = board.Board(np.array([
        [' ', ' ', ' ', 'k'],
        [' ', ' ', ' ', ' '],
        [' ', ' ', 'K', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', 'R', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
    ]), white_to_move=True)
)


# expand the root
value, probs = dummy_model_predict(root.state)
root.expand(action_probs=probs)


if __name__ == '__main__':
    print(root.state)
    for mv, child in root.children.items():
        print(child.state)
