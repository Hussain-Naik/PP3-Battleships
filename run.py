from simple_term_menu import TerminalMenu
from blessed import Terminal
import numpy as np
import sys
from time import sleep

term = Terminal()
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

def display_grid(grid):
    """
    Displays the grid in the terminal.
    """
    with term.hidden_cursor():
        print(term.home + term.clear)
        for row in grid:
            grid_string = " ".join(str('-') for col in row) +'\n'
            output_string(grid_string)
            sleep(0.05)

def main():
    """
    Main Function.
    """
    game_running = True
    board = generate_grid()
    while game_running:
        display_grid(board)
        #user_choice = main_menu.show()
        if options_main[user_choice] == "Start":
            print(term.home + term.clear)
            output_string('Starting Battleships Game...\n')
            
        elif options_main[user_choice] == "Exit":
            output_string('Closing Battleships Game...\n')
            game_running = False
    
# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()