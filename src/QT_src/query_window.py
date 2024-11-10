from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from src.lib.share import share

class QueryWindow(QMainWindow):
    def __init__(self):
        super(QueryWindow, self).__init__()
        self.ui = loadUi(share.querywindow_ui, self)  # 加载查询UI文件

        # 城市名称到编号的映射
        self.city_mapping = {
            "巴黎": 1,
            "柏林": 2,
            "北京": 3,
            "成都": 4,
            "长春": 5,
            "东京": 6,
            "洛杉矶": 7,
            "曼谷": 8,
            "南京": 9,
            "厦门": 10,
            "上海": 11,
            "深圳": 12,
            "首尔": 13,
            "乌鲁木齐": 14,
            "武汉": 15,
            "西安": 16
        }

        # 连接查询按钮事件
        self.ui.pushButton.clicked.connect(self.onQuery)

    def onQuery(self):
        from_city = self.ui.fromcity.currentText().strip()
        to_city = self.ui.tocity.currentText().strip()

        # 获取城市编号
        from_city_num = self.city_mapping.get(from_city)
        to_city_num = self.city_mapping.get(to_city)

        if from_city_num is None or to_city_num is None:
            # 如果城市编号为空，弹出提示框
            QMessageBox.warning(self, "未找到航班", "抱歉！未找到该组航班，请检查城市选择。")
            return

        # 将城市名称传递给 Mainsystem
        from_city_name = from_city
        to_city_name = to_city

        # 如果选择有效的城市，执行查询操作
        from src.QT_src.main_system import Mainsystem  # 动态导入以避免循环导入
        share.mainWin = Mainsystem(from_city_num, to_city_num, from_city_name, to_city_name)  # 创建主页面窗口实例
        share.mainWin.show()  # 显示主页面
        self.close()  # 关闭查询窗口


# 用于独立测试时运行
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5 import QtCore
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = QueryWindow()
    window.show()
    sys.exit(app.exec_())