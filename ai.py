import random

class Ai:
    """
    AI Class
    """
    def __init__(self, player_fleet):
        self.remaining_ships = player_fleet
        self.sunk_ships = []
        self.all_hits = set()
        self.successful_hits = []
        self.start_counter = False
        self.fail_counter = 0

    def return_last_sunk_ship(self):
        return self.sunk_ships[len(self.sunk_ships) -1]
    
    def update_sunk_ships(self):
        temp_ship_list = []
        for ship in self.remaining_ships:
            if ship.sunk:
                self.sunk_ships.append(ship)
            else:
                temp_ship_list.append(ship)
        
        self.remaining_ships = temp_ship_list
    
    def add_hit_to_set(self, hit):
        self.all_hits.add(hit)
    
    def add_successful_hit(self, hit):
        self.successful_hits.append(hit)

    def increment_counter(self):
        if self.start_counter:
            self.fail_counter += 1

    def reset_counter(self):
        self.start_counter = False
        self.fail_counter = 0
    
    def new_random_move(self):
        random_col = random.randint(0, 9)
        random_row = random.randint(0, 9)
        return (random_col, random_row)

    def new_calculated_move(self):
        return (0,0)

    def new_move(self):
        new_move = ()
        if len(self.successful_hits) == 0:
            new_move = self.new_random_move()
        else:
            new_move = self.new_calculated_move()
        check = new_move in self.all_hits
        while check:
            new_move = self.new_random_move()
            check = new_move in self.all_hits

        return new_move