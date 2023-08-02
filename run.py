from simple_term_menu import TerminalMenu
from blessed import Terminal
import numpy as np
import sys
from time import sleep

terminal = Terminal()
# Menu option lists
options_main = ['Start', 'Exit']
# Menu Variables
main_menu = TerminalMenu(options_main,title='Main Menu')

def generate_grid():
    """
    Generates and returns a grid of nodes as a 2D numpy array.
    """
    return np.arange(100).reshape(10,10)

def output_string(string):
    """ 
    Displays the string parameter with a delayed timer.
    """
    for char in string:
        sleep(0.1)
        sys.stdout.write(char)
        sys.stdout.flush()



def main():
    """
    Main Function.
    """
    game_running = True
    board = generate_grid()
    while game_running:
        user_choice = main_menu.show()
        if options_main[user_choice] == "Start":
            output_string('Starting Battleships Game...\n')
        elif options_main[user_choice] == "Exit":
            output_string('Closing Battleships Game...\n')
            game_running = False
    
# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()