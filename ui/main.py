from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from typing import Text
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QApplication, QLabel, QWidget, QComboBox, QTextEdit, QLineEdit
import sys

from main_window import Ui_MainWindow


class CargoWingsApp(QMainWindow, QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationDisplayName("Cargo Wings")

    MainWindow = CargoWingsApp()

    MainWindow.show()

    sys.exit(app.exec_())