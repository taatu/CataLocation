from tile import TileConfig
from config import Config
from menu import *
from location import Location

# import qdarktheme


class Cell(QLabel):
    def __init__(self, image):
        super().__init__()
        self.setPixmap(image)


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

        self.location = Location("{}/data/json/mapgen/daycare.json".format(self.config.path))

        self.images = self.location.processed

        self.cache = {}

        self.updateTileConfig()

        self.gridLayout.setSpacing(0)
        self.gridLayout.setAlignment(Qt.AlignCenter)

    def updateTileConfig(self):
        self.config = Config()
        self.cache.clear()
        self.path = "{}/gfx/{}/tile_config.json".format(self.config.path, self.config.tileset)
        self.tileConfig = TileConfig(self.path)
        self.setMinimumSize(24*self.tileConfig.getScale(), 24*self.tileConfig.getScale())
        prev = None

        for i in range(self.x):
            for j in range(self.y):
                if self.images[i][j] in self.cache:
                    cell = Cell(self.cache[self.images[i][j]])
                else:
                    image = self.tileConfig.getSprite(self.images[i][j])
                    image = image.scaledToHeight(int(1*self.tileConfig.getScale()))
                    cell = Cell(image)
                    self.cache[self.images[i][j]] = image
                if self.gridLayout.itemAtPosition(i, j):
                    self.gridLayout.removeWidget(self.gridLayout.itemAtPosition(i, j).widget())

                self.gridLayout.addWidget(cell, i, j)


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
        if self.config.theme == "dark":
            import qdarktheme
            self.setStyleSheet(qdarktheme.load_stylesheet())

        self.grid = Grid()
        wrapper = ScrollWrap(self.grid)
        self.setCentralWidget(wrapper)
        menuBar = self.initMenuBar()
        self.show()

