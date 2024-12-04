import math

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QSizePolicy, QLabel
from functools import partial
import os
import sympy as sp
from src.QT_src.Info_win import *
from src.QT_src.buy_win import BuyWindow
from src.lib.User import share
from src.algorithm.flight_find import Info
from src.algorithm.data_manager import data_loader


class MyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args, **kwargs)
        self.setFixedHeight(100)
        self.expanded = False
        self.original_text = ""
        self.simplified_text = ""
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWordWrap(True)
        self.setStyleSheet(""" 
            QLabel {
                background-color: #f0f8ff;
                border: 1px solid #87cefa;
                border-radius: 15px;
                padding: 0px;
                margin: 0px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                font-family: "Arial", sans-serif;
                font-size: 14px;
                color: #333;
            }
        """)


class Mainsystem(QMainWindow):
    def __init__(self, a, b, from_city_name, to_city_name):
        super(Mainsystem, self).__init__()
        self.got = get(a, b)
        self.ui = loadUi(share.MainSyetem_ui, self)
        self.sort = []  # Initialize self.sort here
        self.setup_scroll_area()

        self.ui.pushButton.clicked.connect(self.show_info)
        self.ui.pushButton1.clicked.connect(self.switch)
        self.ui.pushButton2.clicked.connect(self.exit)
        self.ui.button.clicked.connect(self.f2)
        self.ui.pushButton_2.clicked.connect(self.star)

        self.ui.from_2.currentIndexChanged.connect(self.sort_flights0)
        self.ui.from_3.currentIndexChanged.connect(self.sort_flights1)

        self.ui.fromc.setText(from_city_name)
        self.ui.toc.setText(to_city_name)

        self.ui.fromc.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.ui.fromc.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.toc.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.ui.toc.setAlignment(QtCore.Qt.AlignCenter)

        self.extra = []
        self.best = -1



    def setup_scroll_area(self):
        layout = QVBoxLayout()
        for i in range(len(self.got.all)):
            flights = []
            line_flights = []
            for j in range(len(self.got.all[i])):
                num0 = self.got.all[i][j][0]
                num1 = self.got.all[i][j][1]
                num2 = self.got.all[i][j][2]
                flights.append(self.got.loader.get_flight_info_all(num0, num1, num2))
                line_flights.append([num0, num1])
            time, price = self.calculate(flights)
            self.sort.append([price, time, i])

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
            buy_button.clicked.connect(partial(self.buy, flights, self.got.all, line_flights, len(flights)))
            button_layout.addWidget(expand_button)
            button_layout.addWidget(buy_button)
            card_layout.addWidget(label)
            card_layout.addLayout(button_layout)
            layout.addWidget(widget)
            label.expanded_height = 225 * len(self.got.all[i])

        self.ui.scrollArea.setWidget(QWidget())
        self.ui.scrollArea.widget().setLayout(layout)
        self.ui.scrollArea.setWidgetResizable(True)

    def star(self):
        self.clear_scroll_area()
        self.setup_scroll_area()


    def calculate(self, flights):
        total_price = 0
        total_time = 0
        for flight in flights:
            total_price += flight[6]
        dep_time = flights[0][0]
        arr_time = flights[len(flights) - 1][3]
        dep_minutes = dep_time.hour * 60 + dep_time.minute
        arr_minutes = arr_time.hour * 60 + arr_time.minute
        total_time += arr_minutes - dep_minutes
        return total_time, total_price

    def sort_flights0(self):
        # 获取用户选择的排序方式
        price_sort = self.ui.from_2.currentText().strip() == "升序价格"

        # 排序根据价格
        if price_sort:
            self.sort.sort(key=lambda x: x[0])  # 按价格升序
        else:
            self.sort.sort(key=lambda x: x[0], reverse=True)  # 按价格降序
        # 清空现有内容
        self.clear_scroll_area()
        # 更新显示
        self.update_scroll_area()

    def sort_flights1(self):
        time_sort = self.ui.from_3.currentText().strip() == "升序时间"

        if time_sort:
            self.sort.sort(key=lambda x: x[1])
        else:
            self.sort.sort(key=lambda x: x[1], reverse=True)

        self.clear_scroll_area()

        self.update_scroll_area()

    def clear_scroll_area(self):
        # 获取当前的scroll area widget
        scroll_area_widget = self.ui.scrollArea.widget()

        if scroll_area_widget is not None:
            # 清空现有布局中的所有小部件
            while scroll_area_widget.layout().count():
                item = scroll_area_widget.layout().takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def update_scroll_area(self):
        # 创建新的布局
        layout1 = QVBoxLayout()

        for i in range(len(self.sort)):
            flights = []
            line_flights = []
            k = self.sort[i][2]
            # print(k)
            # 获取航班数据
            for j in range(len(self.got.all[k])):
                num0 = self.got.all[k][j][0]
                num1 = self.got.all[k][j][1]
                num2 = self.got.all[k][j][2]
                flights.append(self.got.loader.get_flight_info_all(num0, num1, num2))
                line_flights.append([num0, num1])

            # 创建新的widget并添加到布局
            widget = QWidget()
            card_layout = QVBoxLayout(widget)
            label = MyLabel(self.format_flight_info(flights))
            label.original_text = self.format_flight_info(flights, expanded=True)
            label.simplified_text = self.format_flight_info(flights, expanded=False)
            label.setFont(QFont("Arial", 9))
            label.setFrameShape(QFrame.Box)
            label.setMargin(5)

            # 创建按钮布局
            button_layout = QHBoxLayout()
            expand_button = QPushButton("展开")
            expand_button.clicked.connect(partial(self.toggle_expansion, label, expand_button))
            buy_button = QPushButton("购买")
            buy_button.clicked.connect(partial(self.buy, flights, self.got.all, line_flights, len(flights)))

            button_layout.addWidget(expand_button)
            button_layout.addWidget(buy_button)

            # 将label和按钮布局添加到card_layout
            card_layout.addWidget(label)
            card_layout.addLayout(button_layout)
            layout1.addWidget(widget)
            label.expanded_height = 225 * len(self.got.all[k])


        self.ui.scrollArea.setWidget(QWidget())
        self.ui.scrollArea.widget().setLayout(layout1)
        self.ui.scrollArea.setWidgetResizable(True)


    def toggle_expansion(self, label, button):
        if not label.expanded:
            self.ec_label(label, label.expanded_height)
            label.setText(label.original_text)
            button.setText("收起")
            label.expanded = True
        else:
            self.ec_label(label, 100)
            label.setText(label.simplified_text)
            button.setText("展开")
            label.expanded = False
            label.adjustSize()
            label.setFixedHeight(100)

    def ec_label(self, label, end_height):
        label.setFixedHeight(end_height)


    def tune(self, flights, times):

        tprice = 0
        for i in range(len(flights)):
            tprice += flights[i][6]

        if tprice != self.best:
            b, a = self.calculate(flights)
            t = times

            score0 = self.cal_ep(a, 0, 0)

            score1 = self.cal_ep(b, 1, 1)

            score2 = self.cal_ep(t, 2, 2)

            # Store the scores in a list
            scores = [score0, score1, score2]

            # Determine the index of the maximum score
            max_index = scores.index(max(scores))

            if 0.8 <= share.value[max_index] <= 1.2:
                share.value[max_index] -= 0.02



    def buy(self, flights, num_flights, line_flights, times):
        if self.best != -1:
            self.tune(flights, times)



        self.buy_window = BuyWindow(flights, num_flights, line_flights, times)
        self.buy_window.show()

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

    def show_info(self):
        self.user_info_window = userInfo()
        self.user_info_window.show()

    def switch(self):
        from src.QT_src.query_win import QueryWindow
        share.queryWin = QueryWindow()
        share.queryWin.show()
        self.close()

    def exit(self):
        self.close()

    def f2(self):
        self.cal_extra()
        self.clear_scroll_area()
        self.update_scroll_area()

    # 筛选
    def screening(self):

        self.extra.clear()

        max_price = float('-inf')
        min_price = float('inf')
        max_time = float('-inf')
        min_time = float('inf')
        max_transfers = float('-inf')
        min_transfers = float('inf')

        for i in range(len(self.got.all)):
            flights = []
            line_flights = []
            for j in range(len(self.got.all[i])):
                num0 = self.got.all[i][j][0]
                num1 = self.got.all[i][j][1]
                num2 = self.got.all[i][j][2]
                flights.append(self.got.loader.get_flight_info_all(num0, num1, num2))
                line_flights.append([num0, num1])

            total_time, total_price = self.calculate(flights)
            transfers = len(flights)

            if total_price > max_price:
                max_price = total_price
            if total_price < min_price:
                min_price = total_price

            if total_time > max_time:
                max_time = total_time
            if total_time < min_time:
                min_time = total_time

            if transfers > max_transfers:
                max_transfers = transfers
            if transfers < min_transfers:
                min_transfers = transfers

        self.extra.append(max_price)
        self.extra.append(min_price)
        self.extra.append(max_time)
        self.extra.append(min_time)
        self.extra.append(max_transfers)
        self.extra.append(min_transfers)

    def cal_ep(self, v, idx0, idx1):
        dof = self.extra[idx0 * 2] - self.extra[idx0 * 2 + 1] + 1
        mof = v
        x = (mof / dof * 4 - 4)

        if share.slide[idx1] > 50:
            a = 25 + (share.slide[idx1] - 50) * 1.5
        else:
            a = share.slide[idx1] * 0.5

        numerator =  math.exp(x) - math.exp(-x)
        denominator = a * math.exp(x) + 0.5 * math.exp(-x)


        return (numerator / denominator + 2) * 50

    def cal_extra(self):

        self.screening()
        self.sort.clear()
        for i in range(len(self.got.all)):
            flights = []
            line_flights = []
            for j in range(len(self.got.all[i])):
                num0 = self.got.all[i][j][0]
                num1 = self.got.all[i][j][1]
                num2 = self.got.all[i][j][2]
                flights.append(self.got.loader.get_flight_info_all(num0, num1, num2))
                line_flights.append([num0, num1])

            time, price = self.calculate(flights)
            trans = len(flights)

            score0 = self.cal_ep(price, 0, 0)
            score1 = self.cal_ep(time, 1, 1)
            score2 = self.cal_ep(trans, 2, 2)

            t_score = share.value[0] * score0 + share.value[1] * score1 + share.value[2] * score2

            self.sort.append([t_score, price, i])


        self.sort.sort(key=lambda x: x[0])
        self.best = self.sort[0][1]

        if len(self.sort) > 3:
            self.sort = self.sort[:3]




class get:
    def __init__(self, a, b):
        self.loader = data_loader(share.directory)
        self.loader.load_flights_info()
        self.info = Info(self.loader, a, b)
        self.all = self.info.total


if __name__ == "__main__":
    import sys
    from PyQt5 import QtCore

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    share.mainWin = Mainsystem(3, 11, '北京', '上海')
    share.mainWin.show()
    sys.exit(app.exec_())