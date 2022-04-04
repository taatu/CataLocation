import sys
from setupwindow import SetupWindow
from grid import *


def main():
    config = Config()
    app = QApplication(sys.argv)

    win = MainWindow()

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
