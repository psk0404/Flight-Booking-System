import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QLabel
from PyQt5.uic import loadUi
from boltons.funcutils import partial
from src.QT_src.change import changeWindow
from src.lib.share import *

class userInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi(share.UserInfo_ui, self)
        self.setup_user_info()
        self.china_map = [
            [3, 947, 396],
            [4, 637, 663],
            [5, 1106, 265],
            [9, 1010, 602],
            [10, 1010, 795],
            [11, 1070, 663],
            [12, 913, 855],
            [14, 313, 301],
            [15, 841, 626],
            [16, 745, 566]
        ]
        self.view_route(share.condition)

    def setup_user_info(self):
        layout = QVBoxLayout()
        widgets_to_remove = []

        for widget in self.ui.scrollArea.widget().findChildren(QWidget):
            widgets_to_remove.append(widget)

        for widget in widgets_to_remove:
            widget.deleteLater()

        for idx, flights in enumerate(share.user_flights):
            if flights and any(flight is not None for flight in flights):
                widget = QWidget()
                card_layout = QVBoxLayout(widget)

                table = self.create_flight_table(flights, idx)
                card_layout.addWidget(table)

                button_layout = QHBoxLayout()

                refund_button = QPushButton("退票")
                refund_button.clicked.connect(partial(self.refund_ticket_group, idx))
                button_layout.addWidget(refund_button)

                change_button = QPushButton("改签")
                change_button.clicked.connect(partial(self.change_ticket_group, idx))
                button_layout.addWidget(change_button)

                card_layout.addLayout(button_layout)

                layout.addWidget(widget)

        self.ui.scrollArea.widget().setLayout(layout)
        self.ui.scrollArea.setWidgetResizable(True)

    def create_flight_table(self, flights, user_idx):
        table = QTableWidget(len(flights), 9)  # 修改列数，增加一列用于放按钮
        table.setHorizontalHeaderLabels(
            ["信息编号", "出发时间", "出发机场", "飞行时间", "到达时间", "到达机场", "航班信息", "票价", "操作"])

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 120)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 100)
        table.setColumnWidth(5, 120)
        table.setColumnWidth(6, 120)
        table.setColumnWidth(7, 100)
        table.setColumnWidth(8, 80)  # 设置按钮列的宽度

        table.setFixedHeight(160)

        row_height = 40
        for row, flight in enumerate(flights):
            if flight is None:
                continue

            departure_time, departure_airport, duration, arrival_time, arrival_airport, flight_number, price = flight
            table.setItem(row, 0, QTableWidgetItem(f"0000{random.randint(0, 9999):04d}"))
            table.setItem(row, 1, QTableWidgetItem(departure_time.strftime('%H:%M')))
            table.setItem(row, 2, QTableWidgetItem(departure_airport))
            table.setItem(row, 3, QTableWidgetItem(duration))
            table.setItem(row, 4, QTableWidgetItem(arrival_time.strftime('%H:%M')))
            table.setItem(row, 5, QTableWidgetItem(arrival_airport))
            table.setItem(row, 6, QTableWidgetItem(flight_number))
            table.setItem(row, 7, QTableWidgetItem(f"¥{price}"))

            # 创建航线按钮并放到最后一列
            route_button = QPushButton("航线")
            route_button.clicked.connect(partial(self.view_route))

            table.setCellWidget(row, 8, route_button)

            table.setRowHeight(row, row_height)

        return table

    def refund_ticket_group(self, user_idx):
        share.user_flights[user_idx] = [None] * len(share.user_flights[user_idx])
        self.setup_user_info()
        QMessageBox.information(self, "退票成功", "航班已退票！")

    def change_ticket_group(self, user_idx):
        self.close()
        change_window = changeWindow(share.num_flights[user_idx], user_idx, self)
        change_window.show()

    def update_flight_info(self, user_idx, flights):
        share.user_flights[user_idx] = flights
        self.setup_user_info()

    def view_route(self, condition):
        if condition == 0:
            self.pixmap = QPixmap(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\background2.png')
        elif condition == 1:
            self.pixmap = QPixmap(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\cmap.png')

            self.printmap(0, 0, 1250, 1000)

        # show picture
        self.ui.map.setPixmap(self.pixmap)
        self.ui.map.setScaledContents(True)

    def printmap(self, x1, y1, x2, y2):
        # 创建 QPainter 对象
        painter = QPainter(self.pixmap)
        # 设置画笔，使用 QColor 来设置颜色
        pen = QPen(QColor(0, 0, 255))  # 这里用 QColor(0, 0, 255) 表示蓝色
        pen.setWidth(5)  # 设置线宽

        painter.setPen(pen)
        # 绘制线条
        painter.drawLine(x1, y1, x2, y2)
        # 结束绘制
        painter.end()