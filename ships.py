import numpy as np
from node import Node
class Ship:
    """
    Battleship class
    """
    sunk = False
    vertical = False
    vertical_size = 1
    horizontal_size = 1
    nodes = []
    def __init__(self, size):
        self.size = size
        self.horizontal_size = size
        self.nodes = np.array([Node(row, 0) for row in range(size)])
        #self.nodes = np.array([Node(0,0), Node(0,1), Node(0,2)])

    def print_location(self):
        return self.nodes
    
    def rotate_ship(self):
        for node in self.nodes:
            temp_row = node.return_row()
            temp_col = node.return_col()
            node.col = temp_row
            node.row = temp_col
        self.vertical = False if True else False
        self.horizontal_size = 1 if True else self.size
        self.vertical_size =  self.size if True else 0