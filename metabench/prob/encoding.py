import random
import math

import numpy as np

import metabench.misc.distances as dist


class Encoding(np.ndarray):
    pass


class BinaryEncoding(Encoding):
    def __init__(self, size, distance=dist.hamming_distance):
        super().__init__()
        self.size = size
        self.distance = distance

    def generate_random_solution(self):
        return np.random.randint(2, size=self.size)

    def space_size(self):
        return 2 ** self.size

    def distance(self, solution_1, solution_2):
        return self.distance(solution_1, solution_2)


class DiscreteEncoding(Encoding):
    def __init__(self, boundaries, distance=dist.manhattan_distance):
        super().__init__()
        self.boundaries = boundaries
        self.distance = distance

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            sol.append(np.random.randint(self.boundaries[i][0],
                                         self.boundaries[i][1]))
        return sol

    def space_size(self):
        size = 1.
        for i in range(len(self.boundaries)):
            size *= (self.boundaries[i][1] - self.boundaries[i][0]) + 1
        return size

    def distance(self, solution_1, solution_2):
        return self.distance(solution_1, solution_2)


class RealVector(Encoding):
    def __init__(self, boundaries, distance=dist.euclidian_distance):
        super().__init__()
        self.boundaries = boundaries
        self.distance = distance

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            sol.append(np.random.uniform(self.boundaries[i][0],
                                         self.boundaries[i][1]))
        return sol

    def space_size(self):
        return None

    def distance(self, solution_1, solution_2):
        return self.distance(solution_1, solution_2)


class PermutationEncoding(Encoding):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def generate_random_solution(self):
        sol = self.items[:]
        random.shuffle(sol)
        return sol

    def space_size(self):
        return math.factorial(len(self.items))


class MixedEncoding(Encoding):
    def __init__(self, boundaries, types):
        super().__init__()
        self.boundaries = boundaries
        self.types = types

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            if self.types[i] is bool:
                sol.append(np.random.randint(2))
            elif self.types[i] is int:
                sol.append(np.random.randint(self.boundaries[i][0],
                                             self.boundaries[i][1]))
            elif self.types[i] is float:
                sol.append(np.random.uniform(self.boundaries[i][0],
                                             self.boundaries[i][1]))
            elif self.types[i] is list:
                sol.append(np.random.choice(self.boundaries[i]))
            elif self.types[i] is str:
                sol.append(np.random.choice(self.boundaries[i]))
            else:
                raise TypeError("Unknown type of variable at index {:d} : \
                                {}".format(i, self.types[i]))
        return sol

    def space_size(self):
        if float in self.types:
            return None

        size = 1.
        for i in range(len(self.boundaries)):
            if self.types[i] is bool:
                size *= 2
            elif self.types[i] is int:
                size *= len(range(self.boundaries[i][0],
                                  self.boundaries[i][1]))
            else:
                size *= len(self.boundaries[i])
        return size
