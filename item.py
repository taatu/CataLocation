import os
import json
from config import Config


def getFileNames(path: str) -> list:
    return next(os.walk(path))[2]


def copyFrom(origin: list, copy: list) -> list:
    for i in range(len(copy)):
        for k in origin:
            if k["id"] == copy[i]:
                copy[i] = k

    for i in copy:
        print(str(i))

    for i in origin:
        if i["name"] == "Null":
            for k in copy:
                if k["id"] == i["copy-from"]:
                    i["name"] = k["name"]

    return origin


class TerrainList:
    def __init__(self):
        config = Config()
        self.path = config.path + "/data/json/furniture_and_terrain/"
        self.files = getFileNames(self.path)
        self.terrainList = self._loadTerrain()

    def _loadTerrain(self):
        terrainList = []
        copyList = []
        for i in self.files:
            filename = self.path + i
            file = open(filename)
            data = json.loads(file.read())
            for item in data:
                if item["type"] == "terrain":
                    terr = dict()

                    if "copy-from" in item:
                        terr["copy-from"] = item["copy-from"]
                        copyList.append(item["copy-from"])
                    terr["id"] = item["id"]
                    terr["name"] = item.setdefault("name", "Null")
                    terr["symbol"] = item["symbol"]
                    terr["color"] = item["color"]
                    terr["looks_like"] = item.setdefault("looks_like", "Null")
                    terrainList.append(terr)

                    if "alias" in item:
                        if isinstance(item["alias"], list):
                            for alias in item["alias"]:
                                terr = terr.copy()
                                terr["looks_like"] = terr["id"]
                                terr["id"] = alias
                                terrainList.append(terr)
                        else:
                            terr = terr.copy()
                            terr["looks_like"] = terr["id"]
                            terr["id"] = item["alias"]
                            terrainList.append(terr)

        return copyFrom(terrainList, copyList)

    def getTerrain(self, target: str) -> dict:
        for i in self.terrainList:
            if i["id"] == target:
                return i
