from PyQt4 import QtGui, QtCore
import scipy.optimize as optimization
import math
import sys
from window import Window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # add menu
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')

        saveAction = QtGui.QAction('Save', self)
        saveAction.setStatusTip('Save')
        saveAction.triggered.connect(self.onSave)

        openAction = QtGui.QAction('Open', self)
        openAction.setStatusTip('Open')
        openAction.triggered.connect(self.load_csv)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()

        # main button
        self.addButton = QtGui.QPushButton('Add')
        self.addButton.clicked.connect(self.add_row)

        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.predictButton = QtGui.QPushButton("Predict")
        self.predictButton.clicked.connect(self.predict)

        self.resetButton = QtGui.QPushButton("Reset")
        self.resetButton.clicked.connect(self.reset)

        self.visualizeButton = QtGui.QPushButton("Visualize")
        self.visualizeButton.clicked.connect(self.visualize)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.predictButton)
        self.mainLayout.addWidget(self.resetButton)
        self.mainLayout.addWidget(self.visualizeButton)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def reset(self):
        for i in reversed(range(self.scrollLayout.count())):
            self.scrollLayout.itemAt(i).widget().setParent(None)

    def load_csv(self):
        self.reset()
        path = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open File')
        path = (str(path))
        df = pd.read_csv(path)

        for index, row in df.iterrows():
            form = DailyForm(time=str(row['time']), complete=str(row['complete']))
            self.scrollLayout.addWidget(form)

    def predict(self):
        x = []
        y = []

        initial_value = np.array([1.02, 1.46, 5.1])
        for i in range(self.scrollLayout.count()):
            widget = self.scrollLayout.itemAt(i)
            time = str(widget.widget().time.text())
            complete = str(widget.widget().complete.text())

            x.append(float(time))
            y.append(float(complete))

        errors = np.array([math.exp(-4) for i in x])
        result = optimization.curve_fit(func, x, y, initial_value, errors, method='lm')
        beta = result[0]

        form = ResultForm(alpha=str(beta[0]), beta=str(beta[1]), gamma=str(beta[2]))
        figure = plt.figure()
        result_window = Window(figure=figure, result_form=form)

        plt.plot(x, y, 'r.')
        plt.plot(x, [true_form(xx, beta) for xx in x], 'b')

        result_window.draw()
        result_window.exec_()

    def add_row(self):
        self.scrollLayout.addRow(DailyForm())

    def visualize(self):
        x = []
        y = []

        for i in range(self.scrollLayout.count()):
            widget = self.scrollLayout.itemAt(i)
            time = str(widget.widget().time.text())
            complete = str(widget.widget().complete.text())

            x.append(float(time))
            y.append(float(complete))

        plt.figure()
        plt.plot(x, y, 'r.')
        plt.show()

    def onSave(self):
        path = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Save File')

        times = []
        completes = []
        for i in range(self.scrollLayout.count()):
            widget = self.scrollLayout.itemAt(i)
            time = str(widget.widget().time.text())
            complete = str(widget.widget().complete.text())

            times.append(float(time))
            completes.append(float(complete))

        df = pd.DataFrame({'time': pd.Series(times), 'complete': pd.Series(completes)})
        df.to_csv(path)


def true_form(item, beta):
    return beta[0] * math.exp(-math.exp(beta[1] - beta[2] * item))


def func(x, a, b, c):
    return np.array([a * math.exp(-math.exp(b - c * xx)) for xx in x])


class DailyForm(QtGui.QWidget):
    def __init__(self, parent=None, time='', complete=''):
        super(DailyForm, self).__init__(parent)
        self.time_label = QtGui.QLabel()
        self.time_label.setText("time")
        self.time = QtGui.QLineEdit()
        self.time.setText(time)

        self.complete_label = QtGui.QLabel()
        self.complete_label.setText("complete")
        self.complete = QtGui.QLineEdit()
        self.complete.setText(complete)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.time)
        layout.addWidget(self.complete_label)
        layout.addWidget(self.complete)
        self.setLayout(layout)


class ResultForm(QtGui.QWidget):
    def __init__(self, parent=None, alpha='', beta='', gamma=''):
        super(ResultForm, self).__init__(parent)
        self.alpha = QtGui.QLabel()
        self.alpha.setText("Alpha")
        self.alpha_text = QtGui.QLineEdit()
        self.alpha_text.setText(alpha)

        self.beta = QtGui.QLabel()
        self.beta.setText("Beta")
        self.beta_text = QtGui.QLineEdit()
        self.beta_text.setText(beta)

        self.gamma = QtGui.QLabel()
        self.gamma.setText("Gamma")
        self.gamma_text = QtGui.QLineEdit()
        self.gamma_text.setText(gamma)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.alpha)
        layout.addWidget(self.alpha_text)
        layout.addWidget(self.beta)
        layout.addWidget(self.beta_text)
        layout.addWidget(self.gamma)
        layout.addWidget(self.gamma_text)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWidget = Main()
    myWidget.setWindowTitle(QtCore.QString("Calculator"))
    myWidget.resize(500, 600)
    myWidget.show()
    app.exec_()
