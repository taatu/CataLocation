from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from prefs import PrefsWindow
from signals import Signals

FOLDER = "data/assets/"


class Icon(QIcon):
    def __init__(self, filename):
        super().__init__(FOLDER + filename)


class FileAction(QAction):
    def __init__(self, icon: str, text: str, parent):
        super().__init__(Icon(icon), text, parent)


class NewAction(FileAction):
    def __init__(self, parent):
        super().__init__("new.png", "&New", parent)
        self.setShortcut("Ctrl+N")
        self.setStatusTip("Create a new document")


class OpenAction(FileAction):
    def __init__(self, parent):
        super().__init__("open.png", "&Open", parent)
        self.setStatusTip("Open a file")


class SaveAction(FileAction):
    def __init__(self, parent):
        super().__init__("save.png", "Save", parent)
        self.setShortcut("Ctrl+S")
        self.setStatusTip("Save the current document")


class SaveAsAction(FileAction):
    def __init__(self, parent):
        super().__init__("saveas.png", "Save as..", parent)
        self.setStatusTip("Save the current document as a new document")


class PrefsAction(FileAction):
    def __init__(self, parent):
        super().__init__("settings.png", "Preferences", parent)
        self.setStatusTip("Open the settings menu")
        self.prefsWindow = PrefsWindow()
        self.triggered.connect(lambda: self.prefsWindow.show())


class QuitAction(FileAction):
    def __init__(self, parent):
        super().__init__("quit.png", "Quit", parent)
        self.setShortcut("Ctrl+Q")
        self.setStatusTip("Exit the application")
        self.triggered.connect(qApp.quit)


class TilesetMenu(QMenu):
    def __init__(self, parent):
        self.config = parent.config
        self.signal = Signals()
        super().__init__("Tileset", parent)
        actionGroup = QActionGroup(self)
        actionGroup.setExclusive(True)
        for elem in self.config.tilesetList:
            action = QAction(elem, parent)
            action.setData(elem)
            action.setCheckable(True)
            if parent.config.tileset == elem:
                action.setChecked(True)
            action.triggered.connect(self.updateTileset)
            actionGroup.addAction(action)
            self.addAction(action)

    def updateTileset(self):
        for elem in self.actions():
            if elem.isChecked():
                self.config.tileset = elem.data()
                self.config.update()
                self.signal.tilesetSignal.emit()


