"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

User interface layer of the game
"""

import tkinter
import config


class Presenter:
    """
    Main presenter of game. Handle dispalyed window and user interactivity.

    Meaning of hero and enemy is according to visual position in canvas

    Attributes
    ----------
    dh : DataHandler()
        Global data handler
    game : Game()
        Instance of current game
    hero : str
        Key of the hero's component in UI
    hero : str
        Key of the enemy's component in UI
    window : tkinter.Toplevel()
        Instance of current window
    canvas : tkinter.Canvas()
        Main canvas for painting all game UI components
    game_field : GameField()
        Instance of provided game field
    game_settings : dict
        Settings from game state filed

    Methods
    -------
    get_starting_position(name)
        Return (x, y) position of left top corner of `name` component in canvas
    paint_game()
        Wrapper function for painting game plans
    paint_status_bar()
        Paint status bar to canvas
    paint_error_bar()
        Paint error bar to canvas
    set_status(msg)
        Dispay `msg` in status bar
    set_status(msg)
        Dispay `msg` in status bar
    set_err(msg)
        Dispay `msg` in error bar
    paint_plan(name, position, start_x, start_y)
        Paint game plan with data with `name` key
    bind_event_handlers()
        Register event handlers needed for interactivity
    handle_attack(e)
        Callback function for click event handler
    get_field_index(name, x, y)
        Calculate index of filed on `x`, `y` position in canvas
    end_screen(state)
        Pain final screen with provided state
    """

    def __init__(self, name, dh, game, game_field, root):
        """
       Constructor of Presenter class

        Parameters
        ----------
        name : str
            Key of hero's displayed game plan
        dh : DataHandler()
           Global data handler
        game : Game()
            Instance of current game
        game_field : GameField()
            Instance of hero's game field
        root : tkinter.Tk()
            Root node of tkinter
        """

        self.dh = dh
        self.game = game

        self.hero = name

        self.window = tkinter.Toplevel(root)

        if name == config.HERO_KEY:
            self.enemy = config.ENEMY_KEY
            self.window.title(config.UI_HERO_WINDOW_TITLE)
        elif name == config.ENEMY_KEY:
            self.enemy = config.HERO_KEY
            self.window.title(config.UI_ENEMY_WINDOW_TITLE)

        self.canvas = tkinter.Canvas(self.window, width=config.UI_WINDOW_WIDTH, height=config.UI_WINDOW_HEIGHT)
        self.canvas.pack()

        self.game_field = game_field
        self.game_settings = self.dh.get_data(config.SETTINGS_KEY)

        self.paint_game()
        self.status_bar = self.paint_status_bar()
        self.err_bar = self.paint_error_bar()
        self.bind_event_handlers()

    def get_starting_position(self, name):
        """
       Return (x, y) position of left top corner of `name` component in canvas

        Parameters
        ----------
        name : str
            Name of the UI component

        Returns
        -------
        x : int
            X position in canvas
        y : int
            Y position in canvas
        """

        x = config.UI_WINDOW_PADDING_LEFT
        y = config.UI_WINDOW_PADDING_TOP

        if name == config.UI_HERO:
            y += config.STATUS_BAR_HEIGHT
        elif name == config.UI_ENEMY:
            x += config.FIELD_SPACE + config.UI_WINDOW_PADDING_LEFT + (
                    config.BLOCK_PADDING + config.BLOCK_DIMENSION) * \
                 self.game_settings['plan_y']
            y += config.STATUS_BAR_HEIGHT
        elif name == config.UI_STATUS_BAR:
            pass

        return x, y

    def paint_game(self):
        """
        Wrapper function for painting game plans
        """

        hero_x, hero_y = self.get_starting_position(config.UI_HERO)
        enemy_x, enemy_y = self.get_starting_position(config.UI_ENEMY)

        self.paint_plan(self.hero, config.UI_HERO, hero_x, hero_y)
        self.paint_plan(self.enemy, config.UI_ENEMY, enemy_x, enemy_y)

    def paint_status_bar(self):
        """
        Paint status bar to canvas

        Returns
        -------
        any
            Return value of tkinter.Canvas.create_text()
        """
        x, y = self.get_starting_position(config.UI_STATUS_BAR)
        return self.canvas.create_text(x, y, text="", anchor="nw")

    def paint_error_bar(self):
        """
        Paint error bar to canvas

        Returns
        -------
        any
            Return value of tkinter.Canvas.create_text()
        """

        a = self.canvas.create_text(5, 5, text="", anchor="nw", fill='red')
        return a

    def set_status(self, msg):
        """
        Dispay `msg` in status bar

        Parameters
        ----------
        msg : str
            Text to display
        """

        self.canvas.itemconfigure(self.status_bar, text=msg, fill='black')

    def set_err(self, msg):
        """
        Dispay `msg` in error bar

        Parameters
        ----------
        msg : str
            Text to display
        """
        self.canvas.itemconfigure(self.status_bar, text=msg, fill='red')

    def paint_plan(self, name, position, start_x=0, start_y=0):
        """
        Paint game plan with data with `name` key

        Parameters
        ----------
        name : str
            Name of data key in game file
        position : str
            Name of UI component. Needed for recognition of display mode (hero can't see ships of the enemy)
        start_x : int
            X position of top left corner in canvas
        start_y : int
            Y position of top left corner in canvas
        """

        field = self.dh.get_data(name)
        tag = "item_" + position

        for x in range(self.game_settings['plan_x']):
            y1 = start_y + (config.BLOCK_PADDING + config.BLOCK_DIMENSION) * x
            y2 = y1 + config.BLOCK_DIMENSION
            for y in range(self.game_settings['plan_y']):
                x1 = start_x + (config.BLOCK_PADDING + config.BLOCK_DIMENSION) * y
                x2 = x1 + config.BLOCK_DIMENSION
                item = field[x][y]
                self.canvas.create_rectangle(x1, y1, x2, y2, tags=tag, fill=config.UI_DISPLAY_MAP[position][item])

    def bind_event_handlers(self):
        """
        Register event handlers needed for interactivity
        """

        self.canvas.tag_bind('item_' + config.UI_ENEMY, '<Button-1>', self.handle_attack)

    def handle_attack(self, e):
        """
        Callback function for click event handler

       Parameters
        ----------
        e : any
            Event object provided by the event handler
        """
        x, y = self.get_field_index(config.UI_ENEMY, e.x, e.y)
        action = self.game.attack(self.enemy, x, y)
        if action:
            self.canvas.itemconfig('current', fill=config.UI_DISPLAY_MAP[config.UI_ENEMY][action])
        self.game.ai_step()

    def get_field_index(self, name, x, y):
        """
        Calculate index of filed on `x`, `y` position in canvas

        Parameters
        ----------
        name : str
            Name of UI component
        x : int
            X position in canvas
        y : int
            Y position in canvas

        Returns
        -------
        x : int
            X index of field in canvas
        y : int
            Y index of field in canvas
        """
        start_x, start_y = self.get_starting_position(name)
        field_x = (x - start_x) // (config.BLOCK_DIMENSION + config.BLOCK_PADDING)
        field_y = (y - start_y) // (config.BLOCK_DIMENSION + config.BLOCK_PADDING)
        return field_x, field_y

    def end_screen(self, state):
        """
        Pain final screen with provided state

        Parameters
        ----------
        state : str
            Key of state to display
        """

        if state == config.UI_VICTORY:
            background = config.UI_VICTORY_BACKGROUND
            color = config.UI_VICTORY_TEXT_COLOR
            msg = config.UI_VICTORY_TEXT
        elif state == config.UI_LOOSE:
            background = config.UI_LOOSE_BACKGROUND
            color = config.UI_LOOSE_TEXT_COLOR
            msg = config.UI_LOOSE_TEXT
        else:
            assert False, 'Something is wrong'

        top_window = tkinter.Frame(self.canvas, bg=background)
        self.canvas.create_window(config.UI_WINDOW_WIDTH // 2,
                                  config.UI_WINDOW_HEIGHT // 2,
                                  width=config.UI_END_SCREEN_WIDTH,
                                  height=config.UI_END_SCREEN_HEIGHT,
                                  window=top_window
                                  )

        label = tkinter.Label(top_window, text=msg, bg=background, fg=color, font=config.UI_END_SCREEN_FONT,
                              width=config.UI_END_SCREEN_WIDTH, pady=config.UI_END_SCREEN_HEIGHT // 4 + 2)
        button = tkinter.Button(top_window, text=config.UI_CLOSE_GAME_TEXT, command=self.window.destroy, bg=background,
                                fg=color, width=config.UI_END_SCREEN_WIDTH, font=("Helvetica", 12, "bold"))

        label.pack()
        button.pack()
