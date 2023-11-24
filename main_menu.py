import sys
import math
import random

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import game_logic
import statcast_data as st
import help_screen as hs
import game_logic as gl
import game_ui as gu


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = QLabel("Who's Tossing These? - A pitcher guessing game.", self)
        self.start_button = QPushButton("Play", self)
        self.exit_button = QPushButton("X", self)
        self.help_button = QPushButton("?", self)
        self.update_data_button = QPushButton("Update Player Database", self)
        self.hs_text_label = QLabel("=====HIGH SCORE=====", self)
        self.hs_score_label = QLabel(self)

        self.help_window = None
        self.game_ui = gu.GameUI()

        self.format_widgets()
        self.set_signals()
        self.build()

    def format_widgets(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.title.adjustSize()
        self.start_button.setGeometry(100, 100, 50, 30)
        self.exit_button.setGeometry(0, 0, 30, 30)
        self.help_button.setGeometry(self.width() - 30, 0, 30, 30)
        self.update_data_button.setGeometry(self.width() - 1000, 1000, 100, 100)
        self.hs_text_label.adjustSize()
        self.hs_score_label.setText("00")
        self.hs_text_label.move(int((self.geometry().width() / 2)), 100)
        self.hs_score_label.move(20, 50)

    def build(self):
        self.setWindowTitle("Who's Tossing These? - By Colin Herbert")
        self.showFullScreen()
        print(self.geometry())

    def set_signals(self):
        self.start_button.clicked.connect(self.start)
        self.exit_button.clicked.connect(self.exit)
        self.help_button.clicked.connect(self.help)
        self.update_data_button.clicked.connect(self.update_db)

    def exit(self):
        print("Exit Button Pressed")
        self.destroy()
        app.quit()

    def help(self):
        self.help_window = hs.HelpWindow()
        self.help_window.show()

    def update_db(self):
        self.game_ui.game.stats.update_pitcher_db()

    def start(self):
        self.game_ui.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    sys.exit(app.exec_())


