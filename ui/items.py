import pyqtgraph as pg
from abc import abstractmethod
from graph.graph import graph
import numpy as np
from vispy import scene, visuals
from vispy.visuals.transforms import MatrixTransform
import networkx as nx
from vispy.visuals.graphs import layouts
from vispy.visuals.line.line import LineVisual
import seaborn


# 'disc', 'arrow', 'ring', 'clobber', 'square', 'diamond', 'vbar', 'hbar',
# 'cross', 'tailed_arrow', 'x', 'triangle_up', 'triangle_down', 'star',
# 'o', '+', '++', 's', '-', '|', '->', '>', '^', 'v', '*'

class AbstractUpdatableItem:
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def reset_calls_to_zero(self):
        pass


class ScatterSmallUAV(AbstractUpdatableItem):
    def __init__(self, parent):
        scatter = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.plot_item = scatter(parent=parent)
        self.plot_item.set_gl_state("translucent", blend=True, depth_test=True)
        self.plot_item.transform = MatrixTransform()

    def clear(self):
        self.plot_item.set_data(np.random.rand(0, 2))

    def update(self):
        n = 10000
        pos = np.random.rand(n, 2)
        self.plot_item.set_data(pos, symbol="o", size=15, face_color='blue')

    def reset_calls_to_zero(self):
        pass


class ScatterMediumUAV(AbstractUpdatableItem):
    def __init__(self, parent):
        scatter = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.plot_item = scatter(parent=parent)
        self.plot_item.set_gl_state("translucent", blend=True, depth_test=True)

    def clear(self):
        self.plot_item.set_data(np.random.rand(0, 2))

    def update(self):
        n = 10000
        pos = np.random.rand(n, 2)
        self.plot_item.set_data(pos, symbol="o", size=10, face_color='red')

    def reset_calls_to_zero(self):
        pass


class ScatterLargeUAV(AbstractUpdatableItem):
    def __init__(self, parent):
        scatter = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.plot_item = scatter(parent=parent)
        self.plot_item.set_gl_state("translucent", blend=True, depth_test=True)

    def update(self):
        n = 10000
        pos = np.random.rand(n, 2)
        self.plot_item.set_data(pos, symbol="o", size=15, face_color='green')

    def clear(self):
        self.plot_item.set_data(np.random.rand(0, 2))

    def reset_calls_to_zero(self):
        pass


class GraphItem(AbstractUpdatableItem):
    def __init__(self, parent):
        self.parent = parent
        self.calls = 0
        scatter = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.plot_item = scatter(parent=parent)

        self.line_small = None
        self.line_medium = None
        self.line_large = None
        self.scatter_small = None
        self.scatter_medium = None
        self.scatter_large = None

    def clear(self):
        self.line_small.set_data(np.random.rand(0, 2))
        self.line_medium.set_data(np.random.rand(0, 2))
        self.line_large.set_data(np.random.rand(0, 2))
        self.scatter_small.set_data(np.random.rand(0, 2))
        self.scatter_medium.set_data(np.random.rand(0, 2))
        self.scatter_large.set_data(np.random.rand(0, 2))

    def update(self):
        if self.calls == 0:
            self.calls += 1

            line_palette = seaborn.color_palette('muted', 3)
            scatter_palette = seaborn.color_palette('pastel', 3)

            line_small_coords = []
            for coord in graph.edges_coords(graph.get_small_edges()).values():
                line_small_coords.append(list(coord[0]) + [-100])
                line_small_coords.append(list(coord[1]) + [-100])
            self.line_small = scene.visuals.Line
            self.line_small = self.line_small(parent=self.parent)
            self.line_small.set_gl_state("translucent", depth_test=False)
            self.line_small.set_data(pos=np.array(line_small_coords),
                                     connect='segments',
                                     color=list(line_palette[0]) + [0.1],
                                     width=1)

            line_medium_coords = []
            for coord in graph.edges_coords(graph.get_medium_edges()).values():
                line_medium_coords.append(list(coord[0]) + [-100])
                line_medium_coords.append(list(coord[1]) + [-100])
            self.line_medium = scene.visuals.Line
            self.line_medium = self.line_medium(parent=self.parent)
            self.line_medium.set_gl_state("translucent", depth_test=False)
            self.line_medium.set_data(pos=np.array(line_medium_coords),
                                      connect='segments',
                                      color=list(line_palette[1]) + [0.1],
                                      width=2)

            line_large_coords = []
            for coord in graph.edges_coords(graph.get_large_edges()).values():
                line_large_coords.append(list(coord[0]) + [-100])
                line_large_coords.append(list(coord[1]) + [-100])
            self.line_large = scene.visuals.Line
            self.line_large = self.line_large(parent=self.parent)
            self.line_large.set_gl_state("translucent", depth_test=False)
            self.line_large.set_data(pos=np.array(line_large_coords),
                                     connect='segments',
                                     color=list(line_palette[2]) + [0.1],
                                     width=4)

            node_small_coords = []
            for node in graph.get_small_nodes().values():
                node_small_coords.append((node['x'], node['y'], 100))
            self.scatter_small = scene.visuals.create_visual_node(visuals.MarkersVisual)
            self.scatter_small = self.scatter_small(parent=self.parent)

            self.scatter_small.set_gl_state("translucent", depth_test=False)

            self.scatter_small.set_data(pos=np.array(node_small_coords),
                                        symbol='o',
                                        face_color=list(scatter_palette[0]) + [1.],
                                        edge_color=list(scatter_palette[0]) + [1.],
                                        size=1)

            node_medium_coords = []
            for node in graph.get_medium_nodes().values():
                node_medium_coords.append((node['x'], node['y'], 100))
            self.scatter_medium = scene.visuals.create_visual_node(visuals.MarkersVisual)
            self.scatter_medium = self.scatter_medium(parent=self.parent)

            self.scatter_medium.set_gl_state("translucent", depth_test=False)

            self.scatter_medium.set_data(pos=np.array(node_medium_coords),
                                         symbol='o',
                                         face_color=list(scatter_palette[1]) + [1.],
                                         edge_color=list(scatter_palette[1]) + [1.],
                                         size=2)

            node_large_coords = []
            for node in graph.get_large_nodes().values():
                node_large_coords.append((node['x'], node['y'], 100))
            self.scatter_large = scene.visuals.create_visual_node(visuals.MarkersVisual)

            self.scatter_large = self.scatter_large(parent=self.parent)
            self.scatter_large.set_gl_state("translucent", depth_test=False)

            self.scatter_large.set_data(pos=np.array(node_large_coords),
                                        symbol='o',
                                        face_color=list(scatter_palette[2]) + [1.],
                                        edge_color=list(scatter_palette[2]) + [1.],
                                        size=4)

    def reset_calls_to_zero(self):
        self.calls = 0


all_items = [ScatterLargeUAV, ScatterMediumUAV, ScatterSmallUAV, GraphItem, GraphItem]
