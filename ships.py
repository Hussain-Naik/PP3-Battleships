import random
from node import Node


class Ship:
    """
    Battleship class
    """
    sunk = True
    vertical = True
    vertical_size = 1
    horizontal_size = 1
    nodes = []
    name = ""

    def __init__(self, size):
        # Size of the ship
        self.size = size
        # Set horizontal size for checking end collision
        self.vertical_size = size
        # Set temporary nodes for ship
        self.nodes = [Node(0, x) for x in range(size)]
        # Set ship sunk boolean based of all node used variable
        self.sunk = all([node.used for node in self.nodes])
        self.name = self.name_ship()

    def __str__(self):
        # override str method to display ship type as string.
        if self.sunk:
            return ("\u0336".join(self.name) + "\u0336"
                    + " " * (11 - len(self.name)))
        else:
            return self.name + " " * (11 - len(self.name))

    def name_ship(self):
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

    def display_sunk_ship(self):
        """
        Method to set ship nodes to first letter of ship name
        """
        if self.sunk is True:
            for node in self.nodes:
                node.name = self.name[0]

    def rotate_ship(self):
        """
        Rotate method for ship
        """
        for node in self.nodes[1:]:
            # Assign temporary variables
            temp_row = node.return_row()
            temp_col = node.return_col()
            # Invert row and col
            node.col = temp_row
            node.row = temp_col

        self.change_vertical_status()

    def change_vertical_status(self):
        """
        Method to change vertical status
        """
        # Change vertical status
        self.vertical = not self.vertical
        # store ship current sizes as temp
        (temp_horizontal, temp_vertical) = self.return_size()
        # Switch Vertical and horizontal sizes
        self.vertical_size = temp_horizontal + 1
        self.horizontal_size = temp_vertical + 1

    def manual_ship_rotation(self):
        """
        Method to return new list of nodes after rotation
        """
        # Temporary list
        new_list = []
        # Append first node as pivot point for rotation
        new_list.append(self.nodes[0])
        # variable to store first node column value
        col = self.nodes[0].return_col()
        # variable to store first ndoe row value
        row = self.nodes[0].return_row()
        # variable to unpack tuple of ship size
        (col_size, row_size) = self.return_size()
        # Loop through remaining nodes of ship
        for x, node in enumerate(self.nodes[1:]):
            # Check if ship is vertical or horizontal 
            if col_size < row_size:
                new_list.append(Node(row + x + 1, col))
            else:
                new_list.append(Node(row, col + x + 1))
        # Return temporary list
        return new_list

    def update_status(self):
        """
        Update ship sunk status
        """
        self.sunk = all([node.used for node in self.nodes])
        self.display_sunk_ship()

    def assign_ship_to_board(self, board):
        """
        Add board nodes to ship so ship
        nodes reference same board node
        """
        # Temporary list
        placed_nodes = []

        # loop through all nodes
        for node in self.nodes:
            # Add board node with node col and row to temp list
            placed_nodes.append(board[node.col][node.row])
        # Save node list with temporary list
        self.nodes = placed_nodes

    def is_ship_placed(self):
        """
        Method to return if ship has been placed on board
        """
        return all([node.occupied for node in self.nodes])

    def confirm_placement(self):
        """
        Set all ship nodes to occupied variable to True
        """
        # Loop through all ship nodes
        for node in self.nodes:
            # Call node occupy method
            node.occupy()

    def assign_to_player(self):
        """
        Set all ship nodes to occupied variable to True
        """
        # Loop through all ship nodes
        for node in self.nodes:
            # Call node occupy method
            node.set_players()

    def return_node_set(self):
        """
        Method to return ship nodes as set
        """
        # Temporary set of node 
        node_set = set()
        # Loop through all nodes
        for node in self.nodes:
            # Add node row, col tuple values to set
            node_set.add(node.location())

        return node_set

    def set_random_position(self):
        """
        Method for random ship placement
        """
        # Reset ship
        self.reset_ship()
        # Randomly chose to rotate 
        random_rotate = random.randint(0, 1)
        if random_rotate == 0:
            self.rotate_ship()
        # Randomly assign new position for ship nodes
        (x, y) = self.return_size()
        random_col = random.randint(0, 9 - y)
        random_row = random.randint(0, 9 - x)
        for node in self.nodes:
            node.col += random_col
            node.row += random_row

    def return_size(self):
        """
        Method to return ship size as tuple
        """
        # Return ship dimensions with respective size -1
        return (self.horizontal_size - 1, self.vertical_size - 1)

    def reset_ship(self):
        """
        Method to reset ship position and status
        """
        for x in range(0, self.size):
            self.nodes[x].reset_node()
            self.nodes[x] = Node(x, 0)
        self.horizontal_size = len(self.nodes)
        self.vertical = False
        self.vertical_size = 1
