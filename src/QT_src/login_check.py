from PyQt5.uic import loadUi

from src.lib.share import *
from main_system import *

class win_login:
    def __init__(self):
        self.ui = loadUi(share.win_login_ui)

        self.ui.Button_login.clicked.connect(self.onSignIn)
        self.ui.Edit_username.returnPressed.connect(self.onSignIn)
        self.ui.Edit_password.returnPressed.connect(self.onSignIn)

    def onSignIn(self):
        username = self.ui.Edit_username.text().strip()
        password = self.ui.Edit_password.text().strip()

        if username != '0' or password != '0':
            QMessageBox.warning(
                self.ui,
                '登陆失败',
                '用户名或密码错误，请重新输入'
            )
            return

        share.mainWin = Mainsystem()
        share.mainWin.ui.show()
        share.loginWin.ui.close()






