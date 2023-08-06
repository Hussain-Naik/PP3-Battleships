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
        
def display_grid(enemy_grid, player_grid, enemy_ships, player_ships):
    """
    Displays the grid in the terminal.
    """
    with terminal.hidden_cursor():
        print(terminal.home + terminal.clear)
        print("           #######################     #######################")
        for (enemy_row, player_row, i) in zip(enemy_grid, player_grid, range(0,10)):
            enemy_ship_name = " " * 11
            player_ship_name = " " * 11
            if i < len(enemy_ships):
                enemy_ship_name = str(enemy_ships[i])
                player_ship_name = str(player_ships[i])
            print(enemy_ship_name + "# " + " ".join(str(node) for node in enemy_row) + " #     # " + " ".join(str(point) for point in player_row) + " # "+ player_ship_name)
        print("           #######################     #######################")
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
    carrier = Ship(5)
    fleet.append(carrier)
    battleship = Ship(4)
    fleet.append(battleship)
    destroyer = Ship(3)
    fleet.append(destroyer)
    submarine = Ship(2)
    fleet.append(submarine)
    patrol = Ship(1)
    fleet.append(patrol)
    
    return fleet

def auto_position_fleet(fleet):
    fleet_positions = set()
    for x in range(0, len(fleet)):
        fleet[x].set_random_position()
        ship_position = fleet[x].return_node_set()
        while len(ship_position.difference(fleet_positions)) < len(ship_position):
            fleet[x].set_random_position()
            ship_position = fleet[x].return_node_set()
        fleet_positions.update(ship_position)

        
def place_fleet_on_board(fleet, board):
    for x in range(0, len(fleet)):
        fleet[x].assign_ship_to_board(board)
        fleet[x].confirm_placement()
        
def main():
    """
    Main Function.
    """
    enemy_fleet = generate_fleet()
    enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])

    player_fleet = generate_fleet()
    player_fleet_status = all([ship.sunk for ship in enemy_fleet])
 
    enemy_board = generate_grid()
    player_board = generate_grid()

    #Testing section
    print(enemy_fleet_status)
    print(enemy_fleet[0].name)
    auto_position_fleet(enemy_fleet)
    enemy_fleet[0].sunk = True
    print(f'{str(enemy_fleet[0])} nodes:{enemy_fleet[0].return_node_set()} size:{enemy_fleet[0].return_size()}')
    print(f'{str(enemy_fleet[1])} nodes:{enemy_fleet[1].return_node_set()} size:{enemy_fleet[1].return_size()}')
    print(f'{str(enemy_fleet[2])} nodes:{enemy_fleet[2].return_node_set()} size:{enemy_fleet[2].return_size()}')
    print(f'{str(enemy_fleet[3])} nodes:{enemy_fleet[3].return_node_set()} size:{enemy_fleet[3].return_size()}')
    print(f'{str(enemy_fleet[4])} nodes:{enemy_fleet[4].return_node_set()} size:{enemy_fleet[4].return_size()}')
    place_fleet_on_board(enemy_fleet, enemy_board)
    #End of testing section
    while not enemy_fleet_status or not player_fleet_status:
        user_choice = main_menu.show()
        enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])
        if options_main[user_choice] == "Start":
            output_string('Starting Battleship Game...')
            display_grid(enemy_board, player_board, enemy_fleet, player_fleet)
            with terminal.cbreak(), terminal.hidden_cursor():
                output_string('Select Location to Strike.\nPress Enter when Co-ordinates confirmed Admiral')
                temp_start = enemy_board[5][5]
                while not enemy_fleet_status or not player_fleet_status:
                    key_pressed = terminal.inkey()
                    temp_start.set_view()
                    enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])
                    if key_pressed.code == terminal.KEY_ESCAPE or enemy_fleet_status:
                        temp_start.set_hidden()
                        break
                    elif key_pressed.code == terminal.KEY_ENTER:
                        enemy_board[temp_start.row][temp_start.col].make_used()
                        enemy_board[temp_start.row][temp_start.col].set_hidden()
                        for ships in enemy_fleet:
                            ships.update_status()
                    elif key_pressed.code == terminal.KEY_UP:
                        temp_start = move_node(temp_start, enemy_board, UP, CURSOR)
                    elif key_pressed.code == terminal.KEY_DOWN:
                        temp_start = move_node(temp_start, enemy_board, DOWN, CURSOR)
                    elif key_pressed.code == terminal.KEY_RIGHT:
                        temp_start = move_node(temp_start, enemy_board, RIGHT, CURSOR)
                    elif key_pressed.code == terminal.KEY_LEFT:
                        temp_start = move_node(temp_start, enemy_board, LEFT, CURSOR)
                    display_grid(enemy_board, player_board, enemy_fleet, player_fleet)
        elif options_main[user_choice] == "Exit" or enemy_fleet_status or player_fleet_status:
            break
    if enemy_fleet_status:
        print("You win")
    else:
        print("You Lose")

# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()