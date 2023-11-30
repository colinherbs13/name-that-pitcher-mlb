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

        self.user_input = QLineEdit(self)
        self.guess_button = QPushButton("Guess", self)

        self.score_label = QLabel("Score", self)
        self.score_value_label = QLabel(self)
        self.highscore_label = QLabel("High Score", self)
        self.highscore_value_label = QLabel(self)

        self.strikes_label = QLabel("Strikes", self)
        self.strikes_value_label = QLabel(self)

        self.hints_label = QLabel("HINTS", self)
        self.hint_button1 = QPushButton("Position (SP/RP)", self)
        self.hint_button2 = QPushButton("Awards", self)
        self.hint_button3 = QPushButton("Jersey #", self)
        self.hint_button4 = QPushButton("Birthplace", self)

        self.pitches = []

        self.player_name = QLabel(self)
        self.player_team = QLabel(self)
        self.player_position = QLabel(self)
        self.player_awards = QLabel(self)
        self.player_jersey_num = QLabel(self)
        self.player_birthplace = QLabel(self)

        self.format_widgets()
        self.set_signals()
        self.reset_ui()

    def format_widgets(self):
        self.user_input.move(200, 350)
        self.guess_button.move(210 + self.user_input.width(), 350)

        self.player_name.move(0, 100 * (len(self.game.current_player.pitches) + 1))
        self.player_team.move(0, 100 * (len(self.game.current_player.pitches) + 2))

        self.score_label.move(400, 50)
        self.score_value_label.move(400, 100)
        self.highscore_label.move(400, 150)
        self.highscore_value_label.move(400, 200)

        self.strikes_label.move(400, 250)
        self.strikes_value_label.move(400, 300)

        self.hints_label.move(200, 50)
        self.hint_button1.move(200, 100)
        self.hint_button2.move(200, 150)
        self.hint_button3.move(200, 200)
        self.hint_button4.move(200, 250)

        self.player_position.move(210 + self.hint_button1.width(), 100)
        self.player_awards.move(210 + self.hint_button2.width(), 150)
        self.player_jersey_num.move(210 + self.hint_button3.width(), 200)
        self.player_birthplace.move(210 + self.hint_button4.width(), 250)

        self.player_position.hide()
        self.player_awards.hide()
        self.player_jersey_num.hide()
        self.player_birthplace.hide()

    def reset_ui(self):
        self.player_name.setText(self.game.current_player.get_name())
        self.player_team.setText(self.game.current_player.team)
        self.player_position.setText(self.game.current_player.position)
        self.player_birthplace.setText(self.game.current_player.birthplace)
        self.player_awards.setText(str(self.game.current_player.awards))
        self.player_jersey_num.setText(self.game.current_player.jersey_num)

        self.score_value_label.setText(str(self.game.score))
        self.highscore_value_label.setText(str(self.game.high_score))
        self.strikes_value_label.setText(str(self.game.strikes))

        self.hint_button1.setEnabled(True)
        self.hint_button2.setEnabled(True)
        self.hint_button3.setEnabled(True)
        self.hint_button4.setEnabled(True)
        self.player_position.hide()
        self.player_birthplace.hide()
        self.player_awards.hide()
        self.player_jersey_num.hide()

        for i in range(len(self.pitches)):
            self.pitches[i].hide()
            self.pitches[i].destroy()

        self.pitches = []
        for i in range(len(self.game.current_player.pitches)):
            self.pitches.append(QLabel(self.game.current_player.pitches[i].p_type, self))
            self.pitches[-1].move(0, 100 * i)
            self.pitches[-1].adjustSize()
            self.pitches[-1].show()

    def set_signals(self):
        self.guess_button.clicked.connect(self.submit_answer)
        self.hint_button1.clicked.connect(self.display_position_hint)
        self.hint_button2.clicked.connect(self.display_awards_hint)
        self.hint_button3.clicked.connect(self.display_jersey_hint)
        self.hint_button4.clicked.connect(self.display_birthplace_hint)

    def submit_answer(self):
        if self.game.check_answer(self.user_input.text()):
            self.reset_ui()
        else:
            self.strikes_value_label.setText(str(self.game.strikes))
            if self.game.game_over_status:
                print("GAME OVER: RESET UI")

    def display_position_hint(self):
        self.hint_button1.setEnabled(False)
        self.game.hints[0] = False
        self.player_position.show()

    def display_awards_hint(self):
        self.hint_button2.setEnabled(False)
        self.game.hints[1] = False
        self.player_awards.show()

    def display_jersey_hint(self):
        self.hint_button3.setEnabled(False)
        self.game.hints[2] = False
        self.player_jersey_num.show()

    def display_birthplace_hint(self):
        self.hint_button4.setEnabled(False)
        self.game.hints[3] = False
        self.player_birthplace.show()
