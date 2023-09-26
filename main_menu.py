import sys
import math
import random

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import statcast_data as st
import game_logic as gl

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = QLabel("Who's Tossing These? - A pitcher guessing game.", self)
        self.start_button = QPushButton("Play", self)
        self.exit_button = QPushButton("X", self)
        self.help_button = QPushButton("?", self)
        self.hs_text_label = QLabel("=====HIGH SCORE=====", self)
        self.hs_score_label = QLabel(self)

        self.format_widgets()
        self.set_signals()
        self.build()

    def format_widgets(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.title.setGeometry(500, 500, 1000, 100)
        self.exit_button.setGeometry(0, 0, 30, 30)
        self.help_button.setGeometry(self.width() - 30, 0, 30, 30)
        self.hs_text_label.setText("00")
        self.hs_text_label.move(int((self.geometry().width() / 2)), 100)
        self.hs_score_label.move(20, 50)

    def build(self):
        self.setWindowTitle("Who's Tossing These? - By Colin Herbert")
        self.showFullScreen()
        print(self.geometry())

    def set_signals(self):
        self.exit_button.clicked.connect(self.exit)
        self.help_button.clicked.connect(self.help)

    def exit(self):
        print("Exit Button Pressed")
        QtCore.QCoreApplication.instance().quit()

    def help(self):
        self.help_window = QWindow()
        self.help_window.show()
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = gl.Game()
    menu = MainMenu()
    sys.exit(app.exec_())



