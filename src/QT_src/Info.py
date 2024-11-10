# src/QT_src/Info.py
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QHBoxLayout, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from boltons.funcutils import partial
from src.lib.share import *  # 假设这里导入了需要的共享数据

class userInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi(share.UserInfo_ui, self)
        self.setup_user_info()

    def setup_user_info(self):
        layout = QVBoxLayout()
        widgets_to_remove = []  # 用于存储要删除的widget

        for widget in self.ui.scrollArea.widget().findChildren(QWidget):
            widgets_to_remove.append(widget)

        # 清空现有界面中的所有小部件（避免重复添加）
        for widget in widgets_to_remove:
            widget.deleteLater()

        # 重新生成界面
        for idx, flights in enumerate(share.user_flights):
            if flights and any(flight is not None for flight in flights):  # 只展示非空的航班信息
                widget = QWidget()
                card_layout = QVBoxLayout(widget)
                info_layout = QHBoxLayout()
                table = self.create_flight_table(flights, idx)  # 增加索引参数
                info_layout.addWidget(table)
                card_layout.addLayout(info_layout)
                layout.addWidget(widget)

        self.ui.scrollArea.widget().setLayout(layout)
        self.ui.scrollArea.setWidgetResizable(True)

    def create_flight_table(self, flights, user_idx):
        table = QTableWidget(len(flights), 9)  # 添加一列用于显示信息编号，总共9列
        table.setHorizontalHeaderLabels(
            ["信息编号", "出发时间", "出发机场", "飞行时间", "到达时间", "到达机场", "航班信息", "票价", "操作"])

        # 设置每列的宽度
        table.setColumnWidth(0, 100)  # 信息编号列宽度
        table.setColumnWidth(1, 100)  # 出发时间列宽度
        table.setColumnWidth(2, 120)  # 出发机场列宽度
        table.setColumnWidth(3, 100)  # 飞行时间列宽度
        table.setColumnWidth(4, 100)  # 到达时间列宽度
        table.setColumnWidth(5, 120)  # 到达机场列宽度
        table.setColumnWidth(6, 120)  # 航班号列宽度
        table.setColumnWidth(7, 80)   # 票价列宽度
        table.setColumnWidth(8, 100)  # 操作列宽度

        table.setFixedHeight(160)

        # 设置每一行的固定高度
        row_height = 40
        for row, flight in enumerate(flights):
            if flight is None:  # 如果航班已经被清空，跳过该行
                continue

            departure_time, departure_airport, duration, arrival_time, arrival_airport, flight_number, price = flight
            table.setItem(row, 0, QTableWidgetItem(f"0000{random.randint(0, 9999):04d}"))  # 设置信息编号
            table.setItem(row, 1, QTableWidgetItem(departure_time.strftime('%H:%M')))
            table.setItem(row, 2, QTableWidgetItem(departure_airport))
            table.setItem(row, 3, QTableWidgetItem(duration))
            table.setItem(row, 4, QTableWidgetItem(arrival_time.strftime('%H:%M')))
            table.setItem(row, 5, QTableWidgetItem(arrival_airport))
            table.setItem(row, 6, QTableWidgetItem(flight_number))
            table.setItem(row, 7, QTableWidgetItem(f"¥{price}"))

            # 在最后一列插入退票按钮
            refund_button = QPushButton("退票")
            refund_button.clicked.connect(partial(self.refund_ticket, user_idx, row, table))  # 连接退票事件
            table.setCellWidget(row, 8, refund_button)

            table.setRowHeight(row, row_height)  # 设置每行的高度为40像素

        return table

    def refund_ticket(self, user_idx, flight_idx, table):
        # 清空该行的航班信息
        share.user_flights[user_idx][flight_idx] = None

        # 刷新表格: 如果某一行被清空，跳过该行
        for row in range(table.rowCount()):
            if share.user_flights[user_idx][row] is None:  # 如果该行航班已清空，隐藏这一行
                table.setRowHidden(row, True)
            else:
                table.setRowHidden(row, False)

        # 如果表格中所有的航班都已清空，删除该航班卡片
        if all(flight is None for flight in share.user_flights[user_idx]):
            parent_widget = table.parentWidget()
            parent_widget.deleteLater()  # 删除整个卡片widget

        # 显示退票成功提示
        QMessageBox.information(self, "退票成功", "退票成功！")
        self.close()  # 关闭页面


if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = userInfo()
    window.show()
    sys.exit(app.exec_())