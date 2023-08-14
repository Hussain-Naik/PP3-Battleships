from blessed import Terminal
from simple_term_menu import TerminalMenu
import numpy as np
import sys
from time import sleep
from node import Node
from ships import Ship
from ai import Ai

# Set up constant global variables
# Constant direction values
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Time delay constant
DELAY = 0.02
# Ship controls message
SHIP_CONTROLS = "Use ARROW keys to move around the grid. 'r' to rotate ship"
# Game controls message
GAME_CONTROLS = "Use ARROW keys to move around the grid."
# User validation messages
USER_VALIDATION = [
    'Please select another location',
    'Ship Rotation out of bounds or new co ordinates occupied',
    'Ship Co Ordinate occupied or out of bound']

# List of option for main menu
options_main = ["Start", "Exit"]
# List of option for start menu
options_start = ["Random Placement", "Manual Placement", "Back"]
# List of option for ship placement menu
options_ship = ["Patrol Boat",
                "Submarine",
                "Destroyer",
                "Battleship",
                "Carrier",
                "Back"]
# List of option for confirm menu
options_confirm = ["Start Game", "Reset All Ships", "Back"]

# Variable for main menu
main_menu = TerminalMenu(options_main, title="Main menu")
# Variable for start menu
start_menu = TerminalMenu(options_start, title="Start menu")
# Variable for ship menu
ship_menu = TerminalMenu(options_ship, title="Ship menu")
# Variable for ship menu
confirm_menu = TerminalMenu(options_confirm, title="Start Game")

# Blessed terminal variable
terminal = Terminal()
# User validation global message
user_validation = ''


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


def display_grid(enemy_grid, player_grid, enemy_ships, player_ships, message):
    """
    Displays the grid in the terminal.
    """
    with terminal.hidden_cursor():
        # Clear screen
        print(terminal.home + terminal.clear)
        # Print board top edge
        print(
            "            #######################     #######################"
            )
        # Print ship names, board edge and board rows for both players
        for (enemy_row,
             player_row,
             i) in zip(enemy_grid, player_grid, range(0, 10)):
            enemy_ship_name = " " * 11
            player_ship_name = " " * 11
            if i < len(enemy_ships):
                enemy_ship_name = str(enemy_ships[i])
                player_ship_name = str(player_ships[i])
            print(enemy_ship_name +
                  " # " + " ".join(str(node) for node in enemy_row) +
                  " #     # " + " ".join(str(point) for point in player_row) +
                  " # " + player_ship_name
                  )
        # Print board bottom edge
        print(
            "            #######################     #######################"
            )
        # Print message depending on game or ship placement
        print(message)
        print("Press ENTER to confirm placement. Press ESC to show menu.")
        # Print user validation when user makes error
        print(user_validation)
        sleep(DELAY)


def check_ship_move(t_node, x, y, board):
    """
    Function to return possible ship move
    """
    check_all = []
    # Loop through all nodes
    for node in t_node:
        move_y = node.row + y
        move_x = node.col + x
        if (move_y > len(board) - 1 or
           move_y < 0 or
           move_x > len(board) - 1 or
           move_x < 0 or
           board[move_y][move_x].is_occupied()):
            # Append False to temporary list if invalid node move
            check_all.append(False)
        else:
            # Append True to list if valid node move
            check_all.append(True)

    return check_all


def move_node(t_node, board, direction):
    """
    Function to move in grid
    """
    global user_validation
    (x, y) = direction
    # If parameter t_node is not a list of nodes update node is valid
    if type(t_node) != list:
        grid_row = t_node.row if (
            t_node.row +
            y
            ) > len(board) - 1 or t_node.row + y < 0 else t_node.row + y
        grid_col = t_node.col if (
            t_node.col +
            x
            ) > len(board) - 1 or t_node.col + x < 0 else t_node.col + x
        t_node.set_hidden()
        t_node = board[grid_row][grid_col]
        t_node.set_view()
        return t_node
    else:
        # If list of nodes check all nodes have valid move
        check_all = check_ship_move(t_node, x, y, board)
        if all(check_all):
            new_temp = t_node[:]
            # If moving in negative direction reverse list 
            if x > 0 or y > 0:
                new_temp.reverse()
            new_node_list = []
            # pass each node in move node function and append new list
            for node in new_temp:
                new_node_list.append(move_node(node, board, direction))
            # If moving in negative direction reverse new node list 
            if x > 0 or y > 0:
                new_node_list.reverse()
            return new_node_list
        else:
            # Display user Validation for invalid ship movement
            user_validation = USER_VALIDATION[2]
        return t_node


