import pandas as pd
from typing import List


class Graph:
    def __init__(self):
        nodes_df = pd.read_csv('graph_data/variant4/nodes.csv').dropna()
        edges_df = pd.read_csv('graph_data/variant4/edges.csv').dropna()
        nodes_tuple = tuple(zip(range(len(nodes_df)),
                                nodes_df['type'],
                                nodes_df['x'],
                                nodes_df['y']))
        self.nodes_dict = [dict(zip(['index',
                                     'type',
                                     'x',
                                     'y'], x)) for x in nodes_tuple]
        edges_tuple = tuple(zip(range(len(edges_df)),
                                edges_df['node1'],
                                edges_df['node2'],
                                edges_df['weight'],
                                edges_df['min_type']))
        self.edges_dict = [dict(zip(['index',
                                     'node1',
                                     'node2',
                                     'weight',
                                     'min_type'], x)) for x in edges_tuple]

    def get_all_edges(self) -> List[dict]:
        return self.edges_dict

    def get_all_nodes(self) -> List[dict]:
        return self.nodes_dict

    def get_small_edges(self) -> List[dict]:
        return list(filter(lambda x: x['min_type'] == 0, self.edges_dict))

    def get_medium_edges(self) -> List[dict]:
        return list(filter(lambda x: x['min_type'] == 1, self.edges_dict))

    def get_large_edges(self) -> List[dict]:
        return list(filter(lambda x: x['min_type'] == 2, self.edges_dict))

    def get_small_nodes(self) -> List[dict]:
        return list(filter(lambda x: x['type'] == 0, self.nodes_dict))

    def get_medium_nodes(self) -> List[dict]:
        return list(filter(lambda x: x['type'] == 1, self.nodes_dict))

    def get_large_nodes(self) -> List[dict]:
        return list(filter(lambda x: x['type'] == 2, self.nodes_dict))


graph = Graph()

