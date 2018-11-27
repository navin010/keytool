import sys
from PyQt5 import QtWidgets

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
