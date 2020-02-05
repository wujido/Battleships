# Battle ships
This program was created as credit program on MFF UK in winter semester 2019/2020

## User guide
###How to play?
To play the game just clone repo or download the project.
Then type this command in corresponding directory
````shell script
python index.py
````

Then you can choose between two game modes
1. Player vs player - each game instance is in separate window
2. Player vs computer

or load game from file (format is described below) 

### Rules
Aim of the game is to destroy all ships of the opponent.
Game plan is generated automatically.

Meaning of colors in fields:
* Blue - watter, there is no ship and no attack was performed to this field
* Black - ship, alive part of a ship
* Orange - miss, unsuccessful try to attack
* Red - hit, destroyed part of a ship

 
Players take turns after the attack, if the player hits the ship can play again.
If player destroy all ships of the opponent the wins.

## Configuration
You can configure apperance of the game in ``config.py`` file.
### Game file format
File for load game, must have following format:
It's json file with 4 main sections:
* settings
* state
* hero field
* enemy field

Keys of this section must correspond values from ``config.py`` 

#### Settings
There is 5 required field in this section, their keys must coresponding values from ``config.py``
* Plan x - number of rows in game plan
* Plan y - number of columns in game plan
* Ships -  number of ships in game plan
* Blocks - number of blocks that all ships have together
* Mode - choice of game mode

#### State
There is 3 required field in this section, their keys must coresponding values from ``config.py``
* Play - key of the player on the move
* Step - number of game rounds already played
* State - active or finished   


#### Hero / Enemy field
It must be two dimensional array with 'Plan x' arrays with 'Plan y' items.
Each item must be one of the key (watter, ship, miss, hit).
Number of ship + hit must correspond 'blocks' from settings. Groups of ships (or hits) must cottespond 'ship' form settings.
Group (ship) is sequence of items in one of these direction for item on index [x][y]: 

* field[x+1][y]
* field[x-1][y]
* field[x][y+1]
* filed[x][y+1]

Both indexes must be valid.