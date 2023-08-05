from blessed import Terminal
from simple_term_menu import TerminalMenu
import numpy as np
import sys
from time import sleep
from node import Node
from ships import Ship

#Set up constant global variables
UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1,0)
RIGHT = (1,0)
CURSOR = (0,0)
DELAY = 0.02

#List of option for main menu
options_main = ["Start","Exit"]

options_ship = ["Patrol Boat","Submarine","Destroyer", "Battleship", "Carrier"]
#Variable for main menu
main_menu = TerminalMenu(options_main, title="Main menu")
#Variable for main menu
ship_menu = TerminalMenu(options_ship, title="Main menu")

player_fleet_status = []
enemy_fleet_status = []


#Blessed terminal variable
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
        sleep(DELAY)
        sys.stdout.write(char)
        sys.stdout.flush()
        
def display_grid(grid):
    """
    Displays the grid in the terminal.
    """
    with terminal.hidden_cursor():
        print(terminal.home + terminal.clear)
        print("#######################")
        for row in grid:
            print("# " + " ".join(str(node) for node in row) + " #")
        print("#######################")
        print("Use ARROW keys to move around the grid.")
        print("Press ENTER to confirm placement")
        print("Press ESC to show menu.")
        sleep(DELAY)

def move_node(t_node, board, direction, size):
    """
    Function to move in grid
    """
    (x, y) = direction
    (size_x, size_y) = size
    grid_row = t_node.row if t_node.row + y + size_y > len(board) -1  or t_node.row + y < 0 else t_node.row + y
    grid_col = t_node.col if t_node.col + x + size_x> len(board) -1  or t_node.col + x < 0 else t_node.col + x
    t_node.set_hidden()
    t_node = board[grid_row][grid_col]
    t_node.set_view()
    return t_node

def move_ship(ship, board, direction):
    """
    Method to move ship up on grid
    """
    
def generate_fleet():
    fleet = []
    patrol = Ship(1)
    fleet.append(patrol)
    sub = Ship(2)
    fleet.append(sub)
    destroyer = Ship(3)
    fleet.append(destroyer)
    battleship = Ship(4)
    fleet.append(battleship)
    carrier = Ship(5)
    fleet.append(carrier)
    return fleet

        
def main():
    """
    Main Function.
    """
    enemy_fleet = generate_fleet()
    enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])
 
    board = generate_grid()

    #Testing section

    #End of testing section
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
                    temp_start.set_view()
                    if key_pressed.code == terminal.KEY_ESCAPE:
                        temp_start.set_hidden()
                        break
                    elif key_pressed.code == terminal.KEY_ENTER:
                        board[temp_start.row][temp_start.col].make_used()
                        board[temp_start.row][temp_start.col].set_hidden()
                    elif key_pressed.code == terminal.KEY_UP:
                        temp_start = move_node(temp_start, board, UP, CURSOR)
                    elif key_pressed.code == terminal.KEY_DOWN:
                        temp_start = move_node(temp_start, board, DOWN, CURSOR)
                    elif key_pressed.code == terminal.KEY_RIGHT:
                        temp_start = move_node(temp_start, board, RIGHT, CURSOR)
                    elif key_pressed.code == terminal.KEY_LEFT:
                        temp_start = move_node(temp_start, board, LEFT, CURSOR)
                    display_grid(board)
        elif options_main[user_choice] == "Exit":
            break
        

# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()