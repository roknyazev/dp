import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from vispy import scene
from ui.items import AbstractUpdatableItem
from typing import List
import numpy as np
from graph.graph import graph
from logistics import k_shortest
from collections import deque

class MainVisualization(scene.SceneCanvas):
    def __init__(self, width, height, items, shortest_paths_mode_checkbox: QCheckBox):
        self.shortest_paths_mode_checkbox = shortest_paths_mode_checkbox

        scene.SceneCanvas.__init__(self, keys=None, vsync=True)

        self.size = width, height
        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.bgcolor = '#151515'

        self.view.camera = scene.PanZoomCamera(rect=(90, 50, 10, 10),
                                               aspect=1.0)
        # self.view.camera = scene.cameras.fly.FlyCamera(fov=60)
        # self.view.camera.center = 90, 50, 0

        self.items_classes = items
        self.items: List[AbstractUpdatableItem] = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_view)

        self.call_counter = 0
        self.fps_cycle_start_time = 0
        self.fps_text = scene.visuals.Text('0 fps',
                                           color='w',
                                           anchor_x='left',
                                           parent=self.view,
                                           pos=(20, 30))

        for item_class in self.items_classes:
            self.items.append(item_class(self.view.scene))

        self.node_pair = deque([1, 0], maxlen=2)
        self.parity_flag = False

    def update_view(self):
        if self.call_counter == 0:
            self.fps_cycle_start_time = time.time()
        self.call_counter += 1

        for item in self.items:
            item.update()

        dt = time.time() - self.fps_cycle_start_time
        if dt > 0.2:
            self.fps_text.text = f'{round(self.call_counter / dt)} fps'
            self.call_counter = 0

    def start(self, dt=0):
        for item in self.items:
            item.reset_calls_to_zero()
        self.timer.start(dt)

    def stop(self):
        self.timer.stop()
        for item in self.items:
            item.clear()
        self.fps_text.text = f'0 fps'

    def pause(self, pause_flag):
        self.timer.stop() if pause_flag else self.timer.start()
        self.fps_text.text = f'0 fps'

    def on_mouse_press(self, event):
        tr = self.scene.node_transform(self.view.scene)
        pos = tr.map(event.pos)
        nodes = graph.get_all_nodes()

        if self.shortest_paths_mode_checkbox.isChecked() and event.button == 2:
            closest = min(nodes.keys(), key=lambda key: sum((np.array([nodes[key]['x'], nodes[key]['y']]) -
                                                         np.array([pos[0], pos[1]])) ** 2))

            self.node_pair.append(closest)
            k_shortest.highlight_k_shortest(*list(self.node_pair))


