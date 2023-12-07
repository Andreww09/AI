from Environment import Environment
from Q_Algorithm import Q_Algorithm

environment = Environment(7, 10, 3, 0, 3, 7, [0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
alg = Q_Algorithm(70, 4, 10000, 100, environment)
alg.learn()