def confirm_rotation(ship, temp, board):
    """
    Function to confirm rotation
    """
    for ship_node in ship.nodes:
        ship_node.set_hidden()
    new_node_list = []
    for temp_node in temp:
        temp_node = board[temp_node.row][temp_node.col]
        temp_node.set_view()
        new_node_list.append(temp_node)
    return new_node_list


def manual_ship_placement(
        enemy_board, player_board, enemy_fleet, player_fleet, ship
        ):
    """
    Function to manually place player ships on board
    """
    display_grid(enemy_board, player_board,
                 enemy_fleet, player_fleet, SHIP_CONTROLS)
    ship_placed = ship.is_ship_placed()
    with terminal.cbreak(), terminal.hidden_cursor():
        temp = ship.nodes
        while not ship_placed:
            global user_validation
            user_validation = ''
            key_pressed = terminal.inkey()
            if key_pressed.code == terminal.KEY_ESCAPE:
                display_grid(enemy_board,
                             player_board,
                             enemy_fleet,
                             player_fleet,
                             SHIP_CONTROLS
                             )
                ship_placed = True
                return all(ship.is_ship_placed() for ship in player_fleet)
            elif key_pressed.code == terminal.KEY_ENTER:
                ship.confirm_placement()
                ship.assign_to_player()
                display_grid(enemy_board,
                             player_board,
                             enemy_fleet,
                             player_fleet,
                             SHIP_CONTROLS
                             )
                return all(ship.is_ship_placed() for ship in player_fleet)
            elif key_pressed.code == terminal.KEY_UP:
                temp = move_node(temp, player_board, UP)
                ship.nodes = temp
            elif key_pressed.code == terminal.KEY_DOWN:
                temp = move_node(temp, player_board, DOWN)
                ship.nodes = temp
            elif key_pressed.code == terminal.KEY_RIGHT:
                temp = move_node(temp, player_board, RIGHT)
                ship.nodes = temp
            elif key_pressed.code == terminal.KEY_LEFT:
                temp = move_node(temp, player_board, LEFT)
                ship.nodes = temp
            elif key_pressed.lower() == 'r':
                temp_r = ship.manual_ship_rotation()
                check = check_ship_move(temp_r, 0, 0, player_board)
                if all(check):
                    temp = confirm_rotation(ship, temp_r, player_board)
                    ship.change_vertical_status()
                else:
                    user_validation = USER_VALIDATION[1]
                ship.nodes = temp

            ship_placed = ship.is_ship_placed()
            display_grid(enemy_board, player_board,
                         enemy_fleet, player_fleet, SHIP_CONTROLS)


def computer_move(enemy, board, fleet):
    """
    Function to make computer move on grid
    """
    before = enemy.remaining_ship_count()
    (row, col) = enemy.new_move()
    board[row][col].make_used()
    enemy.add_hit_to_set((row, col))
    if board[row][col].occupied:
        for ships in fleet:
            ships.update_status()
        enemy.add_successful_hit((row, col))

    after = enemy.remaining_ship_count()
    if after < before:
        enemy.update_hit_list()


def generate_fleet():
    """
    Function to set upi default fleet with each size ship
    """
    return [Ship(5), Ship(4), Ship(3), Ship(2), Ship(1)]


def auto_position_fleet(fleet):
    """
    Function to randomly place fleet on board
    """
    fleet_pos = set()
    for x in range(0, len(fleet)):
        fleet[x].set_random_position()
        ship_position = fleet[x].return_node_set()
        while len(ship_position.difference(fleet_pos)) < len(ship_position):
            fleet[x].set_random_position()
            ship_position = fleet[x].return_node_set()
        fleet_pos.update(ship_position)


