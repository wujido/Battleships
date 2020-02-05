"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

Generator of game file
"""

import random

from config import *


class GameBuilder:
    """
    Class used for generating template of game file


    Attributes
    ----------
    template : dict
        Template of game file

    Methods
    -------
        create_settings()
            Add default settings section to the template
        create_initial_state()
            Add default state section to the template
    """

    def __init__(self):
        self.template = {}

    def create_settings(self):
        """
        Add default settings section to the template
        """
        self.template[SETTINGS_KEY] = {
            GAME_PLAN_X_KEY: GAME_PLAN_X,
            GAME_PLAN_Y_KEY: GAME_PLAN_Y,
            GAME_SHIP_KEY: GAME_SHIP,
            GAME_SHIP_BLOCK_KEY: GAME_SHIP_BLOCK,
            GAME_MODE_KEY: GAME_MODE,
        }

    def create_initial_state(self):
        """
        Add default state section to the template
        """
        self.template[STATE_KEY] = {
            ACTUAL_PLAYER_KEY: ACTUAL_PLAYER,
            STEP_KEY: 0,
            GAME_STATE_KEY: GAME_STATE_ACTIVE
        }

    def create_game_plan(self, name):
        """
        Add game plan to the template. Generates required numbers of ships with correct sum of ship parts.

        Parameters
        ----------
        name : str
            Key of game plan section added to the template
        """
        plan = [[0 for i in range(GAME_PLAN_Y)] for j in range(GAME_PLAN_Y)]

        ship = 0
        for i in range(GAME_SHIP_BLOCK):
            while True:
                x = random.randint(0, GAME_PLAN_X - 1)
                y = random.randint(0, GAME_PLAN_Y - 1)

                if plan[x][y] == 0:
                    is_new_ship = True

                    connect = 0
                    if x - 1 > 0 and plan[x - 1][y] == 1:
                        connect += 1
                    if x + 1 < GAME_PLAN_X and plan[x + 1][y] == 1:
                        connect += 1
                    if y - 1 > 0 and plan[x][y - 1] == 1:
                        connect += 1
                    if y + 1 < GAME_PLAN_Y and plan[x][y + 1] == 1:
                        connect += 1

                    if connect > 1:
                        continue
                    elif connect == 1:
                        is_new_ship = False

                    if GAME_SHIP_BLOCK - i + 1 <= GAME_SHIP - ship and not is_new_ship:
                        continue
                    elif ship < GAME_SHIP:
                        plan[x][y] = 1
                        if is_new_ship:
                            ship += 1
                        break
                    elif not is_new_ship:
                        plan[x][y] = 1
                        break

        self.template[name] = plan
