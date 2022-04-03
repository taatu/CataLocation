from tile import TileConfig, Pixmap
from config import Config
from menu import *
from location import Location

# import qdarktheme


class Cell(QLabel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.pixmapList = []
        self.labelList = []

    def addPixmap(self, pixmap: Pixmap):
        length = len(self.pixmapList)
        if length == 0:
            self.pixmapList.append(pixmap)
        else:
            for i in range(length):
                if pixmap.layer >= self.pixmapList[i].layer:
                    self.pixmapList.insert(i, pixmap)      # inserts BEFORE i-th element
                    break

    def draw(self):
        super().show()
        if not self.isVisible():
            return
        pos = self.mapToGlobal(QPoint(0, 0))
        x = pos.x()
        y = pos.y()

        for i in self.pixmapList:
            label = QLabel(self.parent)
            label.setFixedSize(i.width(), i.height())
            label.setPixmap(i)
            self.labelList.append(label)
            label.move(x+i.xOffset-self.parent.xPos, y+i.yOffset-self.parent.yPos)
            label.show()

    def mousePressEvent(self, event):
        print(self.pixmapList[0].name)


class Grid(QWidget):
    def __init__(self):
        super().__init__()

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.config = Config()
        self.path = None
        self.tileConfig = None
        self.x = 24
        self.y = 24
        self.xPos = None
        self.yPos = None

        self.location = Location("{}/data/json/mapgen/daycare.json".format(self.config.path))

        self.images = self.location.processed

        self.cache = {}

        self.gridLayout.setSpacing(0)
        self.gridLayout.setAlignment(Qt.AlignCenter)

    def updateTileConfig(self):
        self._updateTileConfig()
        QTimer.singleShot(0, self._updateTileConfig)

    def _updateTileConfig(self):
        """Due to using absolute positioning, this needs to be run twice"""
        self.config = Config()
        self.cache.clear()
        self.path = "{}/gfx/{}/tile_config.json".format(self.config.path, self.config.tileset)
        self.tileConfig = TileConfig(self.path)
        self.setMinimumSize(24*self.tileConfig.getScale(), 24*self.tileConfig.getScale())
        pos = self.mapToGlobal(QPoint(0, 0))
        self.xPos = pos.x()
        self.yPos = pos.y()

        for i in range(self.x):
            for j in range(self.y):
                current = self.images[i][j]
                cell = Cell(self)
                if current in self.cache:
                    cell.addPixmap(self.cache[current])
                    cell.setFixedSize(int(self.tileConfig.getScale()), int(self.tileConfig.getScale()))
                else:
                    image = self.tileConfig.getSprite(current)
                    # image = image.scaledToHeight(int(self.tileConfig.getScale()))
                    cell.addPixmap(image)
                    cell.setFixedSize(int(self.tileConfig.getScale()), int(self.tileConfig.getScale()))
                    self.cache[current] = image
                if self.gridLayout.itemAtPosition(i, j):
                    self.gridLayout.removeWidget(self.gridLayout.itemAtPosition(i, j).widget())

                self.gridLayout.addWidget(cell, i, j)
                cell.draw()

        for i in range(self.x):     # raise cells to the top so they can be clicked
            for j in range(self.y):
                self.gridLayout.itemAtPosition(i, j).widget().raise_()


class ScrollWrap(QScrollArea):
    def __init__(self, widget):
        super().__init__()
        self.setWidget(widget)
        self.setAlignment(Qt.AlignCenter)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.grid = None
        self.statusBar().showMessage("Hey")
        self.setGeometry(180, 144, 800, 600)
        self.setWindowTitle("Grid")

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        newAction = NewAction(self)
        openAction = OpenAction(self)
        saveAction = SaveAction(self)
        saveAsAction = SaveAsAction(self)
        prefsAction = PrefsAction(self)
        quitAction = QuitAction(self)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(prefsAction)
        fileMenu.addAction(quitAction)

        editMenu = menuBar.addMenu("&Edit")

        viewMenu = menuBar.addMenu("&View")

        tilesetMenu = TilesetMenu(self)
        tilesetMenu.signal.tilesetSignal.connect(self.grid.updateTileConfig)
        viewMenu.addMenu(tilesetMenu)

        helpMenu = menuBar.addMenu("&Help")
        return menuBar

    def finishInit(self):   # Called from main()
        print("Running now!")
        self.show()
        if self.config.theme == "dark":
            import qdarktheme
            self.setStyleSheet(qdarktheme.load_stylesheet())

        self.grid = Grid()
        wrapper = ScrollWrap(self.grid)
        self.setCentralWidget(wrapper)
        menuBar = self.initMenuBar()
        self.show()
        self.grid.updateTileConfig()
