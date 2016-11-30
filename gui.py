from PyQt4 import QtGui, QtCore
import sys
import predict
import json


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
        exitAction.triggered.connect(QtGui.qApp.quit)

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
        self.addButton.clicked.connect(self.addWidget)

        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def addWidget(self):
        self.scrollLayout.addRow(DailyForm())

    def onSave(self):
        name = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Save File')

        data = []
        for i in range(self.scrollLayout.count()):
            widget = self.scrollLayout.itemAt(i)
            time = str(widget.widget().time.text())
            complete = str(widget.widget().complete.text())
            predict = str(widget.widget().predictResult.text())
            data.append({'time': time, 'complete': complete, 'predict': predict})

        jsondata = json.dumps(data)
        f = open(name, "w")
        f.write(jsondata)
        f.close()


class DailyForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DailyForm, self).__init__(parent)
        self.time_label = QtGui.QLabel()
        self.time_label.setText("time")
        self.time = QtGui.QLineEdit()

        self.complete_label = QtGui.QLabel()
        self.complete_label.setText("complete")
        self.complete = QtGui.QLineEdit()

        self.buttonPredict = QtGui.QPushButton('Predict')
        self.buttonPredict.clicked.connect(self.click)
        self.predictResult = QtGui.QLineEdit()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.time)
        layout.addWidget(self.complete_label)
        layout.addWidget(self.complete)
        layout.addWidget(self.buttonPredict)
        layout.addWidget(self.predictResult)
        self.setLayout(layout)

    def click(self):
        time = float(self.time.text())
        complete = float(self.complete.text())
        result = predict.get_parameter(time, complete)
        print result
        self.predictResult.setText(str(result[0]))


app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.setWindowTitle(QtCore.QString("Calculator"))
myWidget.resize(500, 600)
myWidget.show()
app.exec_()