def place_fleet_on_board(fleet, board):
    """
    Function to assign board nodes to ships in fleet
    """
    for x in range(0, len(fleet)):
        fleet[x].assign_ship_to_board(board)
        fleet[x].confirm_placement()


def play_game(enemy_board, player_board, enemy_fleet, player_fleet):
    """
    Main game loop
    """
    enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])
    player_fleet_status = all([ship.sunk for ship in enemy_fleet])
    computer = Ai(player_fleet)
    display_grid(enemy_board, player_board,
                 enemy_fleet, player_fleet, GAME_CONTROLS)
    with terminal.cbreak(), terminal.hidden_cursor():
        output_string(
            'Select Location to Strike.\n' +
            'Press Enter when Co-ordinates confirmed Admiral')
        temp_start = enemy_board[5][5]
        while not enemy_fleet_status or not player_fleet_status:
            global user_validation
            user_validation = ''
            key_pressed = terminal.inkey()
            temp_start.set_view()
            enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])
            player_fleet_status = all([ship.sunk for ship in player_fleet])
            if enemy_fleet_status:
                # Update game_running, start_loop, win, lose
                return (False, False, True, False)
            elif player_fleet_status:
                # Update game_running, start_loop, win, lose
                return (False, False, False, True)
            if key_pressed.code == terminal.KEY_ESCAPE:
                temp_start.set_hidden()
                player_assigned_ships(enemy_fleet)
                display_grid(enemy_board,
                             player_board,
                             enemy_fleet,
                             player_fleet,
                             GAME_CONTROLS
                             )
                # Update game_running, start_loop, win, lose
                return (True, True, False, False)
            elif key_pressed.code == terminal.KEY_ENTER:
                if enemy_board[temp_start.row][temp_start.col].is_used():
                    user_validation = USER_VALIDATION[0]
                else:
                    enemy_board[temp_start.row][temp_start.col].make_used()
                    enemy_board[temp_start.row][temp_start.col].set_hidden()
                    for ships in enemy_fleet:
                        ships.update_status()
                    computer_move(computer, player_board, player_fleet)
            elif key_pressed.code == terminal.KEY_UP:
                temp_start = move_node(temp_start, enemy_board, UP)
            elif key_pressed.code == terminal.KEY_DOWN:
                temp_start = move_node(temp_start, enemy_board, DOWN)
            elif key_pressed.code == terminal.KEY_RIGHT:
                temp_start = move_node(temp_start, enemy_board, RIGHT)
            elif key_pressed.code == terminal.KEY_LEFT:
                temp_start = move_node(temp_start, enemy_board, LEFT)
            display_grid(enemy_board, player_board,
                         enemy_fleet, player_fleet, GAME_CONTROLS)
        return True


def manual_placement(game_running, start_loop):
    """
    manual ship placement loop
    """
    manual = True
    (enemy_fleet,
     enemy_fleet_status,
     enemy_board,
     player_fleet,
     player_fleet_status,
     player_board) = game_initialize()
    auto_position_fleet(enemy_fleet)
    place_fleet_on_board(enemy_fleet, enemy_board)
    all_ship_placed = all(
        ship.is_ship_placed() for ship in player_fleet)

    while manual:
        if all_ship_placed is True:
            options = options_confirm
        else:
            options = options_ship
        user_choice = return_menu_choice(all_ship_placed)
        if user_choice is None:
            user_choice = -1
        if options[user_choice] == "Patrol Boat":
            player_fleet[4].reset_ship()
            all_ship_placed = manual_ship_placement(enemy_board,
                                                    player_board,
                                                    enemy_fleet,
                                                    player_fleet,
                                                    player_fleet[4])
        elif options[user_choice] == "Submarine":
            player_fleet[3].reset_ship()
            all_ship_placed = manual_ship_placement(enemy_board,
                                                    player_board,
                                                    enemy_fleet,
                                                    player_fleet,
                                                    player_fleet[3])
        elif options[user_choice] == "Destroyer":
            player_fleet[2].reset_ship()
            all_ship_placed = manual_ship_placement(enemy_board,
                                                    player_board,
                                                    enemy_fleet,
                                                    player_fleet,
                                                    player_fleet[2])
        elif options[user_choice] == "Battleship":
            player_fleet[1].reset_ship()
            all_ship_placed = manual_ship_placement(enemy_board,
                                                    player_board,
                                                    enemy_fleet,
                                                    player_fleet,
                                                    player_fleet[1])
        elif options[user_choice] == "Carrier":
            player_fleet[0].reset_ship()
            all_ship_placed = manual_ship_placement(enemy_board,
                                                    player_board,
                                                    enemy_fleet,
                                                    player_fleet,
                                                    player_fleet[0])
        elif options[user_choice] == "Start Game":
            (game_running,
             start_loop,
             enemy_fleet_status,
             player_fleet_status) = play_game(enemy_board,
                                              player_board,
                                              enemy_fleet,
                                              player_fleet)
            manual = False
        elif options[user_choice] == "Reset All Ships":
            for ship in player_fleet:
                ship.reset_ship()
        else:
            print(terminal.home + terminal.clear)
            manual = False

        all_ship_placed = all(
            ship.is_ship_placed() for ship in player_fleet)
    return (game_running, start_loop, enemy_fleet_status,
            player_fleet_status)


def player_assigned_ships(fleet):
    """
    Function to assign ships to player
    """
    for ship in fleet:
        ship.assign_to_player()


def return_menu_choice(completed):
    """
    Function to change menu option after all ships placed on board
    """
    if completed is True:
        return confirm_menu.show()
    else:
        return ship_menu.show()


def game_initialize():
    """
    Function to initialize game variables
    """
    enemy_fleet = generate_fleet()
    enemy_fleet_status = all([ship.sunk for ship in enemy_fleet])

    player_fleet = generate_fleet()
    player_fleet_status = all([ship.sunk for ship in enemy_fleet])

    enemy_board = generate_grid()
    player_board = generate_grid()

    return (
        enemy_fleet,
        enemy_fleet_status,
        enemy_board,
        player_fleet,
        player_fleet_status,
        player_board
        )


def main():
    """
    Main Function.
    """
    game_running = True
    enemy_fleet = False
    enemy_fleet_status = False
    enemy_board = False
    player_fleet = False
    player_fleet_status = False
    player_board = False

    user_choice = main_menu.show()
    while game_running:
        if user_choice is None:
            user_choice = -1
        if options_main[user_choice] == "Start":
            print(terminal.home + terminal.clear)
            output_string('Starting Battleship Game...\n')
            user_choice = start_menu.show()
            start_loop = True
            while start_loop:
                if user_choice is None:
                    user_choice = -1
                if options_start[user_choice] == "Random Placement":
                    print(terminal.home + terminal.clear)
                    (enemy_fleet,
                     enemy_fleet_status,
                     enemy_board,
                     player_fleet,
                     player_fleet_status,
                     player_board) = game_initialize()
                    auto_position_fleet(enemy_fleet)
                    place_fleet_on_board(enemy_fleet, enemy_board)
                    auto_position_fleet(player_fleet)
                    place_fleet_on_board(player_fleet, player_board)
                    player_assigned_ships(player_fleet)
                    (game_running,
                     start_loop,
                     enemy_fleet_status,
                     player_fleet_status) = play_game(enemy_board,
                                                      player_board,
                                                      enemy_fleet,
                                                      player_fleet)
                    if not start_loop:
                        break
                    user_choice = start_menu.show()
                elif options_start[user_choice] == "Manual Placement":
                    print(terminal.home + terminal.clear)
                    (game_running,
                     start_loop,
                     enemy_fleet_status,
                     player_fleet_status
                     ) = manual_placement(game_running, start_loop)
                    if not start_loop:
                        break
                    user_choice = start_menu.show()
                elif options_start[user_choice] == "Back":
                    print(terminal.home + terminal.clear)
                    start_loop = False
                    user_choice = main_menu.show()
            if not game_running:
                break
        elif options_main[user_choice] == "Exit":
            game_running = False
    if enemy_fleet_status:
        output_string(
            'Victory is yours Admiral entire enemy fleet destroyed\n'
            )
    elif player_fleet_status:
        output_string(
            'Enemy have sunk all your vessels! better luck next time\n'
            )
    else:
        output_string('Closing Battleship Game...\n')


# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    main()
