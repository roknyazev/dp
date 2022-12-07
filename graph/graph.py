import pandas as pd
import networkx as nx
from tqdm import tqdm
import config as cfg

# 4, 6
variant = 4


class Graph:
    def __init__(self):
        nodes_df = pd.read_csv(f'graph_data/variant{variant}/nodes.csv').dropna()
        edges_df = pd.read_csv(f'graph_data/variant{variant}/edges.csv').dropna()
        nodes_tuple = tuple(zip(range(len(nodes_df)),
                                nodes_df['type'],
                                nodes_df['x'],
                                nodes_df['y']))
        self.nodes_dict = [(x[0], dict(zip(['type',
                                            'x',
                                            'y'], x[1:]))) for x in nodes_tuple]
        self.nodes_dict = dict(self.nodes_dict)
        edges_tuple = tuple(zip(range(len(edges_df)),
                                edges_df['node1'],
                                edges_df['node2'],
                                edges_df['weight'],
                                edges_df['min_type']))
        self.edges_dict = [(x[0], dict(zip(['node1',
                                            'node2',
                                            'weight',
                                            'min_type'], x[1:]))) for x in edges_tuple]
        self.edges_dict = dict(self.edges_dict)

        self.graph = nx.Graph()
        for node in nodes_tuple:
            self.graph.add_node(node[0], type=node[1], pos=(node[2], node[3]))
        for edge in edges_tuple:
            self.graph.add_edge(edge[1], edge[2],
                                index=edge[0],
                                dist=edge[3],
                                type=edge[4])

    @staticmethod
    def calc_price(edge_type: int, dist: float, payload: float):
        return cfg.type_info[edge_type].km_price * dist * (payload // cfg.type_info[edge_type].capacity + 1)

    def get_all_edges(self) -> dict:
        return self.edges_dict

    def get_all_nodes(self) -> dict:
        return self.nodes_dict

    def get_small_edges(self) -> dict:
        return dict(filter(lambda x: x[1]['min_type'] == 0, self.edges_dict.items()))

    def get_medium_edges(self) -> dict:
        return dict(filter(lambda x: x[1]['min_type'] == 1, self.edges_dict.items()))

    def get_large_edges(self) -> dict:
        return dict(filter(lambda x: x[1]['min_type'] == 2, self.edges_dict.items()))

    def get_small_nodes(self) -> dict:
        return dict(filter(lambda x: x[1]['type'] == 0, self.nodes_dict.items()))

    def get_medium_nodes(self) -> dict:
        return dict(filter(lambda x: x[1]['type'] == 1, self.nodes_dict.items()))

    def get_large_nodes(self) -> dict:
        return dict(filter(lambda x: x[1]['type'] == 2, self.nodes_dict.items()))

    def edges_coords(self, edges_dict: dict) -> dict:
        result = {}
        for edge in edges_dict.items():
            node1 = edge[1]['node1']
            node2 = edge[1]['node2']
            coords = ((self.nodes_dict[node1]['x'], self.nodes_dict[node1]['y']),
                      (self.nodes_dict[node2]['x'], self.nodes_dict[node2]['y']),
                      edge[1]['weight'])
            result[edge[0]] = coords
        return result


graph = Graph()


class Graph3d:
    def __init__(self):
        self.graph2d = graph
