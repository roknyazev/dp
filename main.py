import sys
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet
from ui.main_window import MainWindow

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
apply_stylesheet(app, theme='dark_amber.xml')
window.showMaximized()
app.exec_()
