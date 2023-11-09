class State:
    def __init__(self):
        self.moves = [0] * 9
        self.player = -1

    def move(self, player, pos):
        self.moves[pos] = player
        self.player = player

    def get_last_player(self):
        return self.player

    def get_moves(self):
        return self.moves
