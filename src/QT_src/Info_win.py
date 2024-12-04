import random

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QMessageBox, QApplication
from PyQt5.uic import loadUi
from boltons.funcutils import partial
from src.QT_src.change_win import changeWindow
from src.lib.User import *


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
        self.world_map = [
            [1, 950, 225],
            [2, 1000, 210],
            [5, 1640, 245],
            [6, 1700, 300],
            [7, 320, 310],
            [8, 1500, 400],
            [11, 1610, 310],
            [12, 1570, 350],
            [13, 1640, 285]
        ]

        self.horizontalSlider = self.ui.horizontalSlider
        self.horizontalSlider_2 = self.ui.horizontalSlider_2
        self.horizontalSlider_3 = self.ui.horizontalSlider_3

        # Set initial slider values from share.slide
        self.horizontalSlider.setValue(share.slide[0])
        self.horizontalSlider_2.setValue(share.slide[1])
        self.horizontalSlider_3.setValue(share.slide[2])

        self.horizontalSlider.valueChanged.connect(self.update_slider_values)
        self.horizontalSlider_2.valueChanged.connect(self.update_slider_values)
        self.horizontalSlider_3.valueChanged.connect(self.update_slider_values)

    def update_slider_values(self):
        # Save current slider values to share.slide
        share.slide = [
            self.horizontalSlider.value(),
            self.horizontalSlider_2.value(),
            self.horizontalSlider_3.value()
        ]

    def setup_user_info(self):
        layout = QVBoxLayout(self.ui.scrollArea.widget())
        self.ui.scrollArea.widget().setLayout(layout)

        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        for idx, flights in enumerate(share.user_flights):
            if flights and any(flight is not None for flight in flights):
                widget = QWidget()
                card_layout = QVBoxLayout(widget)

                table = self.create_flight_table(flights, idx)
                card_layout.addWidget(table)

                button_layout = QHBoxLayout()

                refund_button = QPushButton("退票")
                refund_button.clicked.connect(partial(self.refund_ticket_group, idx, widget))
                button_layout.addWidget(refund_button)

                change_button = QPushButton("改签")
                change_button.clicked.connect(partial(self.change_ticket_group, idx))
                button_layout.addWidget(change_button)

                card_layout.addLayout(button_layout)
                layout.addWidget(widget)

        self.ui.scrollArea.setWidgetResizable(True)

    def refund_ticket_group(self, user_idx, widget):
        share.user_flights[user_idx] = [None] * len(share.user_flights[user_idx])

        widget.setParent(None)

        QMessageBox.information(self, "退票成功", "航班已退票！")

    def create_flight_table(self, flights, user_idx):
        table = QTableWidget(len(flights), 12)
        table.setHorizontalHeaderLabels(
            ["信息编号", "出发时间", "出发机场", "飞行时间", "到达时间", "到达机场", "航班信息", "票价", "操作",
             "餐饮服务", "住宿服务", "接机服务"])

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 120)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 100)
        table.setColumnWidth(5, 120)
        table.setColumnWidth(6, 120)
        table.setColumnWidth(7, 100)
        table.setColumnWidth(8, 80)
        table.setColumnWidth(9, 100)
        table.setColumnWidth(10, 100)
        table.setColumnWidth(11, 100)

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

            route_button = QPushButton("航线")
            route_button.clicked.connect(partial(self.view_route, user_idx, row))
            table.setCellWidget(row, 8, route_button)

            services = share.service[user_idx]
            service1 = "无"
            if row + 1 in share.food_order[user_idx]:
                service1 = ["汉堡三件套", "婴儿餐", "清淡套餐", "无"][services[0] - 1]

            service2 = "无"
            service3 = "无"
            if row == len(flights) - 1:
                service2 = ["七天酒店", "汉庭酒店", "希尔顿酒店", "无"][services[1] - 1]
                service3 = ["出租车", "网约车", "机场大巴", "无"][services[2] - 1]

            table.setItem(row, 9, QTableWidgetItem(service1))
            table.setItem(row, 10, QTableWidgetItem(service2))
            table.setItem(row, 11, QTableWidgetItem(service3))

            table.setRowHeight(row, row_height)

        return table

    def change_ticket_group(self, user_idx):
        self.close()
        change_window = changeWindow(share.num_flights[user_idx], user_idx, self)
        change_window.show()

    def view_route(self, user_idx, row):
        a = share.line_flights[user_idx][row][0]
        b = share.line_flights[user_idx][row][1]

        self.corw(a, b)

        if share.condition == 1:
            self.pixmap = QPixmap(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\background2.png')
            x1, y1 = self.cntworld(a)
            x2, y2 = self.cntworld(b)
            self.printmap(x1, y1, x2, y2)

        elif share.condition == 2:
            self.pixmap = QPixmap(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\cmap.png')
            x1, y1 = self.cntchina(a)
            x2, y2 = self.cntchina(b)
            self.printmap(x1, y1, x2, y2)

        # show picture
        self.ui.map.setPixmap(self.pixmap)
        self.ui.map.setScaledContents(True)

    def update_flight_info(self, user_idx, flights):
        share.user_flights[user_idx] = flights
        self.setup_user_info()

    def printmap(self, x1, y1, x2, y2):
        painter = QPainter(self.pixmap)

        line_pen = QPen(QColor(0, 0, 255))
        line_pen.setWidth(5)
        line_pen.setStyle(Qt.DashLine)
        painter.setPen(line_pen)

        painter.drawLine(x1, y1, x2, y2)

        point_pen = QPen(QColor(255, 0, 0))
        point_pen.setWidth(8)
        painter.setPen(point_pen)
        painter.setBrush(QColor(255, 0, 0))

        small_radius = 10
        painter.drawEllipse(x1 - small_radius // 2, y1 - small_radius // 2, small_radius, small_radius)

        painter.setPen(point_pen)
        painter.setBrush(QColor(255, 0, 0))

        large_radius = 20
        painter.drawEllipse(x2 - large_radius // 2, y2 - large_radius // 2, large_radius, large_radius)

        painter.end()

    def corw(self, a, b):
        cnt = 0
        for i in range(len(self.china_map)):
            if a == self.china_map[i][0] or b == self.china_map[i][0]:
                cnt += 1
        if cnt == 2:
            share.condition = 2
        else:
            share.condition = 1

    def cntchina(self, x):
        if x <= 5:
            return self.china_map[x - 3][1], self.china_map[x - 3][2]
        elif 5 < x <= 12:
            return self.china_map[x - 6][1], self.china_map[x - 6][2]
        elif x > 12:
            return self.china_map[x - 7][1], self.china_map[x - 7][2]

    def cntworld(self, x):
        if x <= 2:
            return self.world_map[x - 1][1], self.world_map[x - 1][2]
        elif 5 <= x <= 8:
            return self.world_map[x - 3][1], self.world_map[x - 3][2]
        elif 11 <= x <= 13:
            return self.world_map[x - 5][1], self.world_map[x - 5][2]


if __name__ == "__main__":
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = userInfo()
    window.show()
    sys.exit(app.exec_())
