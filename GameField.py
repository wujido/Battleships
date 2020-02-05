"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

Classes representing game field
"""

import copy

import config


class InvalidGameData(Exception):
    pass


class GameField:
    """
    A class used to represent a game field


    Attributes
    ----------
    name : str
        Name of the field
    dh : DataHandler()
        Global data handler
    game_settings : dict
        Settings from game state file
    valid_data : dict
        Last validated state of game
    live_ship : int
        Count of live ships in this game field

    Methods
    -------
    take_the_attack(x, y)
        Save game state after attack on x, y and return performed action code
    validate_fiedl_state()
        Check if state of game field is valid
    count_ship()
        Count ships in game plan
    track_ship(game_plan, x, y, live):
        In game_plan marks all fields of ship with part on x, y and return vitality of the ship
    """

    def __init__(self, field_name, dh):
        """
        Constructor of GameField class

        Parameters
        ----------
        field_name : str
            Name of the field
        dh : DataHandler()
            Global data handler
        """
        self.name = field_name
        self.dh = dh
        self.field = self.dh.get_data(field_name)
        self.game_settings = self.dh.get_data(config.SETTINGS_KEY)
        self.valid_data = copy.deepcopy(self.field)
        self.live_ship = self.game_settings[config.GAME_SHIP_KEY]
        try:
            self.validate_field_state()
        except InvalidGameData as err:
            raise err

    def take_the_attack(self, x, y):
        """
        Save game state after attack on x, y and return performed action code

        Parameters
        ----------
        x : int
            X coortinate of incoming attack
        y : int
            Y coortinate of incoming attack

        Raises
        ------
        AssertionError
            If provided coorditates are invalid or reattack same position
        InvalidGameData
            If state of game field is invalid

        Returns
        -------
        int
            Code of performed action
        """
        try:
            self.validate_field_state()
        except InvalidGameData as err:
            raise err

        if self.field[y][x] == config.IS_WATTER:
            self.field[y][x] = config.IS_MISS
            action = config.IS_MISS
        elif self.field[y][x] == config.IS_SHIP:
            self.field[y][x] = config.IS_HIT
            action = config.IS_HIT
        else:
            assert False, 'Invalid operation'

        self.dh.set_data(self.name, self.field)
        count, self.live_ship = self.count_ship()
        return action

    def validate_field_state(self):
        """
        Check if state of game field is valid

        If the game field is valid, save validated data to the self.valid_data

        Raises
        ------
        InvalidGameData
            If state of game field is invalid
        """

        # Check game plan dimension
        for x in self.field:
            if len(x) != self.game_settings[config.GAME_PLAN_X_KEY]:
                raise InvalidGameData(config.INVALID_FIELD_DIMENSION)

        if len(self.field) != self.game_settings[config.GAME_PLAN_Y_KEY]:
            raise InvalidGameData(config.INVALID_FIELD_DIMENSION)

        # Check if only one fiel is changed from previous game step
        change = False
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.field[i][j] != self.valid_data[i][j]:
                    if change:
                        raise InvalidGameData(config.INVALID_GAME_STEP)
                    else:
                        change = True

        # Check if match count of ships on plan
        count, live = self.count_ship()
        self.live_ship = live
        if count != self.game_settings[config.GAME_SHIP_KEY]:
            raise InvalidGameData(config.INVALID_SHIP_COUNT)

        self.valid_data = copy.deepcopy(self.field)

    def count_ship(self):
        """
         Count ships in game plan

        Returns
        -------
        count : int
            Count of ships in game plan
        live : int
            Count of live ships in game plan
        """

        game_plan = []
        for i in self.field:
            row = []
            for j in i:
                row.append([j, False])
            game_plan.append(row)

        count = 0
        live = 0
        for i, row in enumerate(game_plan):
            for j, item in enumerate(row):
                if item[1]:
                    continue

                if item[0] in [config.IS_SHIP, config.IS_HIT]:
                    count += 1
                    state = item[0] == config.IS_SHIP
                    if self.track_ship(game_plan, i, j, state):
                        live += 1
                else:
                    game_plan[i][j][1] = True
        return count, live

    def track_ship(self, game_plan, x, y, live):
        """
        In game_plan marks all fields of ship with part on x, y and return vitality of the ship

        Check all surrounding fields, their vitality and recursively call themselves if on the field is part of ship

        Parameters
        ----------
        game_plan : list
            List with game field and markers if the field was checked
        x : int
            X coortinate of ship part
        y : int
            Y coortinate of ship part
        live : bool
            Vitality of currently tracked ship

        Returns
        -------
        bool
            Vitality of the ship
        """

        if game_plan[x][y][0] in [config.IS_WATTER, config.IS_MISS] or game_plan[x][y][1]:
            game_plan[x][y][1] = True
            return live
        else:
            game_plan[x][y][1] = True

            if not live and game_plan[x][y][0] == config.IS_SHIP:
                live = True

            if x - 1 > 0:
                live = self.track_ship(game_plan, x - 1, y, live)
            if x + 1 < self.game_settings[config.GAME_PLAN_X_KEY]:
                live = self.track_ship(game_plan, x + 1, y, live)
            if y - 1 > 0:
                live = self.track_ship(game_plan, x, y - 1, live)
            if y + 1 < self.game_settings[config.GAME_PLAN_Y_KEY]:
                live = self.track_ship(game_plan, x, y + 1, live)

            return live
