import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QRadioButton, QLineEdit
from PyQt6.QtWidgets import QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import datetime as dt
import sqlite3
import random
import pymorphy3
from classes.results import Results
from classes.endTest import EndTest


class WPM_test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('WPM test')

        self.testbtn = QPushButton('Новый тест', self)
        self.testbtn.setGeometry(75, 150, 150, 30)
        self.testbtn.clicked.connect(self.newTest)

        self.resbtn = QPushButton('Результаты', self)
        self.resbtn.setGeometry(75, 200, 150, 30)
        self.resbtn.clicked.connect(self.results)

        self.menubtn = QPushButton('Верну-\nться', self)
        self.menubtn.setGeometry(2, 2, 50, 50)
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

        self.lab2 = QLabel("", self)
        self.lab2.setGeometry(52, 199, 300, 20)
        self.lab2.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.lab3 = QLabel("", self)
        self.lab3.setGeometry(52, 215, 300, 20)
        self.lab3.setStyleSheet("""font-family: "Courier New", monospace;""")

        self.acclab = QLabel("Точность: 0%", self)
        self.acclab.setGeometry(20, 175, 200, 20)

        self.erlab = QLabel("", self)
        self.erlab.setGeometry(200, 120, 200, 20)

        self.pick1 = QPixmap(r'pictures\gentleman.png').scaled(150, 150)
        self.im1 = QLabel(self)
        self.im1.move(250, 250)
        self.im1.setPixmap(self.pick1)

        self.pick2 = QPixmap(r'pictures\lady.png').scaled(90, 160)
        self.im2 = QLabel(self)
        self.im2.move(10, 10)
        self.im2.setPixmap(self.pick2)

        self.namelab1 = QLabel("Тест На Скорость Печати", self)
        self.namelab1.setGeometry(120, 30, 300, 60)
        self.namelab1.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.namelab2 = QLabel("Проверь свою скорость печати\nменьше чем за минуту", self)
        self.namelab2.setGeometry(120, 70, 200, 40)

        self.labs = []
        self.started = False
        self.time = 10
        self.lang = "English"

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

        self.testbtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.resbtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.menubtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.s10.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.s15.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.s20.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cust.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.text.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def newTest(self):
        self.lang, ok_pressed = QInputDialog.getItem(self, "Название", "Выберите язык", [
                                                     "Русский", "English"], editable=False)
        if ok_pressed:
            self.draw_test()

    def draw_menu(self):
        self.acclab.hide()
        self.testbtn.show()
        self.resbtn.show()
        self.namelab1.show()
        self.namelab2.show()
        self.im1.show()
        self.im2.show()
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
        self.timeed.hide()
        self.s10.toggle()
        for el in self.labs:
            el.hide()
        self.labs = []
        self.menubtn.hide()

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
        self.acclab.setText("Точность: 0%")
        self.lab1.hide()
        self.lab2.hide()
        self.lab3.hide()
        self.namelab1.hide()
        self.namelab2.hide()
        self.im1.hide()
        self.im2.hide()

    def start(self):
        self.started = True
        self.lab1.show()
        self.lab2.show()
        self.lab3.show()
        self.alllets = 0
        self.corrlets = 0
        self.accuracy = 0
        self.flag = True
        self.flag2 = True
        self.words = 0
        self.lab1.setText("")
        self.lab2.setText(self.LineGenerator())
        self.lab3.setText(self.LineGenerator())
        self.setFocus()

    def results(self):
        self.resmenu = Results()
        self.resmenu.show()

    def keyPressEvent(self, event):
        if not self.flag:
            return

        if self.flag2:
            self.starttime = dt.datetime.now()
            self.flag2 = False

        if (dt.datetime.now() - self.starttime).seconds >= int(self.time):
            self.endtest()
            return

        if not self.started:
            return
        self.let = event.text()

        if event.key() == Qt.Key.Key_Backspace:
            if self.labs:
                if "'green'" in self.labs[-1].styleSheet():
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

        if event.key() == Qt.Key.Key_Space:
            if len(self.labs) == 0:
                return
            if self.let == self.lab2.text()[len(self.labs)]:
                self.words += 1

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
            self.words += 1
            next = self.LineGenerator()
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
        self.second = EndTest(self.alllets, self.corrlets,
                              self.time, self.words)
        self.second.show()
        self.second.lab.show()
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
        else:
            self.timeed.show()
            self.time = self.timeed.text()
            if not self.timeed.text().isdigit():
                self.erlab.setText("Пожалуйста, введите целое число")
            else:
                self.erlab.setText("")

    def resizeEvent(self, event):
        new_size = event.size()
        w = new_size.width()
        h = new_size.height()
        add = int(h / 10)

        btn_w = int(w / 2)
        btn_h = int(h / 13.33)
        btn_x = int(w / 4)
        btn_y = int(h / 2.666)

        self.testbtn.setGeometry(btn_x, btn_y, btn_w, btn_h)
        self.resbtn.setGeometry(btn_x, btn_y + btn_h + 20, btn_w, btn_h)

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
        self.menubtn.setGeometry(
            int(w / 200), int(h / 200), int(w / 8), int(h / 8))
        for i in range(len(self.labs)):
            self.labs[i].setGeometry(
                int((52 * w / 400 + 7 * i)), int(h / 1.86), int(w / 57.14), int(h / 20))

    def LineGenerator(self):
        p, s, op, ob = [], [], [], []

        con = sqlite3.connect(r"sqlite\words.sqlite")
        cur = con.cursor()
        words = cur.execute("""SELECT * FROM words""").fetchall()
        con.close()
        if self.lang == "English":
            for el in words:
                if el[-1] == "П" and el[1] == "EN":
                    p.append(el[0])
                elif el[-1] == "С" and el[1] == "EN":
                    s.append(el[0])
                elif el[-1] == "Оп" and el[1] == "EN":
                    op.append(el[0])
                elif el[-1] == "Об" and el[1] == "EN":
                    ob.append(el[0])

            line = random.choice(op) + " " + random.choice(p) + " " + random.choice(
                ob) + " " + random.choice(s) + " " + random.choice(op) + " " + random.choice(p)
            return line + ' '
        
        p, s, op, ob = [], [], [], []
        for el in words:
            if el[-1] == "П" and el[1] == "RU":
                p.append(el[0])
            elif el[-1] == "С" and el[1] == "RU":
                s.append(el[0])
            elif el[-1] == "Оп" and el[1] == "RU":
                op.append(el[0])
            elif el[-1] == "Об" and el[1] == "RU":
                ob.append(el[0])

        obst = random.choice(ob)
        if len(obst.split()) == 1:
            line = random.choice(op) + " " + random.choice(p) + \
                " " + obst + " " + random.choice(s)
        else:
            line = random.choice(op) + " " + random.choice(p) + \
                " " + random.choice(s) + " " + obst

        morph = pymorphy3.MorphAnalyzer()
        words1 = line.split()
        gramms = set()
        for w in words1:
            parsed = morph.parse(w)[0]
            if 'NOUN' in parsed.tag:
                for g in ('masc', 'femn', 'neut', 'plur', 'sing',
                          'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct'):
                    if g in parsed.tag:
                        gramms.add(g)
                break
        result = []
        for w in words1:
            parsed = morph.parse(w)[0]
            if 'ADJF' in parsed.tag or 'ADJS' in parsed.tag:
                target = {g for g in gramms
                          if g in ('masc', 'femn', 'neut', 'plur', 'sing',
                                   'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct')}
                inflected = parsed.inflect(target) if target else parsed
                result.append(inflected.word if inflected else w)
                continue
            if 'INFN' in parsed.tag or 'VERB' in parsed.tag:
                if 'plur' in gramms:
                    target = {'pres', 'plur', '3per'}
                else:
                    target = {'pres', 'sing', '3per'}
                inflected = parsed.inflect(target)
                if not inflected:
                    inflected = parsed.inflect({'futr', 'sing', '3per'})
                result.append(inflected.word if inflected else w)
                continue
            result.append(w)

        return " ".join(result) + " "

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 
            'Подтверждение', 
            'Вы уверены, что хотите закрыть приложение?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        if reply == 16384:
            self.close()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WPM_test()
    ex.show()
    sys.exit(app.exec())
