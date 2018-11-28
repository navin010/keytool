import sys
from PyQt5 import QtWidgets

'''
def window():
    app = QtWidgets.QApplication(sys.argv)            #passing in system arguments, arguments can be passed in to script via cmd, QApp required
    w = QtWidgets.QWidget()
    b = QtWidgets.QPushButton('Push Me')
    l = QtWidgets.QLabel('Look at me')
    #w.resize(300, 250)
    #w.move(300, 300)

    h_box = QtWidgets.QHBoxLayout()
    h_box.addStretch()
    h_box.addWidget(l)
    h_box.addStretch()

    v_box = QtWidgets.QVBoxLayout()
    v_box.addWidget(b)
    v_box.addLayout(h_box)

    w.setWindowTitle('Key Tool Manager')
    w.setLayout(v_box)
    w.show()
    sys.exit(app.exec_())

window()
'''

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()          #constructor for QWidget

        self.init_ui()

    def init_ui(self):
        self.b1 = QtWidgets.QPushButton('Open')
        self.l1 = QtWidgets.QLabel('Select left keystore')
        self.b2 = QtWidgets.QPushButton('Open')
        self.l2 = QtWidgets.QLabel('Select right keystore')


        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.b1)
        v_box.addWidget(self.l1)
        v_box.addWidget(self.b2)
        v_box.addWidget(self.l2)

        self.setLayout(v_box)
        self.setWindowTitle('KeyTool Manager')

        self.b1.clicked.connect(self.openFileDialog)   #signal = clicked, connecting it to btn_click
        #self.b2.clicked.connect(self.openFileDialog, 'l2')  # signal = clicked, connecting it to btn_click

        self.show()


    def openFileDialog(self, labelname):
        filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")  #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"
        self.l1.setText(str(filename[0]))    #grab the first csv value, dont need the All files()* bit
        print(str(filename[0]))


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec())