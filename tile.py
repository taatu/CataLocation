from common import *

from config import Config
from item import TerrainList
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt


class Pixmap(QPixmap):
    def __init__(self, name: str, xOffset: int, yOffset: int, qPixmap: QPixmap):
        super().__init__(qPixmap)
        self.name = name
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.layer = 0


class TileFile:

    def __init__(self, data: dict, parent):
        self.name = data["file"]
        self.width = data.setdefault("sprite_width", parent.width)
        self.height = data.setdefault("sprite_height", parent.height)
        self.xOffset = data.setdefault("sprite_offset_x", 0)
        self.yOffset = data.setdefault("sprite_offset_y", 0)
        self.config = parent.config
        self.pixelScale = parent.pixelScale

        sheetPath = "{}/gfx/{}/{}".format(self.config.path, self.config.tileset, self.name)
        self.tileSheet = QImage(sheetPath)
        self.columns = self.tileSheet.width() / self.width

        if "ascii" in data:
            self.isAscii = True
            self.tileList = self.createFallback(data["ascii"])
            return
        else:
            self.isAscii = False

        # use the "comment" field to get the offset of the index
        if "//" in data:
            self.indexOffset = str(data["//"])
            self.indexOffset = self.indexOffset.split(" ")
            self.indexOffset = int(self.indexOffset[1])
            if self.indexOffset == 1:
                self.indexOffset = 0
        else:
            print("Warning: tileset is missing tile offsets. May result in graphical errors")
            self.indexOffset = 0

        self.tileList = self.createTileList(data)

    def createFallback(self, data):
        colorCodes = loadJsonFile("data/color.json")
        tileList = []
        for i in data:
            tileList.append(self.getColor(i, colorCodes))
        print(str(tileList))
        return tileList

    @staticmethod
    def getColor(data, colorCodes):
        tile = dict()
        for i in colorCodes:
            if i["bold"] == data["bold"] and i["color"] == data["color"]:
                tile["color"] = i["colorcode"]
                tile["offset"] = data["offset"]
                return tile

    def getFallbackSprite(self, target, color, symbol, parent) -> Pixmap:
        offset = None
        for i in self.tileList:
            if i["color"] == color:
                offset = i["offset"]

        if offset is None:
            print("Invalid color: " + str(color))
            return parent.getErrorSprite()

        img = QPixmap()
        if len(symbol) == 1:
            location = offset + ord(symbol)
        else:
            location = offset + ord("|")
        x = (self.width * (location % self.columns))
        y = (self.height * int(location / self.columns))
        w = self.width
        h = self.height
        height = self.height * self.pixelScale
        img.convertFromImage(self.tileSheet.copy(x, y, w, h))
        pixmap = Pixmap(target, 0, 0, img.scaledToHeight(height))
        return pixmap

    def createTileList(self, data: dict) -> list:

        tileList = []
        tileData = data["tiles"]
        for i in tileData:
            if ("fg" not in i) and ("bg" not in i):
                continue

            if isinstance(i["id"], list):
                for k in i["id"]:
                    tileList.append(self.fillTileInfo(i, k))
            else:
                tileList.append(self.fillTileInfo(i, i["id"]))

        return tileList

    def fillTileInfo(self, parent: dict, idParent: str) -> dict:
        tile = dict()
        tile["id"] = idParent
        if "fg" in parent:
            tile["fg"] = self.reduceSprite(parent["fg"])
        if "bg" in parent:
            tile["bg"] = self.reduceSprite(parent["bg"])
        if "additional_tiles" in parent:
            tile = self.getVariants(tile, parent)

        return tile

    def getVariants(self, tile: dict, parent: dict) -> dict:
        tile["variants"] = parent["additional_tiles"]
        for elem in tile["variants"]:
            if elem["id"] == "center" and "fg" in elem:
                tile["fg"] = self.reduceSprite(elem["fg"])

        return tile

    @staticmethod
    def reduceSprite(arg) -> int:
        if isinstance(arg, list):
            if len(arg) == 0:
                return -1
            if isinstance(arg[0], dict):
                maxWeight = 0
                for i in arg:
                    if i["weight"] > maxWeight:
                        maxWeight = i["weight"]
                        sprite = i["sprite"]
            else:
                sprite = arg[0]
            return sprite
        else:
            return arg

    def getSprite(self, tile: dict) -> Pixmap:
        foreground = QPixmap()
        background = QPixmap()
        out = QPixmap(self.width, self.height)
        foreground.fill(Qt.transparent)
        background.fill(Qt.transparent)
        out.fill(Qt.transparent)
        painter = QPainter(out)

        if "fg" in tile:
            location = tile["fg"] - self.indexOffset
            x = (self.width * (location % self.columns))
            y = (self.height * int(location / self.columns))
            w = self.width
            h = self.height
            foreground.convertFromImage(self.tileSheet.copy(x, y, w, h))

        if "bg" in tile:
            location = tile["bg"] - self.indexOffset
            x = (self.width * (location % self.columns))
            y = (self.height * int(location / self.columns))
            w = self.width
            h = self.height
            background.convertFromImage(self.tileSheet.copy(x, y, w, h))

        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, background)
        painter.drawPixmap(0, 0, foreground)
        painter.end()

        xOffset = self.xOffset * self.pixelScale
        yOffset = self.yOffset * self.pixelScale
        height = self.height * self.pixelScale

        pixmap = Pixmap(tile["id"], xOffset, yOffset, out.scaledToHeight(height))
        return pixmap


class TileConfig:
    def __init__(self, filename):
        data = loadJsonFile(filename)
        tileInfo = data["tile_info"][0]
        self.pixelScale = tileInfo.setdefault("pixelscale", 1)
        self.width = tileInfo["width"]
        self.height = tileInfo["height"]
        self.config = Config()
        self.terrainList = TerrainList()

        tilesNew = data["tiles-new"]
        self.files = []

        for i in tilesNew:
            tileFile = TileFile(i, self)
            self.files.append(tileFile)

    def getScale(self) -> int:
        return self.pixelScale * self.height

    def getFallbackSprite(self, target) -> Pixmap:
        item = self.terrainList.getTerrain(target)
        color = item["color"]
        symbol = item["symbol"]
        for tileFile in self.files:
            if tileFile.isAscii:
                return tileFile.getFallbackSprite(target, color, symbol, self)

    def getErrorSprite(self) -> Pixmap:
        sprite = QPixmap()
        sprite.load("data/assets/quit.png")
        out = Pixmap("Null", 0, 0, sprite.scaledToHeight(self.height*self.pixelScale))
        return out

    def getSprite(self, target: str) -> Pixmap:
        for tileFile in self.files:
            if tileFile.isAscii:
                continue
            for tile in tileFile.tileList:
                if tile["id"] == target:
                    return tileFile.getSprite(tile)

        try:
            if self.terrainList.getTerrain(target)["looks_like"] == "Null":
                return self.getFallbackSprite(target)
            else:
                return self.getSprite(self.terrainList.getTerrain(target)["looks_like"])
        except TypeError:
            print("warn: target \"" + str(target) + "\" is not valid")
            return self.getErrorSprite()
