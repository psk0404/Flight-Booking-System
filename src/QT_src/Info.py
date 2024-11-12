import random

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QMessageBox, QLabel, QApplication
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

    def setup_user_info(self):
        layout = QVBoxLayout(self.ui.scrollArea.widget())
        self.ui.scrollArea.widget().setLayout(layout)

        # 清空原有的布局内容
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # 遍历用户航班信息并添加至布局
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
        # 将对应的航班数据设为 None 以表示已退票
        share.user_flights[user_idx] = [None] * len(share.user_flights[user_idx])

        # 从 scrollArea 布局中移除该航班卡片
        widget.setParent(None)

        QMessageBox.information(self, "退票成功", "航班已退票！")

    def create_flight_table(self, flights, user_idx):
        table = QTableWidget(len(flights), 9)
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
        table.setColumnWidth(8, 80)

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
            route_button.clicked.connect(partial(self.view_route, user_idx, row))

            table.setCellWidget(row, 8, route_button)

            table.setRowHeight(row, row_height)

        return table



    def change_ticket_group(self, user_idx):
        self.close()
        change_window = changeWindow(share.num_flights[user_idx], user_idx, self)
        change_window.show()

    def update_flight_info(self, user_idx, flights):
        share.user_flights[user_idx] = flights
        self.setup_user_info()

    def view_route(self, user_idx, row):
        a = share.line_flights[user_idx][row][0]
        b = share.line_flights[user_idx][row][1]

        self.corw(a, b)

        if share.condition == 1:
            self.pixmap = QPixmap(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\background2.png')
        elif share.condition == 2:
            self.pixmap = QPixmap(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\data\images\cmap.png')
            x1, y1 = self.cntchina(a)
            x2, y2 = self.cntchina(b)
            self.printmap(x1, y1, x2, y2)

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

    def corw(self, a, b):
        cnt = 0
        for i in range(len(self.china_map)):
            if a == self.china_map[i][0] or b == self.china_map[i][0]:
                cnt += 1
        if cnt == 1:
            share.condition = 1
        else:
            share.condition = 2
    def cntchina(self, x):
        if x <= 5:
            return self.china_map[x - 3][1], self.china_map[x - 3][2]
        else:
            return self.china_map[x - 6][1], self.china_map[x - 6][2]

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = userInfo()
    window.show()
    sys.exit(app.exec_())