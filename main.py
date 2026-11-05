import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QRadioButton, QLineEdit
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

        self.resbtn = QPushButton('Результаты', self)
        self.resbtn.setGeometry(75, 200, 150, 30)
        self.resbtn.clicked.connect(self.results)

        self.menubtn = QPushButton('Верну-\nться', self)
        self.menubtn.setGeometry(2, 2, 50, 50)
        self.menubtn.clicked.connect(self.results)
        self.menubtn.clicked.connect(self.draw_menu)

        self.text = QTextEdit(self)
        self.text.setGeometry(50, 200, 300, 190)
        self.text.setReadOnly(True)

        self.btn = QPushButton("Начать", self)
        self.btn.setGeometry(100, 140, 200, 30)
        self.btn.clicked.connect(self.start)

        self.lab = QLabel("Выберите время", self)
        self.lab.setGeometry(10, 50, 380, 20)

        self.s10 = QRadioButton("10 секунд", self)
        self.s10.move(10, 80)
        self.s10.toggle()
        self.s10.clicked.connect(self.getTime)

        self.s15 = QRadioButton("15 секунд", self)
        self.s15.move(105, 80)
        self.s15.clicked.connect(self.getTime)

        self.s20 = QRadioButton("20 секунд", self)
        self.s20.move(210, 80)
        self.s20.clicked.connect(self.getTime)

        self.cust = QRadioButton("Своё время", self)
        self.cust.move(310, 80)
        self.cust.clicked.connect(self.getTime)

        self.timeed = QLineEdit("10", self)
        self.timeed.setGeometry(310, 100, 50, 20)
        self.timeed.textChanged.connect(self.getTime)

        self.lab1 = QLabel("", self)
        self.lab1.setGeometry(52, 183, 300, 20)
        self.lab1.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.lab2 = QLabel(self.line1, self)
        self.lab2.setGeometry(52, 199, 300, 20)
        self.lab2.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.lab3 = QLabel(self.line2, self)
        self.lab3.setGeometry(52, 215, 300, 20)
        self.lab3.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.acclab = QLabel("Точность: 0%", self)
        self.acclab.setGeometry(20, 175, 200, 20)

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
        self.menubtn.hide()
        self.flag = False

    def newTest(self):
        self.lang, ok_pressed = QInputDialog.getItem(self, "Название", "Выберите язык", [
                                                     "Русский", "English"], editable=False)
        if ok_pressed:
            self.draw_test()

    def draw_menu(self):
        self.acclab.hide()
        self.testbtn.show()
        self.resbtn.show()
        self.text.hide()
        self.btn.hide()
        self.s10.hide()
        self.s15.hide()
        self.s20.hide()
        self.cust.hide()
        self.lab.hide()
        self.lab1.hide()
        self.lab2.hide()
        self.lab3.hide()
        for el in self.labs:
            el.hide()
        self.labs = []
        self.menubtn.hide()
        self.resize(300, 400)

    def draw_test(self):
        self.acclab.show()
        self.testbtn.hide()
        self.resbtn.hide()
        self.text.show()
        self.btn.show()
        self.s10.show()
        self.s15.show()
        self.s20.show()
        self.cust.show()
        self.lab.show()
        self.menubtn.show()
        for el in self.labs:
            el.hide()
        self.labs = []
        self.resize(400, 400)
        self.acclab.setText("Точность: 0%")
        self.lab1.hide()
        self.lab2.hide()
        self.lab3.hide()

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

    def results(self):
        pass

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
                    self.accuracy = round(
                        self.corrlets / self.alllets * 100, 1)
                    self.acclab.setText(f"Точность: {self.accuracy}%")
            return
        if event.key() == Qt.Key.Key_Shift:
            return
        self.new = QLabel(self.let, self)
        self.new.setGeometry(52 + 7 * len(self.labs), 215, 7, 20)
        self.alllets += 1
        if self.let == self.lab2.text()[len(self.labs)]:
            self.new.setStyleSheet(
                """font-family: "Courier New", monospace; color: 'green'; background-color: 'white';""")
            self.corrlets += 1
        else:
            self.new.setStyleSheet(
                """font-family: "Courier New", monospace; color: 'red'; background-color: 'white';""")
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
                self.labs2[i].setGeometry(52 + 7 * i, 199, 7, 20)
            for el in self.labs:
                el.hide()
            self.labs = []

        w = self.width()
        h = self.height()
        for i in range(len(self.labs)):
            self.labs[i].setGeometry(
                int((52 + 7 * i) * w / 400), int(h / 1.86), int(w / 57.14), int(h / 20))

    def endtest(self):
        self.flag = False
        self.second = EndTest(self.alllets, self.corrlets, self.time)
        self.second.show()
        if self.second.closeEvent:
            self.draw_test()

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

    def resizeEvent(self, event):
        new_size = event.size()
        w = new_size.width()
        h = new_size.height()

        add = int(h / 10)

        self.testbtn.setGeometry(
            int(w / 4), int(h / 2.666), int(w / 2), int(h / 13.33))
        self.text.setGeometry(int(w / 8), int(h / 2.5) +
                              add, int(w / 1.3), int(h / 2.1))
        self.btn.setGeometry(int(w / 4), int(h / 4) + add,
                             int(w / 2), int(h / 13.33))
        self.lab.setGeometry(int(w / 40), int(h / 40) +
                             add, int(w / 1.05), int(h / 20))
        self.s10.move(int(w / 40), int(h / 10) + add)
        self.s15.move(int(w / 3.8), int(h / 10) + add)
        self.s20.move(int(w / 1.9), int(h / 10) + add)
        self.cust.move(int(w / 1.29), int(h / 10) + add)
        self.timeed.setGeometry(
            int(w / 1.21), int(h / 6.66) + add, int(w / 8), int(h / 20))
        self.lab1.setGeometry(
            int(w / 7.69), int(h / 2.51) - 15 + add, int(w / 1.3), int(h / 8))
        self.lab2.setGeometry(
            int(w / 7.69), int(h / 2.28) - 15 + add, int(w / 1.3), int(h / 8))
        self.lab3.setGeometry(
            int(w / 7.69), int(h / 2.09) - 15 + add, int(w / 1.3), int(h / 8))
        self.acclab.setGeometry(
            int(w / 20), int(h / 3.2) + add, int(w / 2), int(h / 8))
        for i in range(len(self.labs)):
            self.labs[i].setGeometry(
                int((52 * w / 400 + 7 * i)), int(h / 1.86), int(w / 57.14), int(h / 20))


class EndTest(QWidget):
    def __init__(self, all, corr, t):
        super().__init__()
        self.all = all
        self.corr = corr
        self.t = t
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 260, 300)
        self.setWindowTitle('Конец теста')

        self.lab = QLabel(f"Конец теста, результаты:")
        self.lab.setGeometry(100, 10, 160, 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WPS_test()
    ex.show()
    sys.exit(app.exec())
