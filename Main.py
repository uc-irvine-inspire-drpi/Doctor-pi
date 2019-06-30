import sys
import os

from twilio.rest import Client
import pyimgur
import pyscreenshot as ImageGrab

import  PIL
from PIL import Image
import time
#import pillow
import configparser



from PyQt5 import QtWidgets, QtGui


from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
config = configparser.ConfigParser()
config.read('auth.ini')
#client_id = config.get('credentials', 'account')
#client_secret = config.get('credentials', 'token')
#client_id_2 = config.get('credentials', 'account2')


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()


        self.initWindow()


    #GUI
    def initWindow(self):

        # Object of GUI
        self.label = QtWidgets.QLabel("Press Image Capture and type in your cell phone number and then press ENTER")
        self.button = QtWidgets.QPushButton("ENTER")
        self.button2 = QtWidgets.QPushButton("Image Capture")
        self.textbox = QLineEdit(self)



        # astethics of GUI
        vBox = QtWidgets.QVBoxLayout()
        vBox.addWidget(self.label)
        vBox.addWidget(self.textbox)
        vBox.addWidget(self.button)
        vBox.addWidget(self.button2)
        self.setLayout(vBox)

        #actions
        self.button.setEnabled(False)
        self.textbox.textChanged.connect(self.disableButton)

        self.button.clicked.connect(self.uploaded_file)
        self.button.clicked.connect(self.buttonClicked)
       #self.button.setEnabled(True)
        #self.textbox.textChanged.connect(self.disableButton)

        #self.button.clicked.connect(self.errorButton2)
        self.button2.clicked.connect(self.minimize)
        self.button2.clicked.connect(self.screenGrab)

        # athethics/ gives window
        print(self.textbox)
        self.setWindowTitle("Healthy PI")
        self.show()


    def disableButton(self):
        if len(self.textbox.text()) > 0 and os.path.exists('/Users/benhaywood/Desktop/screenshot.png'):
            self.button.setEnabled(True)


    def uploaded_file(self):


        #Athentifcation
        account = os.environ.get('IMGUR_USER')

        path = '/Users/benhaywood/Desktop/screenshot.png'


        #image upload
        im = pyimgur.Imgur("475d5afd6088d17")
        uploaded_image = im.upload_image(path, title="test")



        #test if upload works only!
        #print(uploaded_image.title)  # Cat Ying & Yang
        #print(uploaded_image.link)  # http://imgur.com/S1jmapR.jpg


        return uploaded_image.link_huge_thumbnail





    def buttonClicked(self):

        #twilio login
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        number = self.textbox.text()



        message = client.messages.create(to= number, from_="+17076402887", media_url= self.uploaded_file())

    def screenGrab(self):

        # grab fullscreen
        im = ImageGrab.grab()


         # save image file
        im.save('/Users/benhaywood/Desktop/screenshot.png', 'PNG')


        # stores image in image.
       #self.image = '/Users/benhaywood/Desktop/screenshot.png'

    def minimize(self):
        self.showMinimized()


app = QtWidgets.QApplication(sys.argv)
ourWindow = Window()

sys.exit(app.exec())