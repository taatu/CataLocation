from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Signals(QObject):
    closeSignal = pyqtSignal()
    tilesetSignal = pyqtSignal()
