import random

import pyqtgraph as pg
from PyQt5.QtCore import QTimer
import time
from ui.items import AbstractUpdatableItem
from typing import List
from vispy import app, scene, visuals
import numpy as np
from vispy.geometry.generation import create_sphere


class MainVisualization(scene.SceneCanvas):
    def __init__(self, width, height, items):
        scene.SceneCanvas.__init__(self, keys=None)

        self.size = width, height
        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=(90, 50, 10, 10),
                                               aspect=1.0)
        # self.view.camera.scale_factor = 50000
        # self.view.camera = 'turntable'
        self.items_classes = items
        self.items = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_view)

        self.call_counter = 0
        self.fps_cycle_start_time = 0
        self.fps_text = scene.visuals.Text('0 fps',
                                           color='w',
                                           anchor_x='left',
                                           parent=self.view,
                                           pos=(20, 30))

    def update_view(self):
        if self.call_counter == 0:
            self.fps_cycle_start_time = time.time()
        self.call_counter += 1

        for item in self.items:
            item.update()

        dt = time.time() - self.fps_cycle_start_time
        if dt > 0.2:
            self.fps_text.text = f'{round(self.call_counter / dt)} fps'
            #scene.visuals.Text.draw()
            self.call_counter = 0

    def start(self, dt=0):
        for item_class in self.items_classes:
            self.items.append(item_class(self.view.scene))
        self.timer.start(dt)

    def stop(self):
        self.timer.stop()
        for item in self.items:
            item.clear()
        self.fps_text.text = f'0 fps'

    def pause(self, pause_flag):
        self.timer.stop() if pause_flag else self.timer.start()
        self.fps_text.text = f'0 fps'

#
# class MainVisualizationOld(pg.GraphicsLayoutWidget):
#     def __init__(self, items: List[AbstractUpdatableItem]):
#         super().__init__()
#         self.plot = self.addPlot()
#         self.plot.setAspectLocked()
#         self.plot.showGrid(x=True, y=True, alpha=1)
#         self.plot.setTitle('0 fps')
#         self.plot.setRange(xRange=[-500, 500], yRange=[-500, 500])
#
#         self.items = items
#         for item in self.items:
#             self.plot.addItem(item.get_plot_item())
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update)
#
#         self.call_counter = 0
#         self.fps_cycle_start_time = 0
#
#     def update(self):
#         if self.call_counter == 0:
#             self.fps_cycle_start_time = time.time()
#         self.call_counter += 1
#
#         for item in self.items:
#             item.update()
#
#         dt = time.time() - self.fps_cycle_start_time
#         if dt > 0.2:
#             self.plot.setTitle(f'{round(self.call_counter / dt)} fps')
#             self.call_counter = 0
#
#     def start(self, dt=0):
#         for item in self.items:
#             item.reset_calls_to_zero()
#         self.timer.start(dt)
#
#     def stop(self):
#         self.timer.stop()
#         for item in self.items:
#             item.get_plot_item().setData()
#         self.plot.setTitle('0 fps')
#
#     def pause(self, pause_flag):
#         self.timer.stop() if pause_flag else self.timer.start()
#         self.plot.setTitle('0 fps')
