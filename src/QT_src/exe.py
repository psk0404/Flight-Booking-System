from PyQt5.QtWidgets import QApplication
from login_check import *  # 登录相关的逻辑
from src.lib.share import *  # 共享数据
from main_system import *  # 主页面的逻辑

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication([])

# 显示登录界面
share.loginWin = win_login()
share.loginWin.ui.show()

# 启动事件循环
app.exec_()
