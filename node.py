class Node:
    """
    Node Class
    """
    def __init__(self, row, col):
        # Row and Column position of node
        self.row = row
        self.col = col
        # variable for ship placement
        self.occupied = False
        # variable for used attack position
        self.used = False
        # Variable for grid position selection
        self.view = False
        # Variable for assigned to player ships
        self.player = False
        # Variable for initial display on board
        self.name = 'X'

    def __str__(self):
        # override str method to display node as string.
        if self.used and self.occupied:
            # board to display X if Hit and occupied
            return self.name
        elif self.player:
            # board to display + when selecting grid position
            return "@"
        elif self.view:
            # board to display + when selecting grid position
            return "+"
        elif self.used:
            # board to display 0 when missed
            return "0"
        # board default available grid positions displayed as -
        return "-"

    def location(self):
        """
        method for testing node positions
        """
        return f"{self.col}, {self.row}"

    def reset_node(self):
        """
        method to reset node status
        """
        # variable for ship placement
        self.occupied = False
        # variable for used attack position
        self.used = False
        # Variable for grid position selection
        self.view = False
        # Variable for assigned to player ships
        self.player = False

    def is_used(self):
        """
        method to access used variable
        """
        return self.used

    def make_used(self):
        """
        Method to change used to True
        """
        self.used = True

    def set_view(self):
        """
        Method to change view variable to True
        """
        self.view = True

    def set_hidden(self):
        """
        Method to reset view variable to False
        """
        self.view = False

    def set_players(self):
        """
        Method to set node is assigned to player
        """
        self.player = True

    def is_occupied(self):
        """
        Method to access variable occupied
        """
        return self.occupied

    def occupy(self):
        """
        Method to set variable occupied to True
        """
        self.occupied = True

    def return_row(self):
        """
        method to access variable row
        """
        return self.row

    def return_col(self):
        """
        Method to access variable col
        """
        return self.col
