import numpy as np
from node import Node
class Ship:
    """
    Battleship class
    """
    sunk = False
    vertical = True
    nodes = []
    def __init__(self, size):
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
battleship = Ship(3)
for node in battleship.nodes:
    print((node.location()))

battleship.rotate_ship()
for node in battleship.nodes:
    print((node.location()))
battleship.rotate_ship()
for node in battleship.nodes:
    print((node.location()))