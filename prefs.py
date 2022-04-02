from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from config import Config


class PrefsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preferences")
        self.setGeometry(400, 200, 400, 400)

