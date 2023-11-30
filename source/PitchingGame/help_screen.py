from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1000, 1000)
        self.layout = QStackedLayout(self)
        self.about_label = QLabel("About \'Who\'s Tossing These?\'", self)
        self.summary_label = QLabel("'Who's Tossing These?' is a trivia game utilizing pybaseball, a framework that \n"
                                    "scrapes Baseball Reference, Statcast, and Fangraphs data.", self)
        self.how_to_play_label = QLabel("How to Play: ", self)
        self.how_to_play_1 = QLabel("Guess as many pitchers as you can!", self)
        self.how_to_play_2 = QLabel("- You will be presented with a mystery player's pitch arsenal and current team",
                                    self)
        self.how_to_play_3 = QLabel("- You may use any or all of the 4 hints per level,"
                                    " but using hints will make you score less (max 5 points per level)", self)
        self.how_to_play_4 = QLabel("- You get 3 guesses total... 3 strikes and you're out!", self)
        self.how_to_play_5 = QLabel("* Active Players Only (as of the 2023 season) *", self)

        self.exit_button = QPushButton("X", self)
        self.exit_button.clicked.connect(self.exit)

        self.layout.addWidget(self.about_label)
        self.layout.addWidget(self.summary_label)
        self.layout.addWidget(self.how_to_play_label)
        self.set_layouts()

    def set_layouts(self):
        self.about_label.move(0, 100)
        self.summary_label.move(0, 200)
        self.how_to_play_label.move(0, 500)
        self.about_label.adjustSize()
        self.summary_label.adjustSize()
        self.how_to_play_label.adjustSize()
        self.exit_button.setGeometry(0, 0, 30, 30)

    def exit(self):
        self.destroy()
