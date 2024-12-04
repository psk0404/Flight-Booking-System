# src/QT_src/buy_win.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from src.lib.User import *


class BuyWindow(QMainWindow):
    def __init__(self, flights, numflights, lineflights, times):
        super().__init__()
        self.ui = loadUi(share.BuyWindow_ui, self)
        self.flights = flights
        self.numflights = numflights
        self.lineflights = lineflights
        self.pushButton_2.clicked.connect(self.confirm_purchase)
        self.pushButton_3.clicked.connect(self.cancel_purchase)

        self.init_list_widget()
        self.times = times
        self.mem = [4, 4, 4]
        self.mem2 = []
        self.create_dynamic_list_widget()

    def create_dynamic_list_widget(self):
        self.listWidget_4.clear()

        font = QFont("华文中宋", 11)
        font.setStyleStrategy(QFont.PreferAntialias)

        for i in range(self.times):
            item = QListWidgetItem(str(i + 1))

            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)

            self.listWidget_4.addItem(item)


    def init_list_widget(self):
        self.listWidget.itemClicked.connect(self.update_label_with_image1)
        self.listWidget_2.itemClicked.connect(self.update_label_with_image2)
        self.listWidget_3.itemClicked.connect(self.update_label_with_image3)

    def update_label_with_image1(self, item):
        item_text = item.text().strip()

        if item_text == "汉堡三件套":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\hanber.jpg")
            self.mem[0] = 1
        elif item_text == "婴儿餐":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\baby.jpg")
            self.mem[0] = 2
        elif item_text == "清淡套餐":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\hefan.jpg")
            self.mem[0] = 3
        else:
            pixmap = QPixmap()
            self.mem[0] = 4

        scaled_pixmap = pixmap.scaled(self.label_6.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.label_6.setPixmap(scaled_pixmap)
        self.label_6.setScaledContents(True)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)

    def update_label_with_image2(self, item):
        item_text = item.text().strip()

        if item_text == "七天酒店":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\qitian.jpg")
            self.mem[1] = 1
        elif item_text == "汉庭酒店":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\hanting.jpg")
            self.mem[1] = 2
        elif item_text == "希尔顿酒店":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\hilton.jpg")
            self.mem[1] = 3
        else:
            pixmap = QPixmap()
            self.mem[1] = 4

        scaled_pixmap = pixmap.scaled(self.label_7.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.label_7.setPixmap(scaled_pixmap)
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)

    def update_label_with_image3(self, item):
        item_text = item.text().strip()

        if item_text == "出租车":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\Taxi.jpg")
            self.mem[2] = 1
        elif item_text == "网约车":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\wang.jpg")
            self.mem[2] = 2
        elif item_text == "机场大巴":
            pixmap = QPixmap(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\bus.jpg")
            self.mem[2] = 3
        else:
            pixmap = QPixmap()
            self.mem[2] = 4

        scaled_pixmap = pixmap.scaled(self.label_8.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.label_8.setPixmap(scaled_pixmap)
        self.label_8.setScaledContents(True)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)

    def confirm_purchase(self):
        phonenum = self.lineEdit.text().strip()
        password = self.lineEdit_3.text().strip()
        password2 = self.lineEdit_2.text().strip()

        if phonenum == password2 == password == '0':
            QMessageBox.information(self, "购买成功", "购买成功！")
            share.user_flights.append(self.flights)
            share.num_flights.append(self.numflights)
            share.line_flights.append(self.lineflights)

            share.service.append([self.mem[0], self.mem[1], self.mem[2]])

            # Initialize self.mem2 if not already done
            if not self.mem2:
                self.mem2 = [[] for _ in range(self.times)]
            # Get selected items from listWidget_4 and convert to integers
            selected_items = self.listWidget_4.selectedItems()

            self.mem2[share.num] = [int(item.text()) for item in selected_items]

            self.mem2[share.num].sort()

            share.food_order.append(self.mem2[share.num])

            # print(share.food_order[0])
            # print(share.service[0], share.service[1], share.service[2]
            share.num += 1

            self.close()
        else:
            QMessageBox.warning(self, "购买失败", "抱歉，存在错误！")

    def cancel_purchase(self):
        self.close()

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = BuyWindow()
    window.show()
    sys.exit(app.exec_())