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
        self.precision_list = [(1,0), (0,1), (-1,0), (0,-1)]
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
        self.reset_counter()

    def increment_counter(self):
        if self.start_counter:
            self.fail_counter += 1

    def reset_counter(self):
        self.start_counter = True
        self.fail_counter = 0
    
    def new_random_move(self):
        random_col = random.randint(0, 9)
        random_row = random.randint(0, 9)
        return (random_col, random_row)

    def new_calculated_move(self):
        last_hit = self.successful_hits[len(self.successful_hits) -1]
        (last_x, last_y) = last_hit
        i = 0
        while True:
            print(f'start loop {i}')
            (precision_x, precision_y) = self.precision_list[(self.fail_counter + i) % 4]
            check_hit = (precision_x + last_x, precision_y + last_y)
            (check_x, check_y) = check_hit
            print(f'check x:{check_x} check y:{check_y}')
            if check_hit in self.all_hits:
                i += 1
            elif 0 > check_x or  check_x > 9 :
                i += 1
            elif 0 > check_y or check_y > 9 :
                i += 1
            else:
                return check_hit
    
    def new_sequence_move(self):
        last_hit = self.successful_hits[len(self.successful_hits) -1]
        sequence_hit = self.successful_hits[len(self.successful_hits) -2]
        (last_x, last_y) = last_hit
        (sequence_x, sequence_y) = sequence_hit
        dy = last_y - sequence_y if self.fail_counter == 0 else sequence_y - last_y
        dy = 0 if dy == 0 else int(dy / abs(dy))
        dx = last_x - sequence_x if self.fail_counter == 0 else sequence_x - last_x
        dx = 0 if dx == 0 else int(dx / abs(dx))
        check_last_x_limit = last_x + dx >= 0 and last_x + dx <= 9
        check_last_y_limit = last_y + dy >= 0 and last_y + dy <= 9
        result_last_x = last_x + dx if check_last_x_limit else sequence_x -dx
        result_last_y = last_y + dy if check_last_y_limit else sequence_y -dy
        check_last_hit = (result_last_x, result_last_y) in self.all_hits

        check_seq_x_limit = sequence_x + dx >= 0 and sequence_x + dx <= 9
        check_seq_y_limit = sequence_y + dy >= 0 and sequence_y + dy <= 9
        result_seq_x = sequence_x + dx if check_seq_x_limit else last_x -dx
        result_seq_y = sequence_y + dy if check_seq_y_limit else last_y -dy
        check_seq_hit = (result_seq_x, result_seq_y) in self.all_hits
        print(f'result seq x:{result_seq_x} y:{result_seq_y}')
        if dx == 0 or dy == 0:
            if self.fail_counter == 0 and not check_last_hit:
                return (result_last_x, result_last_y)
            elif self.fail_counter > 0 and not check_seq_hit:
                return (result_seq_x, result_seq_y)
            else:
                return self.new_calculated_move()
        else:
            return self.new_calculated_move()
        


    def new_move(self):
        new_move = ()
        if len(self.successful_hits) == 0:
            new_move = self.new_random_move()
        elif len(self.successful_hits) == 1:
            new_move = self.new_calculated_move()
        else:
            new_move = self.new_sequence_move()

        check = new_move in self.all_hits
        while check:
            new_move = self.new_random_move()
            check = new_move in self.all_hits

        return new_move

computer = Ai('fleet')
computer.add_successful_hit((0,0))
computer.add_successful_hit((0,1))
computer.add_hit_to_set((0,2))
computer.add_hit_to_set((0,0))
computer.fail_counter = 1
computer.add_hit_to_set((1,5))
computer.add_hit_to_set((2,4))
move = computer.new_move()
print(move)