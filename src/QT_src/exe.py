from login_check import *
from main_system import *

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication([])

# 显示登录界面
share.loginWin = win_login()
share.loginWin.ui.show()

# 启动事件循环
app.exec_()
