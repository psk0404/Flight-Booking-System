from login_win import *
from main_win import *
import atexit

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication([])

# 显示登录界面
share.loginWin = win_login()
share.loginWin.ui.show()

# 在程序退出时调用 save_slide()
atexit.register(share.save_slide)

# 启动事件循环
app.exec_()

