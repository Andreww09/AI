import random


class Q_Algorithm:
    def __init__(self, n, m, episodes, iterations, environment, lr=0.1, eps=1, min_eps=0.01, decay=0.05, gamma=0.99):
        # nr de pozitii posibile din grid 7*10
        self.observations = n
        # 4 actiuni posibile
        self.actions = m

        self.Qtable = [] * n
        for i in range(0, n):
            self.Qtable.append([0] * m)

        self.lr = lr
        # nr total de episoade de antrenare
        self.episodes = episodes
        # maximul de pasi intr-un episod
        self.iterations = iterations
        # mediul va verifica actiunile posibile si va acorda recompense
        self.environment = environment
        # epsilon pentru explorare-exploatare
        self.eps = eps
        # epssilon nu o sa scada mai mult de min_eps
        self.min_eps = min_eps
        # cu cat scade epsilon
        self.decay = decay
        self.gamma = gamma

    def best_action(self, x, y, state):
        # returneaza indicele celei mai bune actiuni sau -1 daca nu are actiuni posibile
        argmax = float('-inf')
        best_action = -1
        for act in self.environment.get_possible_actions(x, y):
            if self.Qtable[state][act] > argmax:
                argmax = self.Qtable[state][act]
                best_action = act
        return best_action

    # fiecare pozitie din grid va avea un numar/state propriu
    def get_state(self, x, y):
        return x * self.environment.m + y

    # returneaza urmatoarea pozitie stiind pozitia curenta si actiunea
    def get_next(self, x, y, action):
        i, j = self.environment.actions[action]
        x += i
        y += j
        return x, y

    def learn(self):

        total_rewards = []
        for i in range(0, self.episodes):
            x_current, y_current = self.environment.reset()
            steps = []
            total_reward = 0

            for j in range(0, self.iterations):
                steps.append((x_current, y_current))

                current_state = self.get_state(x_current, y_current)

                if random.random() < self.eps:
                    # explorare
                    action = self.environment.random_action(x_current, y_current)
                else:
                    #exploatare
                    action = self.best_action(x_current, y_current, current_state)

                x_next, y_next = self.get_next(x_current, y_current, action)
                next_state = self.get_state(x_next, y_next)

                # recompensa daca trecem in urmatoarea pozitie aleasa
                end, reward = self.environment.get_transition(x_next, y_next)

                # actualizare Qtable
                self.Qtable[current_state][action] = self.Qtable[current_state][action] + self.lr * (
                        reward + self.gamma * max(self.Qtable[next_state]) -
                        self.Qtable[current_state][action])
                # trece in pozitia urmatoare
                x_current = x_next
                y_current = y_next

                total_reward += reward
                self.eps = max(self.min_eps,self.eps-self.decay)
                if end:
                    break

            total_rewards.append(total_reward)
            if (i+1)%1000==0:
                print(steps)
        for i in range(0, len(total_rewards)):
            if (i + 1) % 1000 == 0:
                print(f"{i}: {total_rewards[i]}")

