# src/QT_src/buy_win.py
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from src.lib.User import *


class BuyWindow(QMainWindow):
    def __init__(self, flights, numflights, lineflights):
        super().__init__()
        self.ui = loadUi(share.BuyWindow_ui, self)
        self.flights = flights
        self.numflights = numflights
        self.lineflights = lineflights
        self.pushButton_2.clicked.connect(self.confirm_purchase)
        self.pushButton_3.clicked.connect(self.cancel_purchase)

        self.init_list_widget()

    def init_list_widget(self):
        self.listWidget.itemClicked.connect(self.update_label_with_image)

    def update_label_with_image(self, item):
        item_text = item.text().strip()

        if item_text == "汉堡三件套":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\hanber.jpg")
        elif item_text == "婴儿餐":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\baby.jpg")
        elif item_text == "清淡套餐":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\hefan.jpg")
        else:
            pixmap = QPixmap()

        scaled_pixmap = pixmap.scaled(self.label_6.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.label_6.setPixmap(scaled_pixmap)
        self.label_6.setScaledContents(True)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)


    def confirm_purchase(self):
        phonenum = self.lineEdit.text().strip()
        password = self.lineEdit_3.text().strip()
        password2 = self.lineEdit_2.text().strip()
        if phonenum == password2 == password == '0':
            QMessageBox.information(self, "购买成功", "购买成功！")
            share.user_flights.append(self.flights)
            share.num_flights.append(self.numflights)
            share.line_flights.append(self.lineflights)
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
    window = BuyWindow()
    window.show()
    sys.exit(app.exec_())