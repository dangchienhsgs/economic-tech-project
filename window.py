from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class Window(QtGui.QDialog):
    def __init__(self, parent=None, figure=None, result_form=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = figure

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.form = result_form

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.form)
        self.setLayout(layout)

    def draw(self):
        self.canvas.draw()
