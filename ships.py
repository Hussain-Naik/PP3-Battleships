import numpy as np
import random
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

    def __str__(self):
        # override str method to display ship type as string.
        if len(self.nodes) == 5:
            return "Carrier"
        elif len(self.nodes) == 4:
            return "Battleship"
        elif len(self.nodes) == 3:
            return "Destroyer"
        elif len(self.nodes) == 2:
            return "Submarine"
        else:
            return "Patrol Boat"
    
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
        """
        Add board nodes to ship so ship
        nodes reference same board node 
        """
        #Temporary list
        placed_nodes = []

        #loop through all nodes
        for node in self.nodes:
            #Add board node with node col and row to temp list
            placed_nodes.append(board[node.col][node.row])
        #Save node list with temporary list
        self.nodes = placed_nodes

    def confirm_placement(self):
        """
        Set all ship nodes to occupied variable to True
        """
        #Loop through all ship nodes
        for node in self.nodes:
            #Call node occupy method
            node.occupy()
    
    def return_node_set(self):
        node_set = set()
        for node in self.nodes:
            node_set.add(node.location())
        
        return node_set

    def set_random_position(self):
        self.reset_ship()
        random_rotate = random.randint(0,1)
        if random_rotate == 0:
            self.rotate_ship()
            print("rotated ship")
        
        (x,y) = self.return_size()
        random_col = random.randint(0, 9 - y)
        random_row = random.randint(0, 9 - x)
        print(random_col, random_row)
        for node in self.nodes:
            node.col += random_col
            node.row += random_row

    def return_size(self):
        """
        Method to return ship size as tuple
        """
        #Return ship dimensions with respective size -1
        return (self.horizontal_size -1, self.vertical_size -1)
    
    def reset_ship(self):
        for x in range(0 ,self.size):
            self.nodes[x].col = 0
            self.nodes[x].row = x
        self.horizontal_size = len(self.nodes)
        self.vertical = False
        self.vertical_size = 1