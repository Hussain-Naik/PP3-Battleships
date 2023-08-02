from simple_term_menu import TerminalMenu
from blessed import Terminal
import numpy as np

# Menu option lists
options_main = ['Start', 'Exit']
# Menu Variables
main_menu = TerminalMenu(options_main,title='Main Menu')

def main():
    """
    Main Function.
    """
    game_running = True

    while game_running:
        user_choice = main_menu.show()
        if options_main[user_choice] == "Start":
            print('Starting Game...')
        elif options_main[user_choice] == "Exit":
            print('Closing Game...')
            game_running = False
    
# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()