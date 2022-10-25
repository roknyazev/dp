from abc import abstractmethod

import numpy as np
import seaborn
from vispy import scene, visuals
from vispy.visuals.transforms import MatrixTransform

from graph.graph import graph
import config as cfg
from itertools import chain


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

        self.line_small = scene.visuals.Line
        self.line_small = self.line_small(parent=self.parent)
        self.line_small.set_gl_state("translucent", depth_test=False)

        self.line_medium = scene.visuals.Line
        self.line_medium = self.line_medium(parent=self.parent)
        self.line_medium.set_gl_state("translucent", depth_test=False)

        self.line_large = scene.visuals.Line
        self.line_large = self.line_large(parent=self.parent)
        self.line_large.set_gl_state("translucent", depth_test=False)

        self.scatter_small = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.scatter_small = self.scatter_small(parent=self.parent)
        self.scatter_small.set_gl_state("translucent", depth_test=False)

        self.scatter_medium = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.scatter_medium = self.scatter_medium(parent=self.parent)
        self.scatter_medium.set_gl_state("translucent", depth_test=False)

        self.scatter_large = scene.visuals.create_visual_node(visuals.MarkersVisual)
        self.scatter_large = self.scatter_large(parent=self.parent)
        self.scatter_large.set_gl_state("translucent", depth_test=False)
        self.line_palette = seaborn.color_palette('muted', 3)
        self.scatter_palette = seaborn.color_palette('pastel', 3)

    def clear(self):
        self.line_small.set_data(np.random.rand(0, 3))
        self.line_medium.set_data(np.random.rand(0, 3))
        self.line_large.set_data(np.random.rand(0, 3))
        self.scatter_small.set_data(np.random.rand(0, 3))
        self.scatter_medium.set_data(np.random.rand(0, 3))
        self.scatter_large.set_data(np.random.rand(0, 3))

    def update(self):
        if self.calls == 0:
            self.calls += 1

            line_small_coords = []
            for node1_coord, node2_coord, distance in graph.edges_coords(graph.get_small_edges()).values():
                line_small_coords.append(list(node1_coord) + [-10])
                line_small_coords.append(list(node2_coord) + [-10])
            self.line_small.set_data(pos=np.array(line_small_coords),
                                     connect='segments',
                                     color=list(self.line_palette[0]) + [0.1],
                                     width=1)

            line_medium_coords = []
            for node1_coord, node2_coord, distance in graph.edges_coords(graph.get_medium_edges()).values():
                line_medium_coords.append(list(node1_coord) + [-10])
                line_medium_coords.append(list(node2_coord) + [-10])
            self.line_medium.set_data(pos=np.array(line_medium_coords),
                                      connect='segments',
                                      color=list(self.line_palette[1]) + [0.1],
                                      width=2)

            line_large_coords = []
            for node1_coord, node2_coord, distance in graph.edges_coords(graph.get_large_edges()).values():
                line_large_coords.append(list(node1_coord) + [-10])
                line_large_coords.append(list(node2_coord) + [-10])
            self.line_large.set_data(pos=np.array(line_large_coords),
                                     connect='segments',
                                     color=list(self.line_palette[2]) + [0.1],
                                     width=4)

            node_small_coords = []
            for node in graph.get_small_nodes().values():
                node_small_coords.append((node['x'], node['y'], -10))
            self.scatter_small.set_data(pos=np.array(node_small_coords),
                                        symbol='o',
                                        face_color=list(self.scatter_palette[0]) + [1.],
                                        edge_color=list(self.scatter_palette[0]) + [1.],
                                        size=1)

            node_medium_coords = []
            for node in graph.get_medium_nodes().values():
                node_medium_coords.append((node['x'], node['y'], -10))
            self.scatter_medium.set_data(pos=np.array(node_medium_coords),
                                         symbol='o',
                                         face_color=list(self.scatter_palette[1]) + [1.],
                                         edge_color=list(self.scatter_palette[1]) + [1.],
                                         size=2)

            node_large_coords = []
            for node in graph.get_large_nodes().values():
                node_large_coords.append((node['x'], node['y'], -10))
            self.scatter_large.set_data(pos=np.array(node_large_coords),
                                        symbol='o',
                                        face_color=list(self.scatter_palette[2]) + [1.],
                                        edge_color=list(self.scatter_palette[2]) + [1.],
                                        size=4)

    def reset_calls_to_zero(self):
        self.calls = 0


