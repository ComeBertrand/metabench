import random
import math


def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequence of unequal length")
    return sum([el1 != el2 for el1, el2 in zip(s1, s2)])


def manhattan_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequence of unequal length")
    return sum([abs(el1 - el2) for el1, el2 in zip(s1, s2)])


def euclidian_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequence of unequal length")
    return math.sqrt(sum([abs(el1 - el2) ** 2 for el1, el2 in zip(s1, s2)]))


class Encoding(object):
    pass


class BinaryEncoding(Encoding):
    def __init__(self, size):
        super().__init__()
        self.size = size

    def generate_random_solution(self):
        sol = []
        for i in range(self.size):
            sol.append(random.randint(0, 1))
        return sol

    def space_size(self):
        return 2 ** self.size

    def distance(self, solution_1, solution_2):
        return hamming_distance(solution_1, solution_2)


class DiscreteEncoding(Encoding):
    def __init__(self, boundaries):
        super().__init__()
        self.boundaries = boundaries

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            sol.append(random.randint(self.boundaries[i][0],
                                      self.boundaries[i][1]))
        return sol

    def space_size(self):
        size = 1.
        for i in range(len(self.boundaries)):
            size *= len(range(self.boundaries[i][0], self.boundaries[i][1]))
        return size

    def distance(self, solution_1, solution_2):
        return manhattan_distance(solution_1, solution_2)


class RealVector(Encoding):
    def __init__(self, boundaries):
        super().__init__()
        self.boundaries = boundaries

    def generate_random_solution(self):
        sol = []
        for i in range(len(self.boundaries)):
            sol.append(random.uniform(self.boundaries[i][0],
                                      self.boundaries[i][1]))
        return sol

    def space_size(self):
        return None

    def distance(self, solution_1, solution_2):
        return euclidian_distance(solution_1, solution_2)


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
                sol.append(random.randint(0, 1))
            elif self.types[i] is int:
                sol.append(random.randint(self.boundaries[i][0],
                                          self.boundaries[i][1]))
            elif self.types[i] is float:
                sol.append(random.uniform(self.boundaries[i][0],
                                          self.boundaries[i][1]))
            elif self.types[i] is list:
                sol.append(random.choice(self.boundaries[i]))
            elif self.types[i] is str:
                sol.append(random.choice(self.boundaries[i]))
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
