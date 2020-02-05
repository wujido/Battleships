"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

In this file is all constants used in program
"""

# Default name of game state file
GAME_FILE = 'game.json'

# Keys of main sections in game state file
SETTINGS_KEY = 'settings'
STATE_KEY = 'game_state'
HERO_KEY = 'field_hero'
ENEMY_KEY = 'field_enemy'

# Keys used in settings section
GAME_PLAN_X_KEY = 'plan_x'
GAME_PLAN_Y_KEY = 'plan_y'
GAME_SHIP_KEY = 'ship'
GAME_SHIP_BLOCK_KEY = 'block'
GAME_MODE_KEY = 'mode'

# Default values used in settings section
GAME_PLAN_X = 8
GAME_PLAN_Y = 8
GAME_SHIP = 6
GAME_SHIP_BLOCK = 15
GAME_MODE_SINGLE = 'single'
GAME_MODE_MULTI = 'multi'
GAME_MODE = GAME_MODE_MULTI

# Keys usend in game state section
ACTUAL_PLAYER_KEY = 'play'
GAME_STATE_KEY = 'state'
STEP_KEY = 'step'

# Default values used in gam estate section
ACTUAL_PLAYER = HERO_KEY
GAME_STATE_ACTIVE = 'active'
GAME_STATE_FINISH = 'finish'

# Exception error messages
INVALID_GAME_STEP = 'Invalid game step'
INVALID_FIELD_DIMENSION = 'Invalid field dimension'
INVALID_SHIP_COUNT = 'Invalid ship count'

# Identifires of game field
IS_WATTER = 0
IS_SHIP = 1
IS_HIT = 2
IS_MISS = 3

# Main settings of sizes of user interface
UI_WINDOW_WIDTH = 800
UI_WINDOW_HEIGHT = 400
BLOCK_DIMENSION = 25
BLOCK_PADDING = 5
UI_WINDOW_PADDING_TOP = 40
UI_WINDOW_PADDING_LEFT = 40
FIELD_SPACE = 100
STATUS_BAR_HEIGHT = 50

# Name of UI components
UI_HERO = 'hero'
UI_HERO_WINDOW_TITLE = 'Player 1'
UI_ENEMY = 'enemy'
UI_ENEMY_WINDOW_TITLE = 'Player 2'
UI_STATUS_BAR = 'status'

# Maping field identifire to color in UI
UI_DISPLAY_MAP = {
    UI_HERO: {
        IS_SHIP: 'black',
        IS_WATTER: 'blue',
        IS_HIT: 'red',
        IS_MISS: 'orange',
    },
    UI_ENEMY: {
        IS_SHIP: 'blue',
        IS_WATTER: 'blue',
        IS_HIT: 'red',
        IS_MISS: 'orange',
    }
}

# Status bar texts
UI_CAN_PLAY_TEXT = "It's your turn"
UI_CANT_PLAY_TEXT = "Wait for enemy turn"
UI_CANT_PLAY_ERR_TEXT = "YOU CAN'T PLAY NOW"
UI_ALLREADY_ATTACK_TEXT = "You have already attacked this field"

# Settings of final screen
UI_END_SCREEN_WIDTH = 400
UI_END_SCREEN_HEIGHT = 150
UI_END_SCREEN_FONT = ("Helvetica", 25, "bold")
UI_VICTORY = 'victory'
UI_VICTORY_TEXT = 'YOU WIN!'
UI_VICTORY_TEXT_COLOR = 'white'
UI_VICTORY_BACKGROUND = 'gold'
UI_LOOSE = 'loose'
UI_LOOSE_TEXT = 'YOU LOOSE :('
UI_LOOSE_TEXT_COLOR = 'white'
UI_LOOSE_BACKGROUND = 'red'
UI_CLOSE_GAME_TEXT = "Close game"

# Settings of main menu
UI_MAIN_MENU_WINDOW_GEOMETRY = "500x500"
UI_MAIN_MENU_FRAME_WIDTH = 200
UI_MAIN_MENU_FRAME_HEIGHT = 250
UI_MAIN_MENU_HEADING_TEXT = "Battle Ships The Game"
UI_MAIN_MENU_LOAD_FILE_BUTTON_TEXT = "Load Game"
UI_MAIN_MENU_MULTIPLAYER_BUTTON_TEXT = "Start game 1 vs 1"
UI_MAIN_MENU_SINGLEPLAYER_BUTTON_TEXT = "Start game 1 vs PC"
