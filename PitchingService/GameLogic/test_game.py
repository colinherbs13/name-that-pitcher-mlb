import sys

from GameLogic.game_logic import Game

class MainMenu():
    def __init__(self):
        self.update_db()


    def update_db(self):
        game = Game()
        game.new_level()


if __name__ == '__main__':
    menu = MainMenu()
    sys.exit()