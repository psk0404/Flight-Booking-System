from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.uic import loadUi
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\QT\web.ui", self)  # 加载 .ui 文件

        # 获取 QWebEngineView 控件
        self.webView = self.findChild(QWebEngineView, "widget")  # "widget" 是你在 .ui 文件中为 QWebEngineView 控件设置的对象名称

        # 确保文件路径正确，使用 os.path 来构建绝对路径
        file_path = os.path.abspath(r"C:\Users\Lenovo\PycharmProjects\BJUT_dsc\src\traval\index.html")

        # 设置本地文件 URL
        self.webView.setUrl(QUrl.fromLocalFile(file_path))

if __name__ == "__main__":
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())