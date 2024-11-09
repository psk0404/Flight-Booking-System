from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
from src.lib.share import *  # 共享数据
from src.QT_src.query_window import QueryWindow  # 导入查询页面类
from PyQt5 import QtCore

class win_login:
    def __init__(self):
        self.ui = loadUi(share.win_login_ui)  # 加载登录UI文件

        # 连接登录按钮事件
        self.ui.Button_login.clicked.connect(self.onSignIn)
        self.ui.Edit_username.returnPressed.connect(self.onSignIn)
        self.ui.Edit_password.returnPressed.connect(self.onSignIn)

    def onSignIn(self):
        username = self.ui.Edit_username.text().strip()
        password = self.ui.Edit_password.text().strip()

        if username != '22250423' or password != '22250423':
            QMessageBox.warning(self.ui, '登陆失败', '用户名或密码错误，请重新输入')
            return

        # 登录成功，跳转到查询页面
        share.queryWin = QueryWindow()
        share.queryWin.ui.show()
        share.loginWin.ui.close()  # 关闭登录窗口


# 用于独立测试时运行
if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])  # 创建QApplication实例
    share.loginWin = win_login()  # 创建登录窗口实例
    share.loginWin.ui.show()  # 显示登录窗口
    app.exec_()  # 启动应用事件循环


class win_login:
    def __init__(self):
        self.ui = loadUi(share.win_login_ui)  # 加载登录UI文件

        # 连接登录按钮事件
        self.ui.Button_login.clicked.connect(self.onSignIn)
        self.ui.Edit_username.returnPressed.connect(self.onSignIn)
        self.ui.Edit_password.returnPressed.connect(self.onSignIn)

    def onSignIn(self):
        username = self.ui.Edit_username.text().strip()
        password = self.ui.Edit_password.text().strip()

        if username != '22250423' or password != '22250423':
            QMessageBox.warning(self.ui, '登陆失败', '用户名或密码错误，请重新输入')
            return

        # 登录成功，跳转到查询页面
        share.queryWin = QueryWindow()
        share.queryWin.ui.show()
        share.loginWin.ui.close()  # 关闭登录窗口


# 用于独立测试时运行
if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])  # 创建QApplication实例
    share.loginWin = win_login()  # 创建登录窗口实例
    share.loginWin.ui.show()  # 显示登录窗口
    app.exec_()  # 启动应用事件循环
