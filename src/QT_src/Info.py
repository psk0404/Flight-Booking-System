# src/QT_src/user_info.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from src.lib.share import *

class userInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi(share.UserInfo_ui, self)
        self.setup_user_info()

    def setup_user_info(self):
        layout = QVBoxLayout()
        for flights in share.user_flights:
            label = QLabel(self.format_flight_info(flights))
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setWordWrap(True)
            layout.addWidget(label)
        self.ui.scrollArea.widget().setLayout(layout)
        self.ui.scrollArea.setWidgetResizable(True)

    def format_flight_info(self, flights):
        flight_info = ""
        for flight in flights:
            departure_time, departure_airport, duration, arrival_time, arrival_airport, flight_number, price = flight
            flight_info += f"出发时间: {departure_time.strftime('%H:%M')}, 到达时间: {arrival_time.strftime('%H:%M')}, 票价: ¥{price}\n"
        return flight_info

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = userInfo()
    window.show()
    sys.exit(app.exec_())