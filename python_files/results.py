import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QRadioButton, QLineEdit
from PyQt6.QtWidgets import QLabel, QTextEdit, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import datetime as dt
import sqlite3
import random
import pymorphy3


class Results(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Результаты')

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 70, 430, 270)

        self.lab = QLabel("Ваши результаты тестов:", self)
        self.lab.setGeometry(10, 50, 200, 20)

        self.updbtn = QPushButton(self)
        self.updbtn.setGeometry(10, 70, 15, 15)
        self.updbtn.clicked.connect(self.upd)

        self.upd()

    def upd(self):
        con = sqlite3.connect(r"sqlite\results.sqlite")
        cur = con.cursor()
        self.lst = []
        self.lst = cur.execute("""SELECT * FROM results""").fetchall()
        con.close()

        self.table.setColumnCount(7)
        self.table.setRowCount(len(self.lst))
        for y in range(7):
            for x in range(len(self.lst)):
                self.table.setItem(
                    x, y, QTableWidgetItem(str(self.lst[x - 1][y])))

        self.table.setHorizontalHeaderLabels(["Все\nбуквы", "Правильно\nнаписанные\nбуквы",
                                             "Время\nтеста", "Точность", "Написано\nслов", "Слов в\nминуту", "Дата\nтеста"])
        self.table.resizeColumnsToContents()