import sys
import math
import random

import statcast_data as st


class Game:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.strikes = 3
        self.hints = [True, True, True, True]
        self.current_player = None
        self.previous_players = []
        self.stats = st.Statcast()

    def new_game(self):
        self.score = 0
        self.strikes = 3
        self.previous_players = []
        self.hints = [True, True, True, True]
        self.new_level()

    def new_level(self):
        index = random.randint(0, len(self.stats.pitchers))
        self.current_player = self.stats.pitchers[index]

        if self.current_player.get_name() in self.previous_players:
            self.new_level()

        self.current_player.set_pitch_arsenal()
        self.previous_players.append(self.current_player.get_name())

    def check_answer(self, answer):
        if answer == self.current_player.get_name():
            self.score += self.calc_score()
            self.new_level()
        else:
            self.strikes -= 1
            if self.strikes == 0:
                self.game_over()

    def reset_hints(self):
        self.hints = [True, True, True, True]

    def set_hint(self, index):
        assert (0 <= index < 4)
        self.hints[index] = False

    def get_hints(self):
        return self.hints

    def calc_score(self):
        score = 5
        for hint in self.hints:
            if not hint:
                score -= 1
        return score

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
