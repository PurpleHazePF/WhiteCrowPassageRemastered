from random import randint


class ParcheesiDialecto:
    def __init__(self, player0=True, player1=True, player2=True, player3=True, chips_quantity=3, board_len=48,
                 total_cycles=1,
                 auto_start_positions=True):
        self.chips_quantity = chips_quantity
        self.members_quantity = 0
        self.board_len = board_len
        self.total_cycles = total_cycles
        self.players_info = {
            0: {'start_position': 0, 'allowed': player0, 'active_chips': [],
                'nonactive_chips': [*range(0, self.chips_quantity)],
                'finished_chips': []},
            1: {'start_position': 0, 'allowed': player1, 'active_chips': [],
                'nonactive_chips': [*range(0, self.chips_quantity)],
                'finished_chips': []},
            2: {'start_position': 0, 'allowed': player2, 'active_chips': [],
                'nonactive_chips': [*range(0, self.chips_quantity)],
                'finished_chips': []},
            3: {'start_position': 0, 'allowed': player3, 'active_chips': [],
                'nonactive_chips': [*range(0, self.chips_quantity)],
                'finished_chips': []}}
        if auto_start_positions:
            for i in range(4):
                if self.players_info[i]['allowed']:
                    self.members_quantity += 1
                    for j in range(self.chips_quantity):
                        self.players_info[i][j] = [-1, 0]
                    self.players_info[i]['start_position'] = self.board_len // 4 * i
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.dice_val = 0
        self.current_turn = 0
        self.winner = None

    def dice_roll(self):
        return randint(1, 6)

    def chip_activate(self, chip_number, player=-1):
        if player < 0:
            player = self.current_turn
        self.players_info[player]['active_chips'].append(chip_number)
        self.players_info[player]['nonactive_chips'].remove(chip_number)

    def chip_finish(self, chip_number, player=-1):
        self.players_info[player]['finished_chips'].append(chip_number)
        self.players_info[player]['active_chips'].remove(chip_number)
        self.players_info[player][chip_number][0] = -1

    def chip_kill(self, chip_number, player):
        self.players_info[player]['active_chips'].remove(chip_number)
        self.players_info[player]['nonactive_chips'].append(chip_number)
        self.players_info[player][chip_number][0] = -1

    def turn_skip(self):
        while True:
            if self.current_turn > 2:
                self.current_turn = 0
            else:
                self.current_turn += 1
            if self.players_info[self.current_turn]['allowed']:
                break

    def finish_check(self, chip_number, steps, player=-1):
        if player < 0:
            player = self.current_turn
        predict_position = self.players_info[player][chip_number][0] + steps
        if predict_position >= self.players_info[player]['start_position'] and self.players_info[player][chip_number][
            1] >= self.total_cycles:
            return True
        else:
            return False

    def winner_check(self, player=-1):
        if player < 0:
            player = self.current_turn
        if len(self.players_info[player]['finished_chips']) == self.chips_quantity:
            self.winner = player
        return self.winner

    def turn(self, chip_number, steps, turn_skip=False, player=-1):
        if player < 0:
            player = self.current_turn
        if turn_skip:
            self.turn_skip()
        else:
            if self.players_info[player][chip_number][0] < 0:
                chip_val = self.kill_check(self.players_info[player]['start_position'], player=player)
                if chip_val:
                    self.chip_kill(chip_val[1], chip_val[0])
                self.players_info[player][chip_number][0] = self.players_info[player]['start_position']

                self.chip_activate(chip_number, player)
            else:
                if self.players_info[player][chip_number][0] + steps >= self.board_len:
                    self.players_info[player][chip_number][1] += (self.players_info[player][
                                                                      chip_number][0] + steps) // self.board_len
                    chip_val = self.kill_check((self.players_info[player][
                                                    chip_number][0] + steps) % self.board_len, player=player)
                    if chip_val:
                        self.chip_kill(chip_val[1], chip_val[0])
                    self.players_info[player][chip_number][0] = (self.players_info[player][
                                                                     chip_number][0] + steps) % self.board_len
                else:
                    chip_val = self.kill_check(self.players_info[player][chip_number][0] + steps, player=player)
                    if chip_val:
                        self.chip_kill(chip_val[1], chip_val[0])
                    self.players_info[player][chip_number][0] += steps
            if self.finish_check(chip_number, 1, player):
                self.chip_finish(chip_number, player)
            self.winner_check(player)
            self.turn_skip()

    def turn_check(self, chip_number, steps, player=-1):
        if player < 0:
            player = self.current_turn
        if chip_number in self.players_info[player]['finished_chips']:
            return False
        chips = [*range(self.chips_quantity)]
        chips.remove(1)
        if chip_number in self.players_info[player]['nonactive_chips']:
            predict_position = self.players_info[player]['start_position']
        else:
            if self.players_info[player][chip_number][0] + steps >= self.board_len:
                predict_position = self.players_info[player][chip_number][0] = (self.players_info[player][
                                                                                    chip_number][
                                                                                    0] + steps) % self.board_len
            else:
                predict_position = self.players_info[player][chip_number][0] + steps
        for i in chips:
            if self.players_info[player][i] == predict_position:
                return False
        return True

    def kill_check(self, predict_position, player=-1):
        if player < 0:
            player = self.current_turn
        if not self.players_info[player]['allowed']:
            return False
        for i in range(4):
            if self.players_info[i]['allowed'] and self.players_info[i] != self.players_info[player]:
                for j in range(self.chips_quantity):
                    if self.players_info[i][j][0] == predict_position:
                        return (i, j)
        return False