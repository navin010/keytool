import sys
import os
from PyQt5 import QtWidgets, QtGui
import keytool
import logging
from io import StringIO
import datetime as dt

#Start log
logging.basicConfig(filename='logfile.log',level=logging.DEBUG)

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()                                                                  #constructor for QWidget

        self.init_ui()

    def init_ui(self):
        #BUTTON DECLARATION
        self.j1 = QtWidgets.QPushButton('Open JRE bin location')
        self.j2 = QtWidgets.QLabel()
        #b1
        self.b1 = QtWidgets.QPushButton('Open left keystore')
        self.l1 = QtWidgets.QLabel()
        self.p1 = QtWidgets.QLineEdit('password')
        #b2
        self.b2 = QtWidgets.QPushButton('Open right keystore')
        self.l2 = QtWidgets.QLabel()
        self.p2 = QtWidgets.QLineEdit('password')
        #b3
        self.b3 = QtWidgets.QPushButton('Compare')
        self.l4 = QtWidgets.QLabel()
        self.b4 = QtWidgets.QPushButton('Transfer')
        self.l3 = QtWidgets.QLabel()

        #Left Right box join
        v_box_left = QtWidgets.QVBoxLayout()
        v_box_left.addWidget(self.b1)
        v_box_left.addWidget(self.p1)
        v_box_left.addWidget(self.l1)
        v_box_right = QtWidgets.QVBoxLayout()
        v_box_right.addWidget(self.b2)
        v_box_right.addWidget(self.p2)
        v_box_right.addWidget(self.l2)
        h_box_lr = QtWidgets.QHBoxLayout()
        h_box_lr.addLayout(v_box_left)
        h_box_lr.addLayout(v_box_right)

        #LAYOUT
        v_box = QtWidgets.QVBoxLayout()
        #Left Right Boxes
        v_box.addLayout(h_box_lr)
        # j1
        v_box.addWidget(self.j1)
        v_box.addWidget(self.j2)
        #b3/4
        v_box.addWidget(self.b3)
        v_box.addWidget(self.l4)
        v_box.addWidget(self.b4)
        v_box.addWidget(self.l3)

        self.setLayout(v_box)                                                                   #set layout to vbox
        self.setWindowTitle('Key Tool Manager')                                                 #set title
        self.icon = QtGui.QIcon('key.png')                                                     #add icon
        self.setWindowIcon(self.icon)
        #self.setStyleSheet("background-color: lightGray;")

        #Colours
        self.j1.setStyleSheet("QWidget {background-color: black; color: white; border-style: solid; border-color: black; border-width: 5px; border-radius: 10px;}")
        self.j2.setStyleSheet("QWidget {color: black}")
        self.b1.setStyleSheet("QWidget {background-color: purple; color: white; border-style: solid; border-color: purple; border-width: 5px; border-radius: 10px;}")
        self.l1.setStyleSheet("QWidget {color: purple; }")
        self.p1.setStyleSheet("QWidget {color: black; font-size: 7.75pt; border-style: solid; border-color: purple; border-width: 1.5px; border-radius: 10px;}")
        self.b2.setStyleSheet("QWidget {background-color: darkblue; color: white; border-style: solid; border-color: darkblue; border-width: 5px; border-radius: 10px;}")
        self.l2.setStyleSheet("QWidget {color: darkblue}")
        self.p2.setStyleSheet("QWidget {color: black; font-size: 7.75pt; border-style: solid; border-color: darkblue; border-width: 1.5px; border-radius: 10px;}")
        self.b3.setStyleSheet("QWidget {background-color: green; color: white; border-style: solid; border-color: green; border-width: 7px; border-radius: 10px;}")
        self.b4.setStyleSheet("QWidget {background-color: darkred; color: white; border-style: solid; border-color: darkred; border-width: 7px; border-radius: 10px;}")
        self.l3.setStyleSheet("QWidget {color: red}")

        #SIGNALS & CONNECTIONS
        self.j1.clicked.connect(self.openFileDir)                                               #signal = clicked, connecting it to openFileDir
        self.b1.clicked.connect(self.openFileDialog)                                            #signal = clicked, connecting it to openFileDialog
        self.b2.clicked.connect(self.openFileDialog)                                            #signal = clicked, connecting it to openFileDialog
        self.b3.clicked.connect(self.storeFileDialog)                                           #signal = clicked, connecting it to storeFileDialog
        self.b4.clicked.connect(self.transferCerts)                                             #signal = clicked, connecting it to transferCerts

        self.show()


    def openFileDir(self):
        self.jre = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.j2.setText(self.jre)
        global java_path
        java_path = self.jre

    def openFileDialog(self):
        sender = self.sender()                                                                      #find button sending

        if sender.text() == 'Open left keystore':                                                   #button name from sender
            self.filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")     #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"                             #
            global leftLocation                                                                     #declare global variable so can be used in other functions
            leftLocation = str(self.filename[0]).replace('[', '').replace(']','').replace("'",'')   #grab the first csv value, don't need the All files()* bit, store left filename into global var, remove ['']
            self.l1.setText(leftLocation)

        if sender.text() == 'Open right keystore':                                                  #button name from sender
            self.filename = QtWidgets.QFileDialog.getOpenFileNames(self, "Open a file", "C://")     #self, window name, directory start path, .jks file extension filter e.g. "JKS File (*.jks)"                             #
            global rightLocation                                                                    #declare global variable so can be used in other functions
            rightLocation = str(self.filename[0]).replace('[', '').replace(']','').replace("'",'')  #grab the first csv value, dont need the All files()* bit, store right filename into global var, remove ['']
            self.l2.setText(rightLocation)

    def storeFileDialog(self):
        if self.l1.text() == '' or self.l2.text() == '' or  self.p1.text()=='' or self.p2.text()=='' or self.j2.text()=='':          #check if required values are there
            self.l3.setText('Please enter values for all fields')
        else:
            self.thread = "[Start]"
            print(self.thread)
            logging.debug(self.thread + str(dt.datetime.now()))

            global ks1_location                                                                     #define globally so functions can access variables
            self.ks1_location = leftLocation
            self.ks1_pass = self.p1.text()
            self.ks2_location = rightLocation
            self.ks2_pass = self.p2.text()
            print(self.ks1_location)
            print(self.ks2_location)
            print(self.ks1_pass)
            print(self.ks2_pass)

            # Changed to JRE directory
            os.chdir(java_path)
            print(java_path)

            # get cmd list commands for each key store
            self.ks1_list = keytool.cmd_command(self.ks1_location, self.ks1_pass, 'Left')
            self.ks2_list = keytool.cmd_command(self.ks2_location, self.ks2_pass, 'Right')

            # format lists and convert to csv files
            try:
                self.buff1 = keytool.cmd_call_format(self.ks1_list, True, 'Left')
                self.buff2 = keytool.cmd_call_format(self.ks2_list, True, 'Right')
                self.buff2_nd = keytool.cmd_call_format(self.ks2_list, False, 'Right')                      #buff 2 for no dropped items, do not show print as it only for internal reference
            except Exception as e:
                self.thread = '[Exception CMD Format]' + str(e)
                logging.debug(self.thread)
                print(self.thread)
                self.l3.setText(self.thread)
            else:

                # drop unnecessary columns and drop duplicates if required
                try:
                    self.ds1 = keytool.remove_columns(self.buff1, True, 'Left')
                    self.ds2 = keytool.remove_columns(self.buff2, True, 'Right')
                    self.ds2_nd = keytool.remove_columns(self.buff2_nd, False, 'Right')                         #set dropping duplicates to False, will also not be printed
                except Exception as e:
                    self.thread = '[Exception Pandas Format]' + str(e)
                    logging.debug(self.thread)
                    print(self.thread)
                    self.l3.setText(self.thread)
                else:

                    # merge data frames together and filter unique values
                    try:
                        self.ds_string = keytool.merge_data_frames(self.ds1, self.ds2)
                        self.ds = StringIO(self.ds_string)
                    except Exception as e:
                        self.thread = '[Exception Pandas Merge]' + str(e)
                        logging.debug(self.thread)
                        print(self.thread)
                        self.l3.setText(self.thread)
                    else:
                        self.l3.setText('')  # reset dialog box when done
                        self.l4.setText(self.ds_string)

    def transferCerts(self):
        try:
            # export and import the certificates, also do a unique alias check by looking against ds2_nd (non dropped duplicates)
            keytool.generate_certs(self.ds, self.ds2_nd, self.ks1_location, self.ks1_pass, self.ks2_location, self.ks2_pass)
        except Exception as e:
            self.thread = '[Exception Certificate Import Export]' + str(e)
            logging.debug(self.thread)
            print(self.thread)
            self.l3.setText(self.thread)
        else:
            self.thread = "[Complete]"
            print(self.thread)
            logging.debug(self.thread + str(dt.datetime.now()))
            self.l3.setText('')  # reset dialog box when done
            self.l4.setText('')


app = QtWidgets.QApplication(sys.argv)                                                              #create application, required. pass in system variables
a_window = Window()                                                                                 #call class create object
sys.exit(app.exec())