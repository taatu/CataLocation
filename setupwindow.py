from config import Config
from signals import *


class browseButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Browse..")


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(300, 300, 600, 200)
        self.signal = Signals()
        self.config = Config()

        vBox = QVBoxLayout()
        hBox = QHBoxLayout()
        self.pathLine = QLineEdit()
        browse = QPushButton()
        browse.setText("Browse..")
        browse.clicked.connect(self.getPath)

        hBox.addWidget(self.pathLine)
        hBox.addWidget(browse)
        vBox.addLayout(hBox)
        self.setLayout(vBox)

        self.show()

    def closeEvent(self, event):
        self.signal.closeSignal.emit()

    def getPath(self):
        msg = "Select Cataclysm main directory"
        path = str(QFileDialog.getExistingDirectory(self, msg))
        if len(path) > 0:
            self.config.path = path
            self.pathLine.setText(self.config.path)
            if self.config.verifyPath():
                self.config.update()
                print("Found cataicon.ico")
