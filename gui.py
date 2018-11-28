import sys
from PyQt5 import QtWidgets
import keytool

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()          #constructor for QWidget

        self.init_ui()

    def init_ui(self):
        #BUTTON DECLARATION
        #b1
        self.b1 = QtWidgets.QPushButton('Open left keystore')
        self.l1 = QtWidgets.QLabel()
        self.p1 = QtWidgets.QLineEdit('password')
        #b2
        self.b2 = QtWidgets.QPushButton('Open right keystore')
        self.l2 = QtWidgets.QLabel()
        self.p2 = QtWidgets.QLineEdit('password')
        #b3
        self.b3 = QtWidgets.QPushButton('Run')

        #VBOX LAYOUT
        v_box = QtWidgets.QVBoxLayout()
        #b1
        v_box.addWidget(self.b1)
        v_box.addWidget(self.p1)
        v_box.addWidget(self.l1)
        #b2
        v_box.addWidget(self.b2)
        v_box.addWidget(self.p2)
        v_box.addWidget(self.l2)
        #b3
        v_box.addWidget(self.b3)

        self.setLayout(v_box)                          #set layout to vbox
        self.setWindowTitle('KeyTool Manager')         #set title

        #SIGNALS & CONNECTIONS
        self.b1.clicked.connect(self.openFileDialog)   #signal = clicked, connecting it to btn_click
        self.b2.clicked.connect(self.openFileDialog)   #signal = clicked, connecting it to btn_click
        self.b3.clicked.connect(self.storeFileDialog)  # signal = clicked, connecting it to btn_click

        self.show()


    def openFileDialog(self):
        sender = self.sender()          #find button sending

        if sender.text() == 'Open left keystore':                                           #button name from sender
            filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")  #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"
            self.l1.setText(str(filename[0]))                                               #grab the first csv value, don't need the All files()* bit
            global leftLocation                                                             #declare global variable so can be used in other functions
            leftLocation = str(filename[0])                                                 #store left filename into global var

        if sender.text() == 'Open right keystore':                                          #button name from sender
            filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")  #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"
            self.l2.setText(str(filename[0]))                                               #grab the first csv value, dont need the All files()* bit
            global rightLocation                                                            #declare global variable so can be used in other functions
            rightLocation = str(filename[0])                                                #store right filename into global var

    def storeFileDialog(self):
        global ks1_location                               #define globally so functions can access variables
        ks1_location = leftLocation.replace('[', '').replace(']','').replace("'",'')        #remove ['']
        ks1_pass = self.p1.text()
        ks2_location = rightLocation.replace('[', '').replace(']','').replace("'",'')       #remove []
        ks2_pass = self.p2.text()
        print(ks1_location)
        print(ks2_location)
        print(ks1_pass)
        print(ks2_pass)


        ks1_list = keytool.cmd_command(ks1_location, ks1_pass)
        ks2_list = keytool.cmd_command(ks2_location, ks2_pass)

        buff1 = keytool.cmd_call_format(ks1_list, True, 'Left')
        buff2 = keytool.cmd_call_format(ks2_list, True, 'Right')
        buff2_nd = keytool.cmd_call_format(ks2_list, False, 'Right')                                #buff 2 for no dropped items, do not show print as it only for internal reference

        ds1 = keytool.remove_columns(buff1, True, 'Left')
        ds2 = keytool.remove_columns(buff2, True, 'Right')
        ds2_nd = keytool.remove_columns(buff2_nd, False, 'Right')  # set dropping duplicates to False, will also not be printed

        ds = keytool.merge_data_frames(ds1, ds2)

        keytool.generate_certs(ds, ds2_nd, ks1_location, ks1_pass, ks2_location, ks2_pass)



app = QtWidgets.QApplication(sys.argv)  #create application, required. pass in system variables
a_window = Window()                     #call class create object
sys.exit(app.exec())