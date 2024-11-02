from PyQt5.uic import loadUi

from src.lib.share import *
from main_system import *


class QueryWindow():
    def __init__(self):
        self.ui = loadUi(share.querywindow_ui)
