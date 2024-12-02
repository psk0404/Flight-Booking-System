from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from src.algorithm.data_manager import data_loader
from src.lib.User import share

class changeWindow(QMainWindow):
    def __init__(self, num_flight, idx, parent=None):
        super(changeWindow, self).__init__(parent)
        self.num_flight = num_flight
        self.idx = idx
        self.parent = parent
        self.ui = loadUi(share.change_ui, self)
        self.loader = data_loader(share.directory)
        self.loader.load_flights_info()
        self.setup_user_info()

    def setup_user_info(self):
        flightss = []
        layout = QVBoxLayout()
        widgets_to_remove = []

        for widget in self.ui.scrollArea.widget().findChildren(QWidget):
            widgets_to_remove.append(widget)

        for widget in widgets_to_remove:
            widget.deleteLater()

        for i in range(len(self.num_flight)):
            flight_temp = []
            line_flights = []
            for j in range(len(self.num_flight[i])):
                num0 = self.num_flight[i][j][0]
                num1 = self.num_flight[i][j][1]
                num2 = self.num_flight[i][j][2]
                flight_temp.append(self.loader.get_flight_info_all(num0, num1, num2))
                line_flights.append([num0, num1])
            flightss.append(flight_temp)

        for idx, flights in enumerate(flightss):
            if flights and any(flight is not None for flight in flights):
                widget = QWidget()
                card_layout = QVBoxLayout(widget)

                table = self.create_flight_table(flights)
                card_layout.addWidget(table)

                button_layout = QHBoxLayout()

                change_button = QPushButton("确认改签")
                change_button.clicked.connect(partial(self.change_ticket_group, idx, flights, line_flights))
                button_layout.addWidget(change_button)

                card_layout.addLayout(button_layout)

                layout.addWidget(widget)

        self.ui.scrollArea.widget().setLayout(layout)
        self.ui.scrollArea.setWidgetResizable(True)

    def create_flight_table(self, flights):
        table = QTableWidget(len(flights), 7)
        table.setHorizontalHeaderLabels(
            ["出发时间", "出发机场", "飞行时间", "到达时间", "到达机场", "航班信息", "票价"])

        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 100)
        table.setColumnWidth(2, 120)
        table.setColumnWidth(3, 100)
        table.setColumnWidth(4, 100)
        table.setColumnWidth(5, 120)
        table.setColumnWidth(6, 120)

        table.setFixedHeight(160)

        row_height = 40
        for row, flight in enumerate(flights):
            if flight is None:
                continue

            departure_time, departure_airport, duration, arrival_time, arrival_airport, flight_number, price = flight
            table.setItem(row, 0, QTableWidgetItem(departure_time.strftime('%H:%M')))
            table.setItem(row, 1, QTableWidgetItem(departure_airport))
            table.setItem(row, 2, QTableWidgetItem(duration))
            table.setItem(row, 3, QTableWidgetItem(arrival_time.strftime('%H:%M')))
            table.setItem(row, 4, QTableWidgetItem(arrival_airport))
            table.setItem(row, 5, QTableWidgetItem(flight_number))
            table.setItem(row, 6, QTableWidgetItem(f"¥{price}"))

            table.setRowHeight(row, row_height)

        return table

    def change_ticket_group(self, idx, flights, line_flights):
        share.user_flights[self.idx] = flights
        share.line_flights[self.idx] = line_flights
        if self.parent:
            self.parent.update_flight_info(self.idx, flights)

        QMessageBox.information(self, "改签成功", f"已改签 {idx + 1} 航班！")