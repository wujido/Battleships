"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

User interface layer of main menu
"""

from tkinter import *
from tkinter import filedialog

import config
from DataHandler import DataHandler
from Game import Game
from GameBuilder import GameBuilder
from GameField import InvalidGameData


class MainMenu:
    """
    Window with main menu

    Attributes
    ----------
    root : tkinter.Tk()
        Root node of tkinter


    Methods
    -------
    load_game()
        Display file selecting dialog and start the game with selected file
    start_game(mode)
        Start game in provided mode

    """

    def __init__(self, root):
        """
       Constructor of MainMenu class

        Parameters
        ----------
        root : tkinter.Tk()
            Root node of tkinter
        """

        self.root = root
        self.root.title("Main Menu")
        self.root.geometry(config.UI_MAIN_MENU_WINDOW_GEOMETRY)

        canvas = Canvas(self.root)

        canvas.config(bg="#f7f1e3", width=config.UI_MAIN_MENU_FRAME_WIDTH, height=config.UI_MAIN_MENU_FRAME_HEIGHT)
        canvas.pack(expand=True, fill=BOTH)

        heading_frame1 = Frame(self.root, bg="#333945", bd=5)
        heading_frame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

        heading_frame2 = Frame(heading_frame1, bg="#EAF0F1")
        heading_frame2.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)

        heading_label = Label(heading_frame2, text=config.UI_MAIN_MENU_HEADING_TEXT, fg='black')
        heading_label.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.5)

        btn1 = Button(self.root, text=config.UI_MAIN_MENU_LOAD_FILE_BUTTON_TEXT, bg='black', fg='white',
                      command=self.load_game)
        btn1.place(relx=0.28, rely=0.3, relwidth=0.45, relheight=0.1)

        btn2 = Button(self.root, text=config.UI_MAIN_MENU_MULTIPLAYER_BUTTON_TEXT, bg='black', fg='white',
                      command=lambda: self.start_game(config.GAME_MODE_MULTI))
        btn2.place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.1)

        btn3 = Button(self.root, text=config.UI_MAIN_MENU_SINGLEPLAYER_BUTTON_TEXT, bg='black', fg='white',
                      command=lambda: self.start_game(config.GAME_MODE_SINGLE))
        btn3.place(relx=0.28, rely=0.5, relwidth=0.45, relheight=0.1)

    def load_game(self):
        """
        Display file selecting dialog and start the game with selected file
        """

        filename = filedialog.askopenfilename(title="Select A File",
                                              filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if filename:
            data = DataHandler(filename)
            game = Game(data, self.root)
            game.start_game()

    def start_game(self, mode):
        """
       Start game in provided mode

        Parameters
        ----------
        mode : str
            Key of game mode


        Raises
        ------
        InvalidGameData
            If state of game field in automaticaly generaget game file is invalid
        """

        builder = GameBuilder()
        builder.create_settings()
        builder.create_initial_state()
        builder.template[config.SETTINGS_KEY][config.GAME_MODE_KEY] = mode

        while True:
            try:
                builder.create_game_plan(config.HERO_KEY)
                builder.create_game_plan(config.ENEMY_KEY)
                data = DataHandler(config.GAME_FILE, builder.template)
                game = Game(data, self.root)
                game.start_game()
                break
            except InvalidGameData as err:
                if err.args[0] == config.INVALID_SHIP_COUNT:
                    continue
                else:
                    raise err