class Graph3dItem(GraphItem):
    def __init__(self, parent):
        super().__init__(parent)

        self.layers_count = 15

        self.line_small.parent = None
        self.line_small = scene.visuals.Arrow
        self.line_small = self.line_small(parent=self.parent)
        self.line_small.set_gl_state("translucent", depth_test=False)

        self.line_medium.parent = None
        self.line_medium = scene.visuals.Arrow
        self.line_medium = self.line_medium(parent=self.parent)
        self.line_medium.set_gl_state("translucent", depth_test=False)

        self.line_large.parent = None
        self.line_large = scene.visuals.Arrow
        self.line_large = self.line_large(parent=self.parent)
        self.line_large.set_gl_state("translucent", depth_test=False)

        self.v_line_small = scene.visuals.Line
        self.v_line_small = self.v_line_small(parent=self.parent)
        self.v_line_small.set_gl_state("translucent", depth_test=False)

        self.v_line_medium = scene.visuals.Line
        self.v_line_medium = self.v_line_medium(parent=self.parent)
        self.v_line_medium.set_gl_state("translucent", depth_test=False)

        self.v_line_large = scene.visuals.Line
        self.v_line_large = self.v_line_large(parent=self.parent)
        self.v_line_large.set_gl_state("translucent", depth_test=False)

        self.max_height = self.layers_count * cfg.period_small

    def calc_layer(self, period_index: int):
        line_small_coords = []

        for node1_coord, node2_coord, distance in graph.edges_coords(graph.get_small_edges()).values():
            start_height = period_index * cfg.period_small
            end_height = start_height + distance / cfg.vel_small
            line_small_coords.append(list(node1_coord) + [start_height])
            line_small_coords.append(list(node2_coord) + [end_height])

            line_small_coords.append(list(node1_coord) + [end_height])
            line_small_coords.append(list(node2_coord) + [start_height])

        line_medium_coords = []
        for node1_coord, node2_coord, distance in graph.edges_coords(graph.get_medium_edges()).values():
            start_height = period_index * cfg.period_medium
            end_height = start_height + distance / cfg.vel_medium
            if start_height < self.max_height:
                line_medium_coords.append(list(node1_coord) + [start_height])
                line_medium_coords.append(list(node2_coord) + [end_height])

                line_medium_coords.append(list(node1_coord) + [end_height])
                line_medium_coords.append(list(node2_coord) + [start_height])

        line_large_coords = []
        for node1_coord, node2_coord, distance in graph.edges_coords(graph.get_large_edges()).values():
            start_height = period_index * cfg.period_large
            end_height = start_height + distance / cfg.vel_large
            if start_height < self.max_height:
                line_large_coords.append(list(node1_coord) + [start_height])
                line_large_coords.append(list(node2_coord) + [end_height])

                line_large_coords.append(list(node1_coord) + [end_height])
                line_large_coords.append(list(node2_coord) + [start_height])

        node_small_coords = []
        for node in graph.get_small_nodes().values():
            height = period_index * cfg.period_small
            if height < self.max_height:
                node_small_coords.append((node['x'], node['y'], height))

        node_medium_coords = []
        for node in graph.get_medium_nodes().values():
            height = period_index * cfg.period_medium
            if height < self.max_height:
                node_medium_coords.append((node['x'], node['y'], height))

        node_large_coords = []
        for node in graph.get_large_nodes().values():
            height = period_index * cfg.period_large
            if height < self.max_height:
                node_large_coords.append((node['x'], node['y'], height))
        return [line_small_coords, line_medium_coords, line_large_coords,
                node_small_coords, node_medium_coords, node_large_coords]

    def update(self):
        if self.calls == 0:
            self.calls += 1
            line_small_coords = []
            line_medium_coords = []
            line_large_coords = []
            node_small_coords = []
            node_medium_coords = []
            node_large_coords = []
            for i in range(self.layers_count):
                layer = self.calc_layer(i)
                line_small_coords.append(layer[0])
                line_medium_coords.append(layer[1])
                line_large_coords.append(layer[2])
                node_small_coords.append(layer[3])
                node_medium_coords.append(layer[4])
                node_large_coords.append(layer[5])
            line_small_coords = list(chain(*line_small_coords))
            line_medium_coords = list(chain(*line_medium_coords))
            line_large_coords = list(chain(*line_large_coords))
            node_small_coords = list(chain(*node_small_coords))
            node_medium_coords = list(chain(*node_medium_coords))
            node_large_coords = list(chain(*node_large_coords))
            self.line_small.set_data(pos=np.array(line_small_coords),
                                     connect='segments',
                                     color=list(self.line_palette[0]) + [1],
                                     width=1)
            self.line_medium.set_data(pos=np.array(line_medium_coords),
                                      connect='segments',
                                      color=list(self.line_palette[1]) + [1],
                                      width=1)
            self.line_large.set_data(pos=np.array(line_large_coords),
                                     connect='segments',
                                     color=list(self.line_palette[2]) + [1],
                                     width=1)
            self.scatter_small.set_data(pos=np.array(node_small_coords),
                                        symbol='o',
                                        face_color=list(self.scatter_palette[0]) + [1.],
                                        edge_color=list(self.scatter_palette[0]) + [1.],
                                        size=1)
            self.scatter_medium.set_data(pos=np.array(node_medium_coords),
                                         symbol='o',
                                         face_color=list(self.scatter_palette[1]) + [1.],
                                         edge_color=list(self.scatter_palette[1]) + [1.],
                                         size=1)
            self.scatter_large.set_data(pos=np.array(node_large_coords),
                                        symbol='o',
                                        face_color=list(self.scatter_palette[2]) + [1.],
                                        edge_color=list(self.scatter_palette[2]) + [1.],
                                        size=1)

            v_lines_points1 = self.calc_layer(0)[3:]
            v_lines_small_coords = []
            v_lines_medium_coords = []
            v_lines_large_coords = []
            for i in range(len(v_lines_points1[0])):
                point = list(v_lines_points1[0][i])
                v_lines_small_coords.append(point[:])
                point[2] = self.max_height
                v_lines_small_coords.append(point[:])

            for i in range(len(v_lines_points1[1])):
                point = list(v_lines_points1[1][i])
                v_lines_medium_coords.append(point[:])
                point[2] = self.max_height
                v_lines_medium_coords.append(point[:])

            for i in range(len(v_lines_points1[2])):
                point = list(v_lines_points1[2][i])
                v_lines_large_coords.append(point[:])
                point[2] = self.max_height
                v_lines_large_coords.append(point[:])
                # v_lines_large_coords.append(v_lines_points1[2][i])
                # v_lines_large_coords.append(v_lines_points2[2][i])

            self.v_line_small.set_data(pos=np.array(v_lines_small_coords),
                                       connect='segments',
                                       color=list(self.line_palette[0]) + [0.4],
                                       width=1)
            self.v_line_medium.set_data(pos=np.array(v_lines_medium_coords),
                                        connect='segments',
                                        color=list(self.line_palette[1]) + [0.4],
                                        width=1)
            self.v_line_large.set_data(pos=np.array(v_lines_large_coords),
                                       connect='segments',
                                       color=list(self.line_palette[2]) + [0.4],
                                       width=1)

    def clear(self):
        super().clear()
        self.v_line_small.set_data(np.random.rand(0, 3))
        self.v_line_medium.set_data(np.random.rand(0, 3))
        self.v_line_large.set_data(np.random.rand(0, 3))

    def reset_calls_to_zero(self):
        super().reset_calls_to_zero()


all_items = [ScatterLargeUAV, ScatterMediumUAV, ScatterSmallUAV, Graph3dItem, GraphItem]
