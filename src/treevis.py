"""Module for visualizing MCTS decision trees"""

import networkx as nx
import matplotlib.pyplot as plt

# import mcts

def vis(root, filename=None):
    """Visualizes decision tree from MCTS node."""
    G = nx.DiGraph()
    queue = [root]
    while queue:
        curr = queue.pop(0)
        for action, child in curr.children.items():
            if child.visits > 0:
                G.add_edge(curr, child, action=action)
                queue.append(child)

    plt.figure(figsize=(12, 12))
    pos = nx.nx_agraph.graphviz_layout(G, prog='twopi')
    colors = [node.visits for node in G]
    nx.draw(G, pos, node_color=colors, cmap=plt.cm.viridis)
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'action'))

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, format='PNG')