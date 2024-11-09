# src/QT_src/main_system.py
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QSizePolicy
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from functools import partial
import os
from src.QT_src.Info import *
from src.QT_src.buy import BuyWindow
from src.lib.share import *
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
    def __init__(self, a, b):
        super(Mainsystem, self).__init__()
        self.got = get(a, b)
        self.ui = loadUi(share.MainSyetem_ui, self)
        self.setup_scroll_area()
        self.ui.pushButton.clicked.connect(self.show_user_info)

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
            buy_button.clicked.connect(partial(self.buy_ticket, flights))
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
            self.expand_or_collapse_label(label, label.expanded_height)
            label.setText(label.original_text)
            button.setText("收起")
            label.expanded = True
        else:
            self.expand_or_collapse_label(label, 100)
            label.setText(label.simplified_text)
            button.setText("展开")
            label.expanded = False
            label.adjustSize()
            label.setFixedHeight(100)

    def expand_or_collapse_label(self, label, end_height):
        label.setFixedHeight(end_height)

    def buy_ticket(self, flights):
        self.buy_window = BuyWindow(flights)
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

    def show_user_info(self):
        self.user_info_window = userInfo()
        self.user_info_window.show()

class get:
    def __init__(self, a, b):
        self.loader = data_loader(share.directory)
        self.loader.load_flights_info()
        self.info = Info(self.loader, a, b)
        self.all = self.info.total

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    share.querywindow_ui = Mainsystem(3, 11)
    share.querywindow_ui.show()
    sys.exit(app.exec_())