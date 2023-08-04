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
        self.horizontal_size = size
        self.nodes = [Node(row, 0) for row in range(size)]
        #self.nodes = np.array([Node(0,0), Node(0,1), Node(0,2)])
        self.sunk = all([node.used for node in self.nodes])

    def print_location(self):
        return self.nodes
    
    def rotate_ship(self):
        for node in self.nodes:
            temp_row = node.return_row()
            temp_col = node.return_col()
            node.col = temp_row
            node.row = temp_col
        self.vertical = not self.vertical
        self.horizontal_size = 1 if True else self.size
        self.vertical_size =  self.size if True else 0
    
    def update_status(self):
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
