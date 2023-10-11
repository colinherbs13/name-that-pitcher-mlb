from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import game_logic as gl
import help_screen as hs

class GameUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.game = gl.Game()
        self.game.new_game()
        self.game.new_level()

        self.user_input = QLineEdit(self)
        self.score_label = QLabel("Score", self)
        self.highscore_label = QLabel("High Score", self)

        self.strikes_label = QLabel("Strikes", self)
        self.strikes_value_label = QLabel("3", self)

        self.hints_label = QLabel("HINTS", self)
        self.hint_button1 = QPushButton("Position (SP/RP)", self)
        self.hint_button2 = QPushButton("Awards", self)
        self.hint_button3 = QPushButton("Jersey #", self)
        self.hint_button4 = QPushButton("Birthplace", self)

        self.pitches = []
        for i in range(len(self.game.current_player.pitches)):
            self.pitches.append(QLabel(self.game.current_player.pitches[i].p_type, self))
            self.pitches[-1].move(0, 100 * i)
            self.pitches[-1].adjustSize()

        self.player_name = QLabel(self.game.current_player.get_name(), self)
        self.player_name.move(0, 100 * (len(self.game.current_player.pitches) + 1))
        self.player_team = QLabel(self.game.current_player.team, self)
        self.player_team.move(0, 100 * (len(self.game.current_player.pitches) + 2))

