from blessed import Terminal
from simple_term_menu import TerminalMenu
import numpy as np
import sys
from time import sleep
from node import Node

options_main = [
    "Start",
    "Exit",
]
main_menu = TerminalMenu(
    options_main,
    title="Main menu"
    )
terminal = Terminal()

def generate_grid():
    """
    Generates and returns a grid of nodes as a 2D numpy array.
    """
    return np.array(
        [[Node(row, col) for col in range(10)] for row in range(10)]
        )

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
    with terminal.hidden_cursor():
        print(terminal.home + terminal.clear)
        for row in grid:
            print(" ".join(str(node) for node in row))
        sleep(0.15)

def main():
    """
    Main Function.
    """
    board = generate_grid()
    while True:
        user_choice = main_menu.show()
        if options_main[user_choice] == "Start":
            output_string('Starting Battleship Game...')
            display_grid(board)
            with terminal.cbreak(), terminal.hidden_cursor():
                output_string('Select Location to Strike.\nPress Enter when Co-ordinates confirmed Admiral')
                temp_start = board[5][5]
                while True:
                    key_pressed = terminal.inkey()
                    temp_start.make_used()
                    if key_pressed.code == terminal.KEY_ENTER:
                        break
                    elif key_pressed.code == terminal.KEY_UP:
                        temp_start.make_unused()
                        temp_start = board[temp_start.row - 1][temp_start.col]
                        temp_start.make_used()
                    elif key_pressed.code == terminal.KEY_DOWN:
                        if temp_start.row + 1 > len(board) -1:
                            temp_start.make_unused()
                            temp_start = board[0][temp_start.col]
                            temp_start.make_used()
                        else:
                            temp_start.make_unused()
                            temp_start = board[temp_start.row + 1][temp_start.col]
                            temp_start.make_used()
                    elif key_pressed.code == terminal.KEY_RIGHT:
                        if temp_start.col + 1 > len(board) -1:
                            temp_start.make_unused()
                            temp_start = board[temp_start.row][0]
                            temp_start.make_used()
                        else:
                            temp_start.make_unused()
                            temp_start = board[temp_start.row][temp_start.col + 1]
                            temp_start.make_used()
                    elif key_pressed.code == terminal.KEY_LEFT:
                        temp_start.make_unused()
                        temp_start = board[temp_start.row][temp_start.col - 1]
                        temp_start.make_used()
                    display_grid(board)
        elif options_main[user_choice] == "Exit":
            break
        

# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()