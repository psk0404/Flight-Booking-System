from login_check import *
from src.lib.share import *

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication([])
share.loginWin = win_login()
share.loginWin.ui.show()
app.exec_()