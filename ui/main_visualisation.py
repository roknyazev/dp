import time

from PyQt5.QtCore import QTimer
from vispy import scene
from ui.items import AbstractUpdatableItem
from typing import List


class MainVisualization(scene.SceneCanvas):
    def __init__(self, width, height, items):
        scene.SceneCanvas.__init__(self, keys=None, vsync=True)

        self.size = width, height
        self.unfreeze()
        self.view = self.central_widget.add_view()
        # self.view.camera = scene.PanZoomCamera(rect=(90, 50, 10, 10),
        #                                        aspect=1.0)
        self.view.camera = scene.cameras.fly.FlyCamera(fov=60)
        self.view.camera.center = 90, 50, 0

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
