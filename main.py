import sys
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet
from ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
apply_stylesheet(app, theme='dark_amber.xml')
window.show()
app.exec_()
