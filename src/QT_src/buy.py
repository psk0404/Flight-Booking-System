# src/QT_src/buy.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from src.lib.share import *

class BuyWindow(QMainWindow):
    def __init__(self, flights):
        super().__init__()
        self.ui = loadUi(share.BuyWindow_ui, self)
        self.flights = flights
        self.pushButton_2.clicked.connect(self.confirm_purchase)
        self.pushButton_3.clicked.connect(self.cancel_purchase)

    def confirm_purchase(self):
        phonenum = self.lineEdit.text().strip()
        password = self.lineEdit_3.text().strip()
        password2 = self.lineEdit_2.text().strip()
        if phonenum == password2 == password == '0':
            QMessageBox.information(self, "购买成功", "购买成功！")
            share.user_flights.append(self.flights)
            share.num += 1
            self.close()
        else:
            QMessageBox.warning(self, "购买失败", "存在错误！")

    def cancel_purchase(self):
        self.close()

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = BuyWindow([])
    window.show()
    sys.exit(app.exec_())