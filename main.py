import sys
import os 
from twilio.rest import Client

import pyimgur
import pyscreenshot as ImageGrab

import PIL
from PIL import Image
import time
#import pillow
#import configparser



from PyQt5 import QtWidgets, QtGui


from PyQt5.QtWidgets import QMainWindow, QLabel,QApplication,QWidget, QVBoxLayout, QPushButton, QAction, QLineEdit, QMessageBox


from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class MatchBoxLineEdit(QLineEdit):
    def focusInEvent(self, e):
        try:
            subprocess.Popen(["matchbox-keyboard"])
        except FileNotFoundError:
            pass

    def focusOutEvent(self,e):
        subprocess.Popen(["killall","matchbox-keyboard"])



#-------------------------------------------------------------------------------        
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
        self.textbox = QtWidgets.QTextEdit()

        #textbox validation
        self.textbox = QLineEdit()
        self.textbox.setInputMask('99999999999')

        #keyboard popup
        widget = QWidget()
        lay = QVBoxLayout(widget)
        #self.setCentralWidget(widget)
        self.userNameLabel = QLabel("What is your name?")
        self.nameInput = MatchBoxLineEdit()
        lay.addWidget(self.nameInput)

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
        self.button2.clicked.connect(MatchBoxLineEdit)



        self.button2.clicked.connect(self.minimize)
        self.button2.clicked.connect(self.screenGrab)

        # athethics/ gives window
        print(self.textbox)
        self.setWindowTitle("Healthy PI")
        self.show()

    def buttonClicked(self):


        #twilio login
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        
        
        
        number = self.textbox.text()
        
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(to=number, from_="+17076402887", media_url=self.images)

    def disableButton(self):

        if len(self.textbox.text()) > 0 and os.path.exists('/home/pi/screenshot.png') and len(self.textbox.text()) == 11:
            self.button.setEnabled(True)


    def uploaded_file(self):


        #Athentifcation
        account = os.environ.get('IMGUR_USER')

        
        #need to change for pi
        path = '/home/pi/screenshot.png'

        
        #image upload
        im = pyimgur.Imgur(account)
        uploaded_image = im.upload_image(path, title="test")



        #test if upload works only!
        #print(uploaded_image.title)  # Cat Ying & Yang
        #print(uploaded_image.link)  # http://imgur.com/S1jmapR.jpg
        

        self.images = uploaded_image.link_huge_thumbnail






    def screenGrab(self):

        # grab fullscreen
        im = ImageGrab.grab()


         # save image file---need to change for PI
        im.save('/home/pi/screenshot.png', 'PNG')




    def minimize(self):
        self.showMinimized()


app = QtWidgets.QApplication(sys.argv)
ourWindow = Window()

sys.exit(app.exec())

