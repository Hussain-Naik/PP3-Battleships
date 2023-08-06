class Ai:
    """
    AI Class
    """
    def __init__(self, player_fleet):
        self.remaining_ships = player_fleet
        self.sunk_ships = []
        self.all_hits = set()
        self.successful_hits = []
        self.fail_counter = 0
