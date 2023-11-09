import copy

from State import State


class Game:
    def __init__(self):
        self.magic_square = [2, 7, 6, 9, 5, 1, 4, 3, 8]
        self.magic_square_index = [5, 0, 7, 6, 4, 2, 1, 8, 3]
        self.visited = [0] * 9
        self.state = State()
        self.winner = -1

    def move_is_valid(self, move):

        if move < 1 or move > 9:
            return False
        return self.visited[move - 1] == 0

    def is_final(self, state):

        player = state.get_last_player()
        moves = state.get_moves()

        if 0 not in moves:
            self.winner = 0
            return True

        self.winner = player

        for k in range(0, 3):
            # verific linia
            if moves[3 * k] == player and moves[3 * k] == moves[3 * k + 1] and moves[3 * k + 1] == moves[3 * k + 2]:
                return True
            # verific coloana
            if moves[k] == player and moves[k] == moves[3 + k] and moves[3 + k] == moves[6 + k]:
                return True
        # diagonala principala
        if moves[0] == player and moves[0] == moves[4] and moves[4] == moves[8]:
            return True
        # diagonala secundara
        if moves[2] == player and moves[2] == moves[4] and moves[4] == moves[6]:
            return True

        self.winner = -1
        return False

    def evaluate(self, state):
        player = state.get_last_player()
        moves = state.get_moves()

        scores = [0, 1, 10, 100]
        score = 0

        # verific liniile
        for i in range(0, 3):
            cnt_player = cnt_empty = 0
            for j in range(0, 3):
                if moves[3 * i + j] == player:
                    cnt_player += 1
                elif moves[3 * i + j] == 0:
                    cnt_empty += 1
            if cnt_player + cnt_empty == 3:
                score += scores[cnt_player]

        # verific coloanele
        for i in range(0, 3):
            cnt_player = cnt_empty = 0
            for j in range(0, 3):
                if moves[3 * j + i] == player:
                    cnt_player += 1
                elif moves[3 * j + i] == 0:
                    cnt_empty += 1
            if cnt_player + cnt_empty == 3:
                score += scores[cnt_player]

        # diagonala principala
        cnt_player = cnt_empty = 0
        for i in range(0, 3):
            if moves[3 * i + i] == player:
                cnt_player += 1
            elif moves[3 * i + i] == 0:
                cnt_empty += 1
        if cnt_player + cnt_empty == 3:
            score += scores[cnt_player]

        # diagonala secundara
        cnt_player = cnt_empty = 0
        for i in range(0, 3):
            if moves[3 * i + 2 - i] == player:
                cnt_player += 1
            elif moves[3 * i + 2 - i] == 0:
                cnt_empty += 1
        if cnt_player + cnt_empty == 3:
            score += scores[cnt_player]

        return score

    def get_possible_values(self, state):
        moves = state.get_moves()
        values = []
        for i in range(0, len(moves)):
            if moves[i] == 0:
                values.append(self.magic_square[i])
        return values

    def minimax(self, depth, maximizing_player, state):
        if depth == 0 or self.is_final(state):
            return self.evaluate(state)
            # return -1 if maximizing_player else 1

        current_state = copy.deepcopy(state)
        if maximizing_player:
            max_eval = float('-inf')
            for value in self.get_possible_values(current_state):
                current_state.move(2, self.magic_square_index[value - 1])
                eval = self.minimax(depth-1, False, current_state)
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for value in self.get_possible_values(current_state):
                current_state.move(1, self.magic_square_index[value - 1])
                eval = self.minimax(depth - 1, True, current_state)
                min_eval = min(min_eval, eval)
            return min_eval

    def ai_move(self):
        best_move = None
        max_eval = float('-inf')
        current_state = copy.deepcopy(self.state)
        for value in self.get_possible_values(current_state):
            current_state.move(2, self.magic_square_index[value - 1])
            eval = self.minimax(1, False, self.state)
            if eval > max_eval:
                max_eval = eval
                best_move = value
        return best_move

    def start(self):

        player = 1
        while self.is_final(self.state) is False:
            print("Player", player, "'s turn")
            if player == 1:
                move = int(input())
                if self.move_is_valid(move) is False:
                    print("Invalid move")
                    continue
            else:
                move = self.ai_move()
                print(f"AI choose {move}")

            self.state.move(player, self.magic_square_index[move - 1])
            self.visited[move - 1] = 1
            player = 3 - player

        if self.winner == 0:
            print("Tie")
        else:
            print("Player", self.winner, "won!")
