from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore

from src.algorithm.data_manager import *
from src.lib.share import *


class Mainsystem:
    def __init__(self):
        self.ui = loadUi(share.MainSyetem_ui)
        self.ui.query.clicked.connect(self.on_query_clicked)

        # Widget and layout
        self.ui.content_widget = QWidget()
        self.ui.scrollArea.setWidget(self.ui.content_widget)

        # ToolBox and layout
        self.ui.tool_box = QToolBox()

        self.layout = QVBoxLayout(self.ui.content_widget)
        self.layout.addWidget(self.ui.tool_box)

    def on_query_clicked(self):

        city_A = self.ui.comboBox_5.currentText()
        city_B = self.ui.comboBox_6.currentText()

        # show()
        self.show(city_A, city_B)

    def delete(self):
        count = self.ui.tool_box.count()
        for i in range(count - 1, -1, -1):  # 从后向前遍历
            self.ui.tool_box.removeItem(i)

    def show(self, city_A, city_B):

        # load flight data
        directory = share.directory
        flight_manager = FlightManager(directory)
        flight_manager.load_flights()

        # num_flights = len(flight_manager.flights[city_A][city_B])
        # print(f"从 {city_A} 到 {city_B} 的航班数量: {num_flights}")

        self.delete()

        self.ui.tool_box.layout().setSpacing(20)  # 设置间距为20像素

        for i, flight in enumerate(flight_manager.flights[city_A][city_B]):
            page = QWidget()
            page_layout = QHBoxLayout()

            # show info
            for key, value in flight.items():

                label = QLabel(f" || {key}: {value} ||")
                # set font
                font = QFont()
                font.setPointSize(12)
                label.setFont(font)
                page_layout.addWidget(label)

            page.setLayout(page_layout)

            font = QFont()
            font.setPointSize(14)

            self.ui.tool_box.setFont(font)
            self.ui.tool_box.addItem(page, f"航班 {i + 1}")

