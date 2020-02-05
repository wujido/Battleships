"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

Class representing current game
"""

import random

import config
from GameField import GameField, InvalidGameData
from Presenter import Presenter


class Game:
    """
    Class representing current game

    Attributes
    ----------
    dh : DataHandler
        Global data handler
    root : tkinter.Tk
        Root node of tkinter
    game_state : dict
        Game state from game state file
    game_settings: dict
        Settings from game state file
    hero_field : GameField
        Instance of hero's game field
    enemy_field : GameField
        Instance of the enemy's game field
    hero_presenter : Presenter
        Instance of hero's window with game
    enemy_presenter : Presenter
        Instance of the enemy's window with game


    Methods
    -------
    attack(name, x, y)
        Handle attack to `name` game field of coordinates x, y
    can_attack(name)
        Check if `name` can take the attack
    evaluate_game()
        Evaluate state of game and set corresponding state to presenters
    start_game()
        Start game in corresponding game mode
    ai_step()
        One game step of AI
    """

    def __init__(self, dh, root):
        """
        Constructor of Game class

        Parameters
        ----------
        dh : DataHandler()
            Global data handler
        root : tkinter.Tk()
            Root node of tkinter

        Raises
        ------
        InvalidGameData
            If state of any game field is invalid
        """

        self.dh = dh
        self.root = root
        self.game_state = dh.get_data(config.STATE_KEY)
        self.game_settings = self.dh.get_data(config.SETTINGS_KEY)
        try:
            self.hero_field = GameField(config.HERO_KEY, self.dh)
            self.enemy_field = GameField(config.ENEMY_KEY, self.dh)
        except InvalidGameData as err:
            raise err
        self.hero_presenter = None
        self.enemy_presenter = None

    def attack(self, name, x, y):
        """
        Perform attack to `name`

        Parameters
        ----------
        name : str
            Name of defender character
        x : int
            X coortinate to attack to
        y : int
            Y coortinate to attack to

        Returns
        -------
        int
            Code of performed action
        """

        multi = self.game_settings[config.GAME_MODE_KEY] == config.GAME_MODE_MULTI
        if self.can_attack(name):
            action = None

            if name == config.HERO_KEY:
                try:
                    action = self.hero_field.take_the_attack(x, y)
                    self.hero_presenter.paint_game()
                except AssertionError:
                    if multi:
                        self.enemy_presenter.set_status(config.UI_ALLREADY_ATTACK_TEXT)
                except InvalidGameData as err:
                    if multi:
                        self.enemy_presenter.set_err(err)

            elif name == config.ENEMY_KEY:
                try:
                    action = self.enemy_field.take_the_attack(x, y)
                    if multi:
                        self.enemy_presenter.paint_game()
                except AssertionError:
                    self.hero_presenter.set_status(config.UI_ALLREADY_ATTACK_TEXT)
                except InvalidGameData as err:
                    self.hero_presenter.set_err(err)

            if action != config.IS_HIT and action is not None:
                self.game_state[config.ACTUAL_PLAYER_KEY] = name

            self.dh.set_data(config.STATE_KEY, self.game_state)
            self.evaluate_game()
            return action

        else:
            if name == config.HERO_KEY and multi:
                self.enemy_presenter.set_err(config.UI_CANT_PLAY_ERR_TEXT)
            elif name == config.ENEMY_KEY:
                self.hero_presenter.set_err(config.UI_CANT_PLAY_ERR_TEXT)

        return 1

    def can_attack(self, name):
        """
        Check if `name` can take the attack

        Parameters
        ----------
        name : str
            Name of defender

        Returns
        -------
        bool
        """
        return self.game_state[config.ACTUAL_PLAYER_KEY] != name and self.game_state[
            config.GAME_STATE_KEY] == config.GAME_STATE_ACTIVE

    def evaluate_game(self):
        """
        Evaluate state of game and set corresponding state to presenters
        If one field haven't any live ships determinates the winner and end the game
        """
        multi = self.game_settings[config.GAME_MODE_KEY] == config.GAME_MODE_MULTI

        finish = False
        if self.hero_field.live_ship == 0:
            self.hero_presenter.end_screen(config.UI_LOOSE)
            if multi:
                self.enemy_presenter.end_screen(config.UI_VICTORY)
            finish = True
        elif self.enemy_field.live_ship == 0:
            self.hero_presenter.end_screen(config.UI_VICTORY)
            if multi:
                self.enemy_presenter.end_screen(config.UI_LOOSE)
            finish = True

        if finish:
            self.game_state[config.STATE_KEY] = config.GAME_STATE_FINISH
            self.dh.set_data(config.STATE_KEY, self.game_state)

        if self.game_state[config.ACTUAL_PLAYER_KEY] == config.HERO_KEY:
            self.hero_presenter.set_status(config.UI_CAN_PLAY_TEXT)
            if multi:
                self.enemy_presenter.set_status(config.UI_CANT_PLAY_TEXT)
        else:
            self.hero_presenter.set_status(config.UI_CANT_PLAY_TEXT)
            if multi:
                self.enemy_presenter.set_status(config.UI_CAN_PLAY_TEXT)

    def start_game(self):
        """
        Start game in corresponding game mode
        Corresponding game mode is available in self.game_settings
        """
        self.hero_presenter = Presenter(config.HERO_KEY, self.dh, self, self.hero_field, self.root)
        if self.game_settings[config.GAME_MODE_KEY] == config.GAME_MODE_MULTI:
            self.enemy_presenter = Presenter(config.ENEMY_KEY, self.dh, self, self.enemy_field, self.root)

        self.evaluate_game()

    def ai_step(self):
        """
        Perform game steps of AI until can play
        """
        if self.game_settings[config.GAME_MODE_KEY] == config.GAME_MODE_SINGLE and self.can_attack(config.HERO_KEY):
            tries = 0
            while tries <= self.game_settings[config.GAME_PLAN_X_KEY] * self.game_settings[config.GAME_PLAN_Y_KEY] * 50:
                x = random.randint(0, self.game_settings[config.GAME_PLAN_X_KEY] - 1)
                y = random.randint(0, self.game_settings[config.GAME_PLAN_Y_KEY] - 1)

                if self.hero_field.field[y][x] not in [config.IS_HIT, config.IS_MISS]:
                    self.attack(config.HERO_KEY, x, y)
                    if not self.can_attack(config.HERO_KEY):
                        break
                tries += 1
