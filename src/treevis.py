import networkx as nx
import matplotlib.pyplot as plt

# import mcts

def vis(root):
    G = nx.DiGraph()
    queue = [root]
    while queue:
        curr = queue.pop(0)
        for action, child in curr.children.items():
            G.add_edge(curr, child, attr={'action': action})
            queue.append(child)
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw(G, pos)
    plt.show()
