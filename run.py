from blessed import Terminal
import numpy as np
import sys
from time import sleep
import curses

menu = ['Start', 'Exit']
def print_menu(stdscr, selected_option_idx):
    """
    Print Menu
    """
    stdscr.clear()
    h , w = stdscr.getmaxyx()
    
    for idx,row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu) + idx
        if idx == selected_option_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)
    
    stdscr.refresh()
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
        

def display_grid(stdscr, grid):
    """
    Displays the grid in the terminal.
    """

    stdscr.clear()
    h , w = stdscr.getmaxyx()
    
    for idx,row in enumerate(grid):
        x = w//2 - len(row)//2
        y = h//2 - len(grid) + idx
        stdscr.addstr(y,x,row)
    
    stdscr.refresh()

def old_grid(grid):
    for row in grid:
        grid_string = " ".join(str('-') for col in row) +'\n'
        output_string(grid_string)
        sleep(0.05)

def main(stdscr):
    """
    Main Function.
    """
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    print_menu(stdscr, current_row)
    board = generate_grid()
    board.tolist()

    game_board = []
    for i,row in enumerate(board):
        grid_string = " ".join(str('-') for col in row)
        game_board.append(grid_string)
    
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) -1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            if menu[current_row] == 'Exit':
                break
            elif menu[current_row] == 'Start':
                stdscr.refresh()
                display_grid(stdscr, menu)

            stdscr.getch()

        print_menu(stdscr, current_row)
        stdscr.refresh()

# Checking if we are running this file directly.
if __name__ == "__main__":
    # Calling the main function.
    curses.wrapper(main)