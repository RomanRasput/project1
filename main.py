import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QTextBrowser, QRadioButton, QLineEdit
from PyQt6.QtWidgets import QLabel
import time


class WPS_test(QWidget):
    def __init__(self):
        super().__init__()
        self.line1 = "1 2 3 4 5"
        self.line2 = "6 7 8 9 10"
        self.line3 = "11 12 13 14 15"
        self.line4 = "16 17 18 19 20"
        self.line5 = "21 22 23 24 25"
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('WPS test')

        self.trick_button = QPushButton('Новый тест', self)
        self.trick_button.setGeometry(75, 150, 150, 30)
        self.trick_button.clicked.connect(self.new)

        self.text = QTextBrowser(self)
        self.text.setGeometry(50, 140, 300, 190)

        self.btn = QPushButton("Начать", self)
        self.btn.setGeometry(100, 100, 200, 30)
        self.btn.clicked.connect(self.start)

        self.lab = QLabel("Выберите время", self)
        self.lab.setGeometry(10, 10, 380, 20)

        self.s10 = QRadioButton("10 секунд", self)
        self.s10.move(10, 40)
        self.s10.toggle()
        self.s10.clicked.connect(self.getTime)

        self.s15 = QRadioButton("15 секунд", self)
        self.s15.move(105, 40)
        self.s15.clicked.connect(self.getTime)

        self.s20 = QRadioButton("20 секунд", self)
        self.s20.move(210, 40)
        self.s20.clicked.connect(self.getTime)

        self.cust = QRadioButton("Своё время", self)
        self.cust.move(310, 40)
        self.cust.clicked.connect(self.getTime)

        self.timeed = QLineEdit("10", self)
        self.timeed.setGeometry(310, 60, 50, 20)
        self.timeed.textChanged.connect(self.getTime)

        self.text.hide()
        self.btn.hide()
        self.s10.hide()
        self.s15.hide()
        self.s20.hide()
        self.cust.hide()
        self.lab.hide()
        self.timeed.hide()

    def new(self):
        self.lang, ok_pressed = QInputDialog.getItem(self, "Название", "Язык?", ["Русский", "English"], editable=False)
        print(self.lang)
        print(ok_pressed)
        if ok_pressed:
            self.draw_test()

    def draw_menu(self):
        self.trick_button.show()

    def draw_test(self):
        self.trick_button.hide()
        self.text.show()
        self.btn.show()
        self.s10.show()
        self.s15.show()
        self.s20.show()
        self.cust.show()
        self.lab.show()
        self.resize(400, 400)

    def start(self):
        pass

    def getTime(self):
        if "10 секунд" in self.sender().text():
            self.time = 10
            self.timeed.hide()
        elif "15" in self.sender().text():
            self.time = 15
            self.timeed.hide()
        elif "20" in self.sender().text():
            self.time = 20
            self.timeed.hide()
        elif "Своё время" == self.sender().text():
            self.timeed.show()
            self.time = self.timeed.text()
        else:
            self.time = self.timeed.text()
        print(self.time)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WPS_test()
    ex.show()
    sys.exit(app.exec())
