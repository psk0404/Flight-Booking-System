from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QWidget, QSizePolicy)
from PyQt5.uic import loadUi
from functools import partial
import os
import re
from datetime import datetime

from src.QT_src.buy import BuyWindow
from src.lib.share import *
from src.algorithm.flight_find import Info
from src.algorithm.data_manager import data_loader


class MyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args, **kwargs)
        self.setFixedHeight(100)  # 默认高度为100
        self.expanded = False
        self.original_text = ""  # 保存展开前的内容
        self.simplified_text = ""  # 保存简洁信息
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为扩展
        self.setWordWrap(True)  # 允许自动换行

        # 设置初始样式
        self.setStyleSheet("""
            QLabel {
                background-color: #f0f8ff;  /* 浅蓝色背景 */
                border: 1px solid #87cefa;  /* 天蓝色边框 */
                border-radius: 15px;  /* 圆角效果 */
                padding: 0px;  /* 内边距 */
                margin: 0px;  /* 外边距 */
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);  /* 阴影效果 */
                font-family: "Arial", sans-serif;  /* 字体 */
                font-size: 14px;  /* 字体大小 */
                color: #333;  /* 字体颜色 */
            }
        """)


class Mainsystem(QMainWindow):
    def __init__(self, a, b):
        super(Mainsystem, self).__init__()
        self.got = get(a, b)
        self.ui = loadUi(share.MainSyetem_ui, self)
        self.setup_scroll_area()

    def setup_scroll_area(self):
        layout = QVBoxLayout()

        for i in range(len(self.got.all)):
            flights = []
            for j in range(len(self.got.all[i])):
                num0 = self.got.all[i][j][0]
                num1 = self.got.all[i][j][1]
                num2 = self.got.all[i][j][2]

                flights.append(self.got.loader.get_flight_info_all(num0, num1, num2))

            widget = QWidget()
            card_layout = QVBoxLayout(widget)
            label = MyLabel(self.format_flight_info(flights))
            label.original_text = self.format_flight_info(flights, expanded=True)
            label.simplified_text = self.format_flight_info(flights, expanded=False)

            label.setFont(QFont("Arial", 9))
            label.setFrameShape(QFrame.Box)
            label.setMargin(5)

            button_layout = QHBoxLayout()
            expand_button = QPushButton("展开")
            expand_button.clicked.connect(partial(self.toggle_expansion, label, expand_button))

            buy_button = QPushButton("购买")
            buy_button.clicked.connect(lambda checked, idx=i + 1: self.buy_ticket(idx))  # 将航班索引传递给购买按钮

            button_layout.addWidget(expand_button)
            button_layout.addWidget(buy_button)

            card_layout.addWidget(label)
            card_layout.addLayout(button_layout)
            layout.addWidget(widget)

            label.expanded_height = 225 * len(self.got.all[i])

        self.ui.scrollArea.widget().setLayout(layout)
        self.ui.scrollArea.setWidgetResizable(True)

    def toggle_expansion(self, label, button):
        if not label.expanded:
            # 展开时，更新高度和文本
            self.expand_or_collapse_label(label, label.expanded_height)
            label.setText(label.original_text)  # 展开时显示完整的航班信息
            button.setText("收起")  # 改变按钮的文本为"收起"
            label.expanded = True
        else:
            # 收起时，更新高度和文本
            self.expand_or_collapse_label(label, 100)  # 设置为初始高度100
            label.setText(label.simplified_text)  # 使用简洁信息
            button.setText("展开")  # 改变按钮的文本为"展开"
            label.expanded = False

            # 强制刷新界面，确保高度恢复为100
            label.adjustSize()  # 调整标签大小
            label.setFixedHeight(100)  # 设置固定高度为100

    def expand_or_collapse_label(self, label, end_height):
        label.setFixedHeight(end_height)

    def buy_ticket(self, idx):
        print(f"购买航班 {idx} 的票")

    def format_flight_info(self, flights, expanded=False):
        flight_info = ""

        def load_html_template(template_name):
            template_path = os.path.join(r'C:\Users\Lenovo\PycharmProjects\BJUT_dsc\html_templates', template_name)
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()

        if expanded:
            for flight in flights:
                departure_time, departure_airport, duration, arrival_time, arrival_airport, flight_number, price = flight
                template = load_html_template('flight_info_detailed.html')
                flight_info += template.format(
                    departure_time=departure_time.strftime('%H:%M'),
                    arrival_time=arrival_time.strftime('%H:%M'),
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    duration=duration,
                    flight_number=flight_number,
                    price=price
                )
        else:
            totalprice = 0
            times = len(flights)
            for flight in flights:
                totalprice += flight[6]
            departure_time = flights[0][0]
            arrival_time = flights[-1][3]

            template = load_html_template('flight_info_simplified.html')
            flight_info += template.format(
                departure_time=departure_time.strftime('%H:%M'),
                arrival_time=arrival_time.strftime('%H:%M'),
                transfers=times,
                price=totalprice
            )

        return flight_info

    def parse_flight_info(self, original_text):
        flight_info = []

        departure_time_pattern = r"<b>出发时间:</b>\s*(\d{2}:\d{2})"
        departure_time_match = re.search(departure_time_pattern, original_text)
        departure_time = departure_time_match.group(1) if departure_time_match else None

        arrival_time_pattern = r"<b>到达时间:</b>\s*(\d{2}:\d{2})"
        arrival_time_match = re.search(arrival_time_pattern, original_text)
        arrival_time = arrival_time_match.group(1) if arrival_time_match else None

        price_pattern = r"<b>票价:</b>\s*¥([\d,]+)"
        price_match = re.search(price_pattern, original_text)
        price = int(price_match.group(1).replace(',', '')) if price_match else None

        transfers_pattern = r"<b>班次:</b>\s*(\d+)"
        transfers_match = re.search(transfers_pattern, original_text)
        transfers = int(transfers_match.group(1)) if transfers_match else None

        if departure_time and arrival_time and price and transfers is not None:
            departure_time_obj = datetime.strptime(departure_time, "%H:%M")
            arrival_time_obj = datetime.strptime(arrival_time, "%H:%M")
            duration = str(arrival_time_obj - departure_time_obj)

            flight_info.append((
                departure_time_obj.strftime("%H:%M"),
                "JFK",
                duration,
                arrival_time_obj.strftime("%H:%M"),
                "LAX",
                price,
                transfers
            ))

        return flight_info

    def buy_ticket(self, idx):
        print(f"购买航班 {idx} 的票")
        # 弹出购买窗口
        self.buy_window = BuyWindow()
        self.buy_window.show()


class get:
    def __init__(self, a, b):
        self.loader = data_loader(share.directory)
        self.loader.load_flights_info()
        self.info = Info(self.loader, a, b)  # 创建 Info 实例，并传入数据加载器和路径参数
        self.all = self.info.total


if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    share.querywindow_ui = Mainsystem(3, 11)
    share.querywindow_ui.show()  # 显示窗口
    sys.exit(app.exec_())  # 运行应用程序
