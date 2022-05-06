import json


def loadJsonFile(filename: str):
    try:
        file = open(filename)
    except IOError:
        print("Could not open " + filename)
        return

    return json.loads(file.read())
