import pyqtgraph as pg
from PyQt5.QtCore import QTimer
import time
from ui.items import AbstractUpdatableItem
from typing import List


class MainVisualization(pg.GraphicsLayoutWidget):
    def __init__(self, items: List[AbstractUpdatableItem]):
        super().__init__()
        self.plot = self.addPlot()
        self.plot.setAspectLocked()
        self.plot.showGrid(x=True, y=True, alpha=1)
        self.plot.setTitle('0 fps')
        self.plot.setRange(xRange=[-500, 500], yRange=[-500, 500])

        self.items = items
        for item in self.items:
            self.plot.addItem(item.get_plot_item())

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.call_counter = 0
        self.fps_cycle_start_time = 0

    def update(self):
        if self.call_counter == 0:
            self.fps_cycle_start_time = time.time()
        self.call_counter += 1

        for item in self.items:
            item.update()

        dt = time.time() - self.fps_cycle_start_time
        if dt > 0.2:
            self.plot.setTitle(f'{round(self.call_counter / dt)} fps')
            self.call_counter = 0

    def start(self, dt=0):
        for item in self.items:
            item.reset_calls_to_zero()
        self.timer.start(dt)

    def stop(self):
        self.timer.stop()
        for item in self.items:
            item.get_plot_item().setData()
        self.plot.setTitle('0 fps')

    def pause(self, pause_flag):
        self.timer.stop() if pause_flag else self.timer.start()
        self.plot.setTitle('0 fps')

