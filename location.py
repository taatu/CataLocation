import json
from config import Config


class Location:
    def __init__(self, filename):
        try:
            file = open(filename)
        except IOError:
            print("Could not open file " + str(filename))
            return

        data = json.loads(file.read())
        terrain = data[0]["object"]["terrain"]
        for i in data[0]["object"]["furniture"]:
            if i not in terrain:
                terrain[i] = data[0]["object"]["furniture"][i]
        rows = data[0]["object"]["rows"]
        self.processed = []
        for j in range(24):
            self.processed.append([])
            for k in range(24):
                found = False
                for i in terrain:
                    if i == rows[j][k]:
                        if isinstance(terrain[i], list):
                            if isinstance(terrain[i][0], list):
                                found = True
                                self.processed[j].append(terrain[i][0][0])
                            else:
                                found = True
                                self.processed[j].append(terrain[i][0])
                        else:
                            found = True
                            self.processed[j].append(terrain[i])
                if not found:
                    self.processed[j].append("Null")
        print("Loc done.")

