"""
MFF UK - 2019/20 Winter - Programing 1 - Credit Program
@author Václav Hrouda - wujido (vahrouda@gmail.com)

Index file, program starts here
"""

import tkinter

from MainMenu import MainMenu

# Driver code for programm
if __name__ == '__main__':
    root = tkinter.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
