import shutil
import json
import os


class Config:
    def __init__(self):
        configFile = self._getConfigFile()
        data = json.loads(configFile.read())
        self.theme = data.setdefault("theme", "light")
        self.path = data.setdefault("cdda-path", "Null")
        self.tileset = data.setdefault("tileset", "UltimateCataclysm")
        self.tilesetList = []
        self.update()
        if self.verifyPath():
            self._fillTilesetList()

    @staticmethod
    def _getConfigFile():
        try:
            configFile = open("config.cfg")
        except IOError:
            try:
                shutil.copyfile("data/defaultconfig.cfg", "config.cfg")
                configFile = open("config.cfg")
            except IOError:
                msg = "Error: Could not open config file. Check that CataLocation.py has permission to read/write files"
                print(msg)
                return None

        return configFile

    def _fillTilesetList(self):
        path = self.path + "/gfx"
        for i in next(os.walk(path))[1]:    # gets all the first-level subdirectories
            self.tilesetList.append(i)

    def update(self):
        configFile = open("config.cfg", "w")
        out = {"theme": self.theme, "cdda-path": self.path, "tileset": self.tileset}
        json.dump(out, configFile)
        configFile.close()

    def verifyPath(self) -> bool:
        exactPath = self.path + "/data/cataicon.ico"
        try:
            f = open(exactPath)
            f.close()
            return True
        except IOError:
            return False

