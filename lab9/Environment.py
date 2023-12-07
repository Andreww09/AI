import random


class Environment:
    def __init__(self, n, m, x0, y0, xn, yn, wind):
        self.n = n
        self.m = m
        self.x0 = x0
        self.y0 = y0
        self.xn = xn
        self.yn = yn
        self.wind = wind
        self.actions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.viz = [] * n
        for i in range(0, n):
            self.viz.append([0] * m)

    def get_possible_actions(self, x, y):
        possible_acts = []
        for poz, (i, j) in enumerate(self.actions):
            if 0 <= x + i < self.n and 0 <= y + j < self.m and self.viz[x + i][y + j] == 0:
                possible_acts.append(poz)
        return possible_acts

    def random_action(self, x, y):
        acts = self.get_possible_actions(x, y)
        if len(acts) == 0:
            return -1
        return random.choice(acts)

    def get_transition(self, x, y):
        if x == self.xn and y == self.yn:
            return True, 100
        return False, -1

    def reset(self):
        for i in range(0, self.n):
            for j in range(0, self.m):
                self.viz[i][j] = 0
        return self.x0, self.y0
