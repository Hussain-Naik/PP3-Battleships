class Node:
    """
    Node Class
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.occupied = False
        self.used = False
    
    def is_used(self):
        return self.used
    
    def make_used(self):
        self.used = True
    
    def is_occupied(self):
        return self.occupied

    def occupy(self):
        self.occupied = True