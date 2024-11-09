from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from src.lib.share import *

class userInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi(share.UserInfo_ui, self)


if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = userInfo()
    window.show()
    sys.exit(app.exec_())