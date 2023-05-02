import math
import sys
import numpy as np
import board
import treevis

def ucb_score(parent, child):
    prior_score = child.prior * math.sqrt(parent.visits) / (child.visits + 1)
    value_score = 0 if child.visits == 0 else (child.value / child.visits)
    return value_score + prior_score

def dummy_model_predict(state: board.HalfChessBoard):
    """Returns value and dictionary of moves to action probabilities."""
    value_head = 0
    num_moves = len(state.legal_moves)
    policy_head = {lm: 1/num_moves for lm in state.legal_moves}
    return value_head, policy_head

class Node:
    """Class representing a node in an MCTS tree."""
    def __init__(self, prior, state: board.HalfChessBoard):
        self.prior = prior
        self.state = state # contains turn and board
        self.children = {}
        self.value = 0
        self.visits = 0

    def expand(self, action_probs):
        """action_probs is a dictionary of moves to probabilities."""
        for move in self.state.legal_moves:
            if move in action_probs and action_probs[move] > 0:
                self.children[move] = Node(
                    prior = action_probs[move],
                    state = self.state.make_move(*move)
                )
    
    def select_child(self):
        max_score, selected_action, selected_child = -99, None, None
        for action, child in self.children.items():
            score = ucb_score(self, child)
            if score >= max_score:
                max_score, selected_action, selected_child = score, action, child
        return selected_action, selected_child

if __name__ == '__main__':

    NUM_SIMULATIONS = 30 if len(sys.argv) == 1 else int(sys.argv[1])

    # initialize root
    root = Node(
        prior = 0,
        state = board.HalfChessBoard(
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
    )
    # expand the root
    value, action_probs = dummy_model_predict(root.state)
    root.expand(action_probs=action_probs)

    # run simulations
    for _ in range(NUM_SIMULATIONS):
        node = root
        search_path = [node]
        while node.children:
            action, node = node.select_child()
            search_path.append(node)
        value = node.state.result()
        if value is None:
            # game isn't over
            value, action_probs = dummy_model_predict(node.state)
            node.expand(action_probs=action_probs)
        for node in search_path:
            node.value += value
            node.visits += 1

    # print(root.state)
    # for mv, child_node in root.children.items():
    #     print(child_node.state, child_node.value)

    treevis.vis(root, 'graph.png')
