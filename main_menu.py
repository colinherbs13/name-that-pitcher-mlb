import sys
import math
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import statcast_data as st


class MainMenu:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()

        self.title = QLabel(self.window)
        #self.start_button = QPushButton(self.window)
        self.exit_button = QPushButton(self.window)
        self.help_button = QPushButton(self.window)
        self.hs_text_label = QLabel(self.window)
        self.hs_score_label = QLabel(self.window)

        self.format_widgets()
        self.build()

    def format_widgets(self):
        self.exit_button.setGeometry(0, 0, 30, 30)
        self.exit_button.setText("X")
        self.help_button.setGeometry(self.window.width() - 30, 0, 30, 30)
        self.help_button.setText("?")
        self.hs_text_label.setText("00")
        self.hs_score_label.setText("=====HIGH SCORE=====")
        self.hs_text_label.move(int((self.window.width() / 2) - (self.hs_text_label.width() / 2)), 100)
        self.hs_score_label.move(20, 50)
        return

    def build(self):
        self.window.setGeometry(100, 100, 400, 200)
        self.window.setWindowTitle("Name That Pitcher - By Colin Herbert")
        self.window.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    stats = st.Statcast()
    index = random.randint(0, len(stats.pitchers))
    stats.pitchers[index].set_pitch_arsenal()
    print(stats.pitchers[index])
    menu = MainMenu()

