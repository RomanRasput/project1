from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtWidgets import QLabel
import datetime as dt
import sqlite3


class EndTest(QWidget):
    def __init__(self, all, corr, t, words):
        super().__init__()
        self.all = all
        self.corr = corr
        self.t = t
        self.words = words
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 260, 300)
        self.setWindowTitle('Конец теста')

        if self.all == 0:
            self.acc = 0
        else:
            self.acc = round(self.corr / self.all * 100, 2)
        self.wpm = self.words * 60 / int(self.t)

        self.lab = QLabel(f"Время кончилось! Результат:", self)
        self.lab.setGeometry(50, 10, 160, 20)

        self.wpmlab = QLabel(f"Слов в минуту - {round(self.wpm, 2)}", self)
        self.wpmlab.setGeometry(50, 40, 200, 20)

        self.savebtn = QPushButton("Сохранить результат", self)
        self.savebtn.setGeometry(130, 270, 125, 25)
        self.savebtn.clicked.connect(self.save)

        self.Nsavebtn = QPushButton("Не сохранять", self)
        self.Nsavebtn.setGeometry(5, 270, 125, 25)
        self.Nsavebtn.clicked.connect(self.close)

    def save(self):
        con = sqlite3.connect(r"sqlite\results.sqlite")
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS results (
            all_letters INTEGER NOT NULL,
            correct_letters INTEGER NOT NULL,
            time INTEGER NOT NULL,
            accuracy NOT NULL,
            words INTEGER NOT NULL,
            WPM NOT NULL,
            date NOT NULL
        );""").fetchall()

        cur.execute("""INSERT INTO results(all_letters, correct_letters, time, accuracy, words, WPM, date) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (self.all, self.corr, self.t, self.acc, self.words, self.wpm, dt.datetime.strftime(dt.datetime.now(), "%d.%m %H:%M"))).fetchall()
        con.commit()
        con.close()
        self.close()