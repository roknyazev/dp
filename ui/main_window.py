from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ui.ui import Ui_Dialog
from ui.main_visualisation import *
from qt_material import QtStyleTools
import os

from ui.items import all_items


class MainWindow(QMainWindow, Ui_Dialog, QtStyleTools):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.setStyleSheet('background: #252525')

        label = QLabel()
        self.gridLayout.addWidget(label)

        shortest_paths_mode_checkbox = QCheckBox()
        shortest_paths_mode_checkbox.setText('K shortest paths')

        self.horizontalLayout.addWidget(shortest_paths_mode_checkbox)

        self.main_view = MainVisualization(1529,
                                           879,
                                           all_items,
                                           shortest_paths_mode_checkbox)
        self.main_view.create_native()
        self.main_view.native.setParent(label)

        self.startstopButton.clicked.connect(self.start_stop)

        self.pauseButton.clicked.connect(self.pause)
        self.pauseButton.setDisabled(True)
        self.stop_flag = False
        self.pause_flag = False

        # first_node_edit = QLineEdit()
        # second_node_edit = QLineEdit()
        # self.horizontalLayout.addWidget(first_node_edit)
        # self.horizontalLayout.addWidget(second_node_edit)

    def start_stop(self):
        self.start() if not self.stop_flag else self.stop()
        self.stop_flag = not self.stop_flag

    def start(self):
        self.startstopButton.setText('Stop')
        self.pauseButton.setEnabled(True)
        self.main_view.start(0)

    def stop(self):
        self.pauseButton.setStyleSheet(f"background-color: {os.environ['QTMATERIAL_SECONDARYDARKCOLOR']};")
        self.startstopButton.setText('Start')
        self.pauseButton.setDisabled(True)
        self.main_view.stop()

    def pause(self):
        self.pause_flag = not self.pause_flag
        self.main_view.pause(self.pause_flag)
        color = os.environ['QTMATERIAL_SECONDARYCOLOR'] if self.pause_flag \
            else os.environ['QTMATERIAL_SECONDARYDARKCOLOR']
        self.pauseButton.setStyleSheet(f"background-color: {color};")
