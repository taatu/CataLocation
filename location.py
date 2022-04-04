import json
from config import Config


def unList(target):
    """Get a value from the bottom of nested 1-element lists"""
    if isinstance(target, list):
        return unList(target[0])

    return target


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
                        found = True
                        self.processed[j].append(unList(terrain[i]))
                if not found:
                    self.processed[j].append("Null")
        print("Loc done.")

