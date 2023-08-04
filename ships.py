import numpy as np
from node import Node
class Ship:
    """
    Battleship class
    """
    sunk = True
    vertical = False
    vertical_size = 1
    horizontal_size = 1
    nodes = []
    
    def __init__(self, size):
        #Size of the ship
        self.size = size
        #Set horizontal size for checking end collision
        self.horizontal_size = size
        #Set temporary nodes for ship
        self.nodes = [Node(row, 0) for row in range(size)]
        #Set ship sunk boolean based of all node used variable
        self.sunk = all([node.used for node in self.nodes])

    def print_location(self):
        return self.nodes
    
    def rotate_ship(self):
        """
        Rotate method for ship
        """
        for node in self.nodes:
            #Assign temporary variables
            temp_row = node.return_row()
            temp_col = node.return_col()
            #Invert row and col
            node.col = temp_row
            node.row = temp_col
        #Change vertical
        self.vertical = not self.vertical
        #Switch Vertical and horizontal sizes
        self.horizontal_size = 1 if True else self.size
        self.vertical_size =  self.size if True else 0
    
    def update_status(self):
        """
        Update ship sunk status
        """
        self.sunk = all([node.used for node in self.nodes])

    def assign_ship_to_board(self, board):
        placed_nodes = []
        for node in self.nodes:
            placed_nodes.append(board[node.col][node.row])
            print(id(board[node.col][node.row]))
            print(id(node))
        self.nodes = placed_nodes
    def confirm_placement(self):
        for node in self.nodes:
            node.occupy()
