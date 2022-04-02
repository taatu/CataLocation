import sys
from setupwindow import SetupWindow
from grid import *
from item import TerrainList


def main():
    config = Config()
    app = QApplication(sys.argv)

    win = MainWindow()

    terrain = TerrainList()

    if config.path == "Null":
        setup = SetupWindow()
        setup.signal.closeSignal.connect(win.finishInit)
    else:
        if not config.verifyPath():
            print("Error: apparent incorrect path")
        win.finishInit()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
