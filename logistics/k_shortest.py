from graph.graph import graph
import networkx as nx
import config as cfg
import logistics.store as store

from itertools import islice


def k_shortest(G, source, target, weight=None):
    return list(
        islice(nx.shortest_simple_paths(G, source, target, weight=weight),
               cfg.k_shortest)
    )


def highlight_k_shortest(node1, node2):
    store.paths_to_highlight = []
    if node1 == node2:
        return
    paths = k_shortest(graph.graph, node1, node2, 'dist')
    for path in paths:
        store.paths_to_highlight.append(path)

# for path in k_shortest_paths(G, 0, 3, 2):
#     print(path)
