class Node:
    """
    Node Class
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.occupied = False
        self.used = False
    def __str__(self):
        if self.occupied:
            return "X"
        elif self.used:
            return "0"
        return "-"
    def is_used(self):
        return self.used
    
    def make_used(self):
        self.used = True
    def make_unused(self):
        self.used = False
    def is_occupied(self):
        return self.occupied

    def occupy(self):
        self.occupied = True