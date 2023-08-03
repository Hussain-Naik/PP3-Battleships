class Node:
    """
    Node Class
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.occupied = False
        self.used = False
        self.view = False
    def __str__(self):
        if self.view:
            return "+"
        elif self.used:
            return "0"
        elif self.used and self.occupied:
            return "X"
        return "-"
    def is_used(self):
        return self.used
    
    def make_used(self):
        self.used = True

    def make_unused(self):
        self.used = False
    
    def view(self):
        self.view = True
    def hidden(self):
        self.view = False

    def is_occupied(self):
        return self.occupied

    def occupy(self):
        self.occupied = True