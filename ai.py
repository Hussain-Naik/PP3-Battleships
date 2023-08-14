import random


class Ai:
    """
    AI Class
    """
    def __init__(self, player_fleet):
        # Variable for List of ships
        self.remaining_ships = player_fleet
        # Variable for List of sunk ships
        self.sunk_ships = []
        # Variable for set of computer hits
        self.all_hits = set()
        # Variable for list of computer successful hits
        self.successful_hits = []
        # Variable for list of computer relative positions from last hit
        self.precision_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # Variable to start fail counter
        self.start_counter = False
        # variable to increment miss hits after successful hit
        self.fail_counter = 0

    def remaining_ship_count(self):
        """
        Method to return number of remaining ships
        """
        return len(self.remaining_ships)

    def return_last_sunk_ship(self):
        """
        Method to return last sunk ship
        """
        return self.sunk_ships[len(self.sunk_ships) - 1]

    def update_sunk_ships(self):
        """
        Method to update sunk ship list
        """
        # Temporary list
        temp_ship_list = []
        # Loop through all remaining ships
        for ship in self.remaining_ships:
            if ship.sunk:
                # If ship is sunk append to sunk list
                self.sunk_ships.append(ship)
            else:
                # If ship is alive append to temp list
                temp_ship_list.append(ship)
        # Update remaining list to exclude sunk ships
        self.remaining_ships = temp_ship_list

    def update_hit_list(self):
        """
        Method to update successful hit list
        """
        # temp variable last sunk ship
        sunk_ship = self.return_last_sunk_ship()
        # Loop through all last sunk ship nodes
        for node in sunk_ship.nodes:
            # Remove all last sunk ship co ordinates
            self.successful_hits.remove((node.row, node.col))

    def add_hit_to_set(self, hit):
        """
        Method to add computer used hit to set
        """
        # Add to all_hits set
        self.all_hits.add(hit)
        # Call increment counter
        self.increment_counter()

    def add_successful_hit(self, hit):
        """
        Method to add successful hits
        """
        # Append hit to list
        self.successful_hits.append(hit)
        # Reset fail counter
        self.reset_counter()
        # Call update sunk ships method
        self.update_sunk_ships()

    def increment_counter(self):
        """
        Method to increment fail counter
        """
        if self.start_counter:
            self.fail_counter += 1

    def reset_counter(self):
        """
        Method to reset counter
        """
        self.start_counter = True
        self.fail_counter = 0

    def new_random_move(self):
        """
        Method to return AI random move
        """
        random_col = random.randint(0, 9)
        random_row = random.randint(0, 9)
        return (random_col, random_row)

    def new_calculated_move(self):
        """
        Method to return AI calculated move after successful hit
        """
        # Temporary variable for last item in successful hits list
        last_hit = self.successful_hits[-1]
        # Unpack tuple
        (last_x, last_y) = last_hit
        # Temporary loop variable
        i = 0
        while True:
            '''
            Unpack precision list item with index of loop variable +
            fail counter mod 4 to be within list index size
            '''

            (precision_x, precision_y) = self.precision_list[
                (self.fail_counter + i) % 4
                ]
            # Temporary tuple variable for new hit location
            check_hit = (precision_x + last_x, precision_y + last_y)
            # Unpack new hit location
            (check_x, check_y) = check_hit
            # Check if hit already in all hits list
            if check_hit in self.all_hits:
                # Increment loop variable
                i += 1
            # Check new hit col outside bounds
            elif 0 > check_x or check_x > 9:
                # Increment loop variable
                i += 1
            # Check new hit row outside bounds
            elif 0 > check_y or check_y > 9:
                # Increment loop variable
                i += 1
            else:
                return check_hit

    def new_seq_move(self):
        """
        Method for AI sequence move selection
        """
        # Variable for last successful hit
        last_hit = self.successful_hits[-1]
        # Variable for previous successful hit
        seq_hit = self.successful_hits[-2]
        # Unpack last hit tuple
        (last_x, last_y) = last_hit
        # Unpack previous hit tuple
        (seq_x, seq_y) = seq_hit
        '''
        Find direction in vertical axis as last hit y value - previous hit y
        value. Invert difference if fail counter > 0 as computer has missed
        after second successful hit
        '''
        dy = last_y - seq_y if self.fail_counter == 0 else seq_y - last_y
        '''
        Change vertical direction to be one of three values -1, 0, 1 by
        dividing by absolute value of vertical direction for any value that
        is not 0
        '''
        dy = 0 if dy == 0 else int(dy / abs(dy))
        '''
        Find direction in horizontal axis as last hit x value - previous hit x
        value. Invert difference if fail counter > 0 as computer has missed
        after second successful hit
        '''
        dx = last_x - seq_x if self.fail_counter == 0 else seq_x - last_x
        '''
        Change horizontal direction to be one of three values -1, 0, 1 by
        dividing by absolute value of horizontal direction for any value that
        is not 0
        '''
        dx = 0 if dx == 0 else int(dx / abs(dx))
        # Variable to check new hit x from last hit x value in bounds
        check_last_x_limit = last_x + dx >= 0 and last_x + dx <= 9
        # Variable to check new hit y from last hit y value in bounds
        check_last_y_limit = last_y + dy >= 0 and last_y + dy <= 9
        '''
        Result x set to last x value + the horizontal direction if new hit in
        bounds else result x set to previous x value - horizontal direction
        '''
        result_last_x = last_x + dx if check_last_x_limit else seq_x - dx
        '''
        Result y set to last y value + the vertical direction if new hit in
        bounds else result y set to previous y value - vertical direction
        '''
        result_last_y = last_y + dy if check_last_y_limit else seq_y - dy
        # Variable to check new hit result in all hits
        check_last_hit = (result_last_x, result_last_y) in self.all_hits
        # variable to check new hit result in successful hits
        check_last_larger_seq = (result_last_x,
                                 result_last_y) in self.successful_hits
        # Variable to check new hit x from previous hit x in bounds
        check_seq_x_limit = seq_x + dx >= 0 and seq_x + dx <= 9
        # Variable to check new hit y from previous hit y in bounds
        check_seq_y_limit = seq_y + dy >= 0 and seq_y + dy <= 9
        '''
        Sequence result x set to previous x value + the horizontal direction
        if new hit in bounds else result x set to last x value - horizontal
        direction
        '''
        result_seq_x = seq_x + dx if check_seq_x_limit else last_x - dx
        '''
        Sequence result y set to previous y value + the vertical direction if
        new hit in bounds else result y set to last y value - vertical
        direction
        '''
        result_seq_y = seq_y + dy if check_seq_y_limit else last_y - dy
        # Variable to check sequence hit result in all hits
        check_seq_hit = (result_seq_x, result_seq_y) in self.all_hits
        # Variable to check sequence hit result in successful hits
        check_seq_larger_seq = (result_seq_x,
                                result_seq_y) in self.successful_hits
        # Check if sequence is a vertical or horizontal
        if dx == 0 or dy == 0:
            # Check computer has not failed and move not done prior
            if self.fail_counter == 0 and not check_last_hit:
                return (result_last_x, result_last_y)
            # Check computer has not failed and larger ship placed on edge
            elif self.fail_counter == 0 and check_last_larger_seq:
                while check_last_larger_seq:
                    # increase in opposite direction
                    result_last_x -= dx
                    result_last_y -= dy
                    # Update loop condition
                    check_last_larger_seq = (
                                             result_last_x,
                                             result_last_y
                                             ) in self.successful_hits
                # Check if hit after larger sequence is a miss
                if (result_last_x, result_last_y) in self.all_hits:
                    return self.new_calculated_move()
                else:
                    return (result_last_x, result_last_y)
            # If computer has failed and reverse sequence direction new hit
            elif self.fail_counter > 0 and not check_seq_hit:
                return (result_seq_x, result_seq_y)
            # Check if computer has failed and larger ship adjacent to edge
            elif self.fail_counter > 0 and check_seq_larger_seq:
                while check_seq_larger_seq:
                    # increase in opposite direction
                    result_seq_x += dx
                    result_seq_y += dy
                    # Update loop condition
                    check_seq_larger_seq = (
                                            result_seq_x,
                                            result_seq_y
                                            ) in self.successful_hits
                # Check if hit after larger sequence is a miss
                if (result_seq_x, result_seq_y) in self.all_hits:
                    return self.new_calculated_move()
                else:
                    return (result_seq_x, result_seq_y)
            else:
                return self.new_calculated_move()
        else:
            return self.new_calculated_move()

    def new_move(self):
        """
        Method for AI new move
        """
        # Temporary tuple
        new_move = ()
        # Check if there any successful hits
        if len(self.successful_hits) == 0:
            # return random move if no successful hits
            new_move = self.new_random_move()
        elif len(self.successful_hits) == 1:
            # return calculated move if 1 successful hit
            new_move = self.new_calculated_move()
        else:
            # return sequence move
            new_move = self.new_seq_move()

        # Temporary loop variable as boolean if new move exists in hits set
        check = new_move in self.all_hits
        while check:
            # return new random move
            new_move = self.new_random_move()
            # Update loop variable
            check = new_move in self.all_hits

        return new_move
