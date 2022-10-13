import pyqtgraph as pg
import random
from abc import abstractmethod
from graph.graph import graph
import numpy as np
from pyqtgraph.Qt import QtGui


def custom_symbol(symbol: str, font: QtGui.QFont = QtGui.QFont("San Serif")) -> QtGui.QPainterPath:
    """Create custom symbol with font"""
    # We just want one character here, comment out otherwise
    assert len(symbol) == 1
    pg_symbol = QtGui.QPainterPath()
    pg_symbol.addText(0, 0, font, symbol)
    # Scale symbol
    br = pg_symbol.boundingRect()
    scale = min(1. / br.width(), 1. / br.height())
    tr = QtGui.QTransform()
    tr.scale(scale, scale)
    tr.translate(-br.x() - br.width() / 2., -br.y() - br.height() / 2.)
    return tr.map(pg_symbol)


class AbstractUpdatableItem:
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_plot_item(self):
        pass

    @abstractmethod
    def reset_calls_to_zero(self):
        pass


class ScatterSmallUAV(AbstractUpdatableItem):
    def __init__(self):
        self.plot_item = pg.ScatterPlotItem(size=15, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 255, 120))
        self.plot_item.opts["useCache"] = True
        self.calls = 0
        self.symbol = None

    def rotate(self, symbol, angle):
        transform = QtGui.QTransform()
        transform.rotate(angle)
        return transform.map(symbol)

    def get_plot_item(self):
        return self.plot_item

    def update(self):
        if self.calls == 0:
            self.calls = 1
            self.symbol = custom_symbol('➤')
        positions = ([random.normalvariate(0, 10) for _ in range(500)],
                     [random.normalvariate(0, 10) for _ in range(500)])
        positions = list(zip(*positions))
        angles = [random.randint(0, 360) for _ in range(500)]
        symbols = list(map(lambda x: self.rotate(self.symbol, x), angles))
        data = [{'pos': pos, 'symbol': symbol} for pos, symbol in zip(positions, symbols)]
        self.plot_item.setData(data)

    def reset_calls_to_zero(self):
        pass


class ScatterMediumUAV(AbstractUpdatableItem):
    def __init__(self):
        self.plot_item = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 255, 120))
        self.plot_item.opts["useCache"] = True

    def get_plot_item(self):
        return self.plot_item

    def update(self):
        self.plot_item.setData([random.normalvariate(0, 10) for _ in range(500)],
                               [random.normalvariate(0, 10) for _ in range(500)])

    def reset_calls_to_zero(self):
        pass


class ScatterLargeUAV(AbstractUpdatableItem):
    def __init__(self):
        self.plot_item = pg.ScatterPlotItem(size=15, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 0, 120))
        self.plot_item.opts["useCache"] = True

    def get_plot_item(self):
        return self.plot_item

    def update(self):
        self.plot_item.setData([random.normalvariate(0, 10) for _ in range(500)],
                               [random.normalvariate(0, 10) for _ in range(500)])

    def reset_calls_to_zero(self):
        pass


class GraphItem(AbstractUpdatableItem):
    def __init__(self):
        self.plot_item = pg.GraphItem()
        self.calls = 0
        self.node_pens = {0: pg.mkPen(pg.mkColor(255, 255, 0, 255), width=1),
                          1: pg.mkPen(pg.mkColor(255, 0, 255, 255), width=2),
                          2: pg.mkPen(pg.mkColor(0, 255, 255, 255), width=3)}
        self.edge_pens = {0: (255, 255, 0, 70, 1),
                          1: (255, 0, 255, 70, 2),
                          2: (0, 255, 255, 70, 5)}
        self.dtype = [('red', np.ubyte), ('green', np.ubyte), ('blue', np.ubyte), ('alpha', np.ubyte), ('width', float)]

    def get_plot_item(self):
        return self.plot_item

    def update(self):
        if self.calls == 0:
            self.calls += 1
            nodes = graph.get_all_nodes()
            edges = graph.get_all_edges()
            nodes_pos = []
            nodes_style = []
            for node in nodes:
                nodes_pos.append((node['x'], node['y']))
                nodes_style.append(self.node_pens[node['type']])
            adj = []
            edges_style = []
            for edge in edges:
                adj.append((edge['node1'], edge['node2']))
                edges_style.append(self.edge_pens[edge['min_type']])

            self.plot_item.setData(pos=np.array(nodes_pos),
                                   adj=np.array(adj),
                                   pen=np.array(edges_style, dtype=self.dtype),
                                   symbolPen=nodes_style)

    def reset_calls_to_zero(self):
        self.calls = 0


# all_items = [ScatterLargeUAV(), ScatterMediumUAV(), ScatterSmallUAV()]
# all_items = [ScatterLargeNode(), ScatterMediumNode(), ScatterSmallNode()]
all_items = [ScatterLargeUAV(), ScatterMediumUAV(), ScatterSmallUAV(), GraphItem()]
