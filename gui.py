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
            self.filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")  #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"
            self.l1.setText(str(self.filename[0]))                                               #grab the first csv value, don't need the All files()* bit
            global leftLocation                                                             #declare global variable so can be used in other functions
            leftLocation = str(self.filename[0])                                                 #store left filename into global var

        if sender.text() == 'Open right keystore':                                          #button name from sender
            self.filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")  #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"
            self.l2.setText(str(self.filename[0]))                                               #grab the first csv value, dont need the All files()* bit
            global rightLocation                                                            #declare global variable so can be used in other functions
            rightLocation = str(self.filename[0])                                                #store right filename into global var

    def storeFileDialog(self):
        global ks1_location                               #define globally so functions can access variables
        self.ks1_location = leftLocation.replace('[', '').replace(']','').replace("'",'')        #remove ['']
        self.ks1_pass = self.p1.text()
        self.ks2_location = rightLocation.replace('[', '').replace(']','').replace("'",'')       #remove ['']
        self.ks2_pass = self.p2.text()
        print(self.ks1_location)
        print(self.ks2_location)
        print(self.ks1_pass)
        print(self.ks2_pass)

        # get cmd list commands for each key store
        self.ks1_list = keytool.cmd_command(self.ks1_location, self.ks1_pass)
        self.ks2_list = keytool.cmd_command(self.ks2_location, self.ks2_pass)
        # format lists and convert to csv files
        self.buff1 = keytool.cmd_call_format(self.ks1_list, True, 'Left')
        self.buff2 = keytool.cmd_call_format(self.ks2_list, True, 'Right')
        self.buff2_nd = keytool.cmd_call_format(self.ks2_list, False, 'Right')                        #buff 2 for no dropped items, do not show print as it only for internal reference
        # drop unnecessary columns and drop duplicates if required
        self.ds1 = keytool.remove_columns(self.buff1, True, 'Left')
        self.ds2 = keytool.remove_columns(self.buff2, True, 'Right')
        self.ds2_nd = keytool.remove_columns(self.buff2_nd, False, 'Right')                           #set dropping duplicates to False, will also not be printed
        # merge data frames together and filter unique values
        self.ds = keytool.merge_data_frames(self.ds1, self.ds2)
        # export and import the certificates, also do a unique alias check by looking against ds2_nd (non dropped duplicates)
        keytool.generate_certs(self.ds, self.ds2_nd, self.ks1_location, self.ks1_pass, self.ks2_location, self.ks2_pass)



app = QtWidgets.QApplication(sys.argv)  #create application, required. pass in system variables
a_window = Window()                     #call class create object
sys.exit(app.exec())