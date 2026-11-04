import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QPlainTextEdit, QRadioButton, QLineEdit
from PyQt6.QtWidgets import QLabel, QTextEdit
from PyQt6.QtCore import Qt
import datetime as dt


class WPS_test(QWidget):
    def __init__(self):
        super().__init__()
        self.line1 = "abciiim "
        self.line2 = "abcmiii "
        self.line3 = "defghkl "
        self.line4 = "jmnopqrs "
        self.line5 = "tuvwxyz"
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('WPS test')

        self.testbtn = QPushButton('Новый тест', self)
        self.testbtn.setGeometry(75, 150, 150, 30)
        self.testbtn.clicked.connect(self.newTest)

        self.text = QTextEdit(self)
        self.text.setGeometry(50, 160, 300, 190)
        self.text.setReadOnly(True)

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

        self.lab1 = QLabel("", self)
        self.lab1.setGeometry(52, 159, 300, 20)
        self.lab1.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.lab2 = QLabel(self.line1, self)
        self.lab2.setGeometry(52, 175, 300, 20)
        self.lab2.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.lab3 = QLabel(self.line2, self)
        self.lab3.setGeometry(52, 191, 300, 20)
        self.lab3.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.acclab = QLabel("Точность: 0%", self)
        self.acclab.setGeometry(20, 135, 200, 20)

        self.labs = []  
        self.started = False
        self.time = 10

        self.text.hide()
        self.btn.hide()
        self.s10.hide()
        self.s15.hide()
        self.s20.hide()
        self.cust.hide()
        self.lab.hide()
        self.timeed.hide()
        self.lab1.hide()
        self.lab2.hide()
        self.lab3.hide()
        self.acclab.hide()
        self.flag = False


    def newTest(self):
        self.lang, ok_pressed = QInputDialog.getItem(self, "Название", "Выберите язык", ["Русский", "English"], editable=False)
        if ok_pressed:
            self.draw_test()

    def draw_menu(self):
        self.testbtn.show()

    def draw_test(self):
        self.acclab.show()
        self.testbtn.hide()
        self.text.show()
        self.btn.show()
        self.s10.show()
        self.s15.show()
        self.s20.show()
        self.cust.show()
        self.lab.show()
        self.resize(400, 400)

    def start(self):
        self.starttime = dt.datetime.now()
        self.started = True
        self.lab1.show()
        self.lab2.show()
        self.lab3.show()
        self.alllets = 0
        self.corrlets = 0
        self.accuracy = 0
        self.flag = True

    def keyPressEvent(self, event):
        if not self.flag:
            return
        
        if (dt.datetime.now() - self.starttime).seconds >= (dt.datetime.strptime(str(self.time), "%S")).second:
            self.endtest()
            return

        if not self.started:
            return
        self.let = event.text()
        if event.key() == Qt.Key.Key_Backspace:
            if self.labs:
                if self.labs[-1] == self.lab2.text()[len(self.labs)]:
                    pass
                self.corrlets -= 1
                self.alllets -= 1

                self.labs[-1].hide()
                self.labs.remove(self.labs[-1])
                if self.alllets != 0:
                    self.accuracy = round(self.corrlets / self.alllets * 100, 1)
                    self.acclab.setText(f"Точность: {self.accuracy}%")
            return
        if event.key() == Qt.Key.Key_Shift:
            return
        self.new = QLabel(self.let, self)
        self.new.setGeometry(52 + 7 * len(self.labs), 175, 7, 20) 
        self.alllets += 1
        if self.let == self.lab2.text()[len(self.labs)]:
            self.new.setStyleSheet("""font-family: "Courier New", monospace; color: 'green'; background-color: 'white';""")
            self.corrlets += 1
        else:
            self.new.setStyleSheet("""font-family: "Courier New", monospace; color: 'red'; background-color: 'white';""")
        self.new.show()
        self.labs.append(self.new)
        if self.alllets != 0:
            self.accuracy = round(self.corrlets / self.alllets * 100, 1)
            self.acclab.setText(f"Точность: {self.accuracy}%")
        

        if len(self.labs) == len(self.lab2.text()[:-1]):
            next = self.line4
            self.lab1.setText(self.lab2.text())
            self.lab2.setText(self.lab3.text())
            self.lab3.setText(next)
            self.text.setPlainText("")
            self.labs2 = self.labs.copy()
            for i in range(len(self.labs2)):
                self.labs2[i].setGeometry(52 + 7 * i, 159, 7, 20)
            for el in self.labs:
                el.hide()
            self.labs = []

    def endtest(self):
        self.flag = False
        pass

    def getTime(self):
        if "10 секунд" in self.sender().text():
            self.time = 10
            self.timeed.hide()
        elif "15 секунд" in self.sender().text():
            self.time = 15
            self.timeed.hide()
        elif "20 секунд" in self.sender().text():
            self.time = 20
            self.timeed.hide()
        elif "Своё время" == self.sender().text():
            self.timeed.show()
            self.time = self.timeed.text()
        else:
            self.time = self.timeed.text()


class EndTest(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('Конец теста')

        self.lab = QLabel(f"Конец теста, результаты:")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WPS_test()
    ex.show()
    sys.exit(app.exec())
