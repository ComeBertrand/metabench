"""
File: continuous.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Classical continuous functions for performance evaluation of
metaheuristics. All theses functions were taken from the following website :
https://www.sfu.ca/~ssurjano/optimization.html
"""

import numpy as np

from metabench.algorithmic.problem.abstract import Problem
from metabench.common.representation import RealEncoding, Boundaries
from metabench.common.fitness import Objective
from metabench.algorithmic.operators.neighborhood import (NeighborhoodGenerator, move_distance_continuous,
                                                          ContinuousLogMoveRange)


class ContinuousProblem(Problem):
    """Problems that are defined by a continuous function.

    # TODO: Do it in a more abstract way and move it in abstract

    Args:
        n_dim (int): Number of dimensions.
        min_vals (np.array): Minimum values for each dimension.
        max_vals (np.array): Maximum values for each dimension.
        move_range (MoveRange): Range of the move step.
        known_min (float): Minimum of the continuous function. None means that
            the minimum is not known.

    """
    def __init__(self, n_dim, min_vals, max_vals, move_range, known_min):
        nb_neighbors = n_dim * 100 # TODO: shall be an argument of the object
        neighborhood = NeighborhoodGenerator(move_distance_continuous, move_range, nb_neighbors)
        boundaries = Boundaries(min_vals, max_vals, np.float)
        encoding = RealEncoding(boundaries)
        objective = Objective(self._eval_func)

        super().__init__(objective, encoding, neighborhood=neighborhood, known_min=known_min)

    def _eval_func(self, solution):
        """Actual evaluation of a solution by the continuous function.

        Args:
            solution (Solution): Solution to be evaluated.

        Returns:
            float: function value of the solution.

        """
        raise NotImplementedError("Abstract Class")


# --------------------------------------------------------------------------- #
#                      Functions with many local minima                       #
# --------------------------------------------------------------------------- #


class Ackleys(ContinuousProblem):
    """Ackley's function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-32.768] * n_dim, np.float)
        max_vals = np.array([32.768] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        part1 = -0.2 * np.sqrt(1/n * np.sum(solution * solution))
        part2 = 1/n * np.sum(np.cos(2 * np.pi * solution))
        return 20 - 20 * np.exp(part1) + np.e - np.exp(part2)


class Bukin6(ContinuousProblem):
    """Bukin funtion N.6."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-15.0, -3.0], np.float)
        max_vals = np.array([-5.0, 3.0], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        part1 = np.abs(solution[1] - 0.01 * solution[0] * solution[0])
        part2 = np.abs(solution[0] + 10)
        return 100 * np.sqrt(part1) + 0.01 * part2


class CrossInTray(ContinuousProblem):
    """Cross-in-tray function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-10.0, -10.0], np.float)
        max_vals = np.array([10.0, 10.0], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = -2.06261
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        part1 = np.abs(100 - np.sqrt(np.sum(solution * solution)) / np.pi)
        part2 = np.sin(solution[0]) * np.sin(solution[1])
        final = np.abs(part2 * np.exp(part1)) + 1.0
        return -0.0001 * np.power(final, 0.1)


class DropWave(ContinuousProblem):
    """Drop-Wave function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-5.12, -5.12], np.float)
        max_vals = np.array([5.12, 5.12], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = -1.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        sum_sol_sq = np.sum(solution * solution)
        part1 = 1.0 + np.cos(12 * np.sqrt(sum_sol_sq))
        part2 = 0.5 * sum_sol_sq + 2.0
        return -1.0 * (part1 / part2)


class Eggholder(ContinuousProblem):
    """Eggholder function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-512, -512], np.float)
        max_vals = np.array([512, 512], np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.0)
        known_min = -959.6407
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        part1 = np.sin(np.sqrt(np.abs(solution[1] + (solution[0]/2.) + 47)))
        part2 = np.sin(np.sqrt(np.abs(solution[0] - (solution[1] + 47))))
        return -1.0 * (solution[1] + 47) * part1 - 1.0 * part2


class GramacyLee(ContinuousProblem):
    """Gramacy & Lee function."""
    def __init__(self):
        n_dim = 1
        min_vals = np.array([0.5], np.float)
        max_vals = np.array([2.5], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = None
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        part1 = np.sin(10 * np.pi * solution[0]) / (2 * solution[0])
        part2 = np.power(solution[0] - 1.0, 4)
        return part1 + part2


class Griewank(ContinuousProblem):
    """Griewank function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-600] * n_dim, np.float)
        max_vals = np.array([600] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        part1 = np.sum((solution * solution) / 4000.0)
        sqrt = np.array([np.sqrt(i) for i in range(len(solution))], np.float)
        part2 = np.prod(np.cos(solution / sqrt))
        return part1 - 1.0 * part2 + 1.0


class HolderTable(ContinuousProblem):
    """Holder Table function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-10.0, -10.0], np.float)
        max_vals = np.array([10.0, 10.0], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = -19.2085
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        sum_sqrt_sq = np.sqrt(np.sum(solution * solution))
        part1 = np.exp(np.abs(1.0 - (sum_sqrt_sq / np.pi)))
        part2 = np.sin(solution[0]) * np.cos(solution[1])
        return -1.0 * np.abs(part2 * part1)


class Langermann(ContinuousProblem):
    """Langermann function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([0.0] * n_dim, np.float)
        max_vals = np.array([10.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        A = np.array([[3, 5],
                      [5, 2],
                      [2, 1],
                      [1, 4],
                      [7, 9]], np.float)
        c = np.array([1, 2, 5, 2, 3], np.float)
        part_sum = np.sum((solution - A) * (solution - A), axis=1)

        part1 = np.cos(np.pi * part_sum)
        part2 = np.exp((-1.0 / np.pi) * part_sum)
        return np.sum(c * part1 * part2)


class Levy(ContinuousProblem):
    """Levy function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-10] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        w = 1.0 + (solution - 1.0) / 4.0
        part_w = w[:-1]
        part1 = np.power(np.sin(np.pi * w[0]), 2)
        part2 = np.sum((part_w - 1) * (part_w - 1) *
                       (1 + 10 * np.power(np.sin(np.pi * part_w + 1), 2)))
        part3 = ((w[-1] - 1) * (w[-1] - 1) * (1 + np.power(np.sin(2 * np.pi *
                                                                  w[-1]), 2)))
        return part1 + part2 + part3


class Levy13(ContinuousProblem):
    """Levy function N.13."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-10.0] * n_dim, np.float)
        max_vals = np.array([10.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = np.power(np.sin(3 * np.pi * x1), 2)
        part2 = (x1 - 1) * (x1 - 1) * (1 + np.power(np.sin(3 * np.pi * x2), 2))
        part3 = (x2 - 1) * (x2 - 1) * (1 + np.power(np.sin(2 * np.pi * x2), 2))
        return part1 + part2 + part3


class Rastrigin(ContinuousProblem):
    """Rastrigin function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-5.12] * n_dim, np.float)
        max_vals = np.array([5.12] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        A = 10
        n = len(solution)
        part1 = A * np.cos(2 * np.pi * solution)
        part2 = solution * solution
        return A*n + np.sum(part2 - part1)


class Schaffer2(ContinuousProblem):
    """Schaffer function N.2."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-100.0] * n_dim, np.float)
        max_vals = np.array([100.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = np.power(np.sin((x1 * x1) - (x2 * x2)), 2)
        part2 = np.power(1.0 + 0.001 * ((x1 * x1) + (x2 * x2)), 2)
        return 0.5 + (part1 - 0.5) / part2


class Schaffer4(ContinuousProblem):
    """Schaffer function N.4."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-100.0] * n_dim, np.float)
        max_vals = np.array([100.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = np.cos(np.sin(np.abs((x1 * x1) - (x2 * x2))))
        part2 = np.power(1.0 + 0.001 * ((x1 * x1) + (x2 * x2)), 2)
        return 0.5 + (part1 - 0.5) / part2


class Schwefel(ContinuousProblem):
    """Schwefel function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-500] * n_dim, np.float)
        max_vals = np.array([500] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 20.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        A = 418.9829
        n = len(solution)
        sq_sol = np.sqrt(np.abs(solution))
        return A*n - 1.0 * np.sum(solution * np.sin(sq_sol))


class Shubert(ContinuousProblem):
    """Shubert function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-5.12] * n_dim, np.float)
        max_vals = np.array([5.12] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = -186.7309
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        A = np.array(range(1, 6), np.float)
        x1 = solution[0]
        x2 = solution[1]
        part1 = A + np.cos((A + 1.) * x1 + A)
        part2 = A + np.cos((A + 1.) * x2 + A)
        return np.sum(part1) * np.sum(part2)


# --------------------------------------------------------------------------- #
#                            Functions Bowl-Shaped                            #
# --------------------------------------------------------------------------- #


class Bohachevsky(ContinuousProblem):
    """Bohachevsky functions.

    Args:
        num_func (int): 1, 2 or 3. Define which Bohachevsky function is used.
            Default is 1.

    """
    def __init__(self, num_func=1):
        if num_func not in [1, 2, 3]:
            raise ValueError("The Bohachevsky can only be of "
                             "numbers 1, 2 or 3.")
        self.num_func = num_func
        n_dim = 2
        min_vals = np.array([-100] * n_dim, np.float)
        max_vals = np.array([100] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        if self.num_func == 1:
            return self._eval_func_1(solution)
        elif self.num_func == 2:
            return self._eval_func_2(solution)
        elif self.num_func == 3:
            return self._eval_func_3(solution)

    def _eval_func_1(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = (x1 * x1) + 2 * (x2 * x2)
        part2 = 0.3 * np.cos(3 * np.pi * x1)
        part3 = 0.4 * np.cos(4 * np.pi * x2)
        return part1 - part2 - part3 + 0.7

    def _eval_func_2(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = (x1 * x1) + 2 * (x2 * x2)
        part2 = 0.3 * np.cos(3 * np.pi * x1)
        part3 = np.cos(4 * np.pi * x2)
        return part1 - (part2 * part3) + 0.3

    def _eval_func_3(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = (x1 * x1) + 2 * (x2 * x2)
        part2 = 3 * np.pi * x1
        part3 = 4 * np.pi * x2
        return part1 - 0.3 * np.cos(part2 + part3) + 0.3


class Perm0(ContinuousProblem):
    """Perm 0,d,B function.

    Args:
        n_dim (int): Number of dimensions.
        beta (float): Argument of the function.

    """
    def __init__(self, n_dim, beta):
        self.beta = beta
        min_vals = np.array([-1 * n_dim] * n_dim, np.float)
        max_vals = np.array([n_dim] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, n_dim/10.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        j = np.array(range(1, n+1), np.float)
        s_mat = np.zeros((n, n), np.float)
        j_mat = np.zeros((n, n), np.float)
        for i in range(n):
            s_mat[i] += np.power(solution, i+1)
            j_mat[i] += 1 / np.power(j, i+1)
        part1 = np.sum(j + self.beta) * np.sum(s_mat - 1.0 * j_mat, axis=1)
        return np.sum(np.power(part1, 2))


class RotatedHyperEllipsoid(ContinuousProblem):
    """Rotated Hyper-Ellipsoid function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-65.536] * n_dim, np.float)
        max_vals = np.array([65.536] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        s_mat = np.zeros((n, n), np.float)
        solsq = solution * solution
        prod = solsq.copy()
        for i in range(n):
            l = np.array(prod[:i+1].copy())
            l.resize((n,))
            s_mat[i] += l
        return np.sum(s_mat)


class Sphere(ContinuousProblem):
    """Sphere function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-5.12] * n_dim, np.float)
        max_vals = np.array([5.12] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        return np.sum(solution * solution)


class SumDiffPower(ContinuousProblem):
    """Sum of Different Powers function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-1] * n_dim, np.float)
        max_vals = np.array([1] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.001, 0.1)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        powers = np.array(range(2, n+2), np.float)
        return np.sum(np.power(np.abs(solution), powers))


class SumSquare(ContinuousProblem):
    """Sum Squares function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-10] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        i = np.array(range(1, n+1), np.float)
        return np.sum(i * solution * solution)


class Trid(ContinuousProblem):
    """Trid function.

    Global minimum are knowm for dimensions 6 and 10.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        dimsq = n_dim * n_dim
        min_vals = np.array([dimsq] * n_dim, np.float)
        max_vals = np.array([dimsq] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, dimsq/10.)
        if n_dim == 6:
            known_min = -50.
        elif n_dim == 10:
            known_min = -200.
        else:
            known_min = None
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        part1 = np.sum(np.power(solution - 1, 2))
        part2 = np.sum(solution[1:] * solution[:-1])
        return part1 - part2


# --------------------------------------------------------------------------- #
#                            Functions Plate-Shaped                           #
# --------------------------------------------------------------------------- #


class Booth(ContinuousProblem):
    """Booth function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-10] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = np.power(x1 + 2 * x2 - 7.0, 2)
        part2 = np.power(2 * x1 + x2 - 5.0, 2)
        return part1 + part2


class Matyas(ContinuousProblem):
    """Matyas function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-10] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = 0.26 * (x1 * x1 + x2 * x2)
        part2 = 0.48 * x1 * x2
        return part1 - part2


class McCormick(ContinuousProblem):
    """McCormick function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-1.5, 3.0], np.float)
        max_vals = np.array([4.0, 4.0], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = -1.9133
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = np.sin(x1 + x2) + np.power(x1 - x2, 2)
        part2 = -1.0 * x1 + 2.5 * x2 + 1.0
        return part1 + part2


class PowerSum(ContinuousProblem):
    """Power Sum function."""
    def __init__(self):
        n_dim = 4
        min_vals = np.array([0] * n_dim, np.float)
        max_vals = np.array([n_dim] * n_dim, np.float)
        step = n_dim / 10.
        move_range = ContinuousLogMoveRange(0.01, step)
        known_min = None
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        b = np.array([8, 18, 44, 114], np.float)
        n = len(solution)
        s_mat = np.zeros((n, n), np.float)
        i = np.array(range(1, n+1), np.float)
        prod = np.power(solution, i)
        for i in range(n):
            l = np.array(prod[:i+1].copy())
            l.resize((n,))
            s_mat[i] += l
        return np.sum(np.power(np.sum(s_mat, axis=1) - b, 2))


class Zakharov(ContinuousProblem):
    """Zakharov function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-5] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        i = np.array(range(1, n+1), np.float)
        part1 = np.sum(np.power(solution, 2))
        part2 = np.power(np.sum(0.5 * i * solution), 2)
        part3 = np.power(np.sum(0.5 * i * solution), 4)
        return part1 + part2 + part3


# --------------------------------------------------------------------------- #
#                          Functions Valley-Shaped                            #
# --------------------------------------------------------------------------- #


class ThreeHumpCamel(ContinuousProblem):
    """Three-Hump Camel function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-5.0] * n_dim, np.float)
        max_vals = np.array([5.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = 2 * x1 * x1
        part2 = 1.05 * np.power(x1, 4)
        part3 = np.power(x1, 6) / 6.
        part4 = x1 * x2
        part5 = np.power(x2, 2)
        return part1 - part2 + part3 + part4 + part5


class SixHumpCamel(ContinuousProblem):
    """Six-Hump Camel function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-3.0, -2.0], np.float)
        max_vals = np.array([3.0, 2.0], np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = -1.0316
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = 4.0 - 2.1 * np.power(x1, 2) + np.power(x1, 4) / 3.0
        part2 = np.power(x2, 2)
        part3 = x1 * x2
        part4 = (-4.0 + 4.0 * np.power(x2, 2)) * np.power(x2, 2)
        return part1 * part2 + part3 + part4


class DixonPrice(ContinuousProblem):
    """Dixon-Price function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-10.0] * n_dim, np.float)
        max_vals = np.array([10.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        x1 = solution[0]
        s1 = solution[1:]
        s2 = solution[:-1]
        i = np.array(range(2, n+1), np.float)
        part1 = np.power(x1 - 1.0, 2)
        part2 = np.sum(i * np.power(2 * s1 * s1 - s2, 2))
        return part1 + part2


class Rosenbrock(ContinuousProblem):
    """Rosenbrock function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-5.0] * n_dim, np.float)
        max_vals = np.array([10.0] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        s1 = solution[1:]
        s2 = solution[:-1]
        part1 = s1 - (s2 * s2)
        part2 = s2 - 1.
        return np.sum((100 * part1 * part1) + (part2 * part2))


# --------------------------------------------------------------------------- #
#                       Functions with Steep Ridges/Drops                     #
# --------------------------------------------------------------------------- #


class DeJong5(ContinuousProblem):
    """De Jong function N.5."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-65.536] * n_dim, np.float)
        max_vals = np.array([65.536] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 5.)
        known_min = None
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        A = np.array([[-32, -16, 0, 16, 32] * 5,
                      [-32] * 5 + [-16] * 5 + [0] * 5 + [16] * 5 + [32] * 5],
                     np.float)
        x1 = solution[0]
        x2 = solution[1]
        i = np.array(range(1, 26), np.float)
        part1 = np.sum(np.power(i + np.power(x1 - A[0], 6) +
                                np.power(x2 - A[1], 6), -1))
        return np.power(0.002 + part1, -1)


class Easom(ContinuousProblem):
    """Easom function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-100] * n_dim, np.float)
        max_vals = np.array([100] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 10.)
        known_min = -1.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = -1 * np.power(x1 - np.pi, 2) - 1 * np.power(x2 - np.pi, 2)
        part2 = -1 * np.cos(x1) * np.cos(x2)
        return part2 * np.exp(part1)


class Michalewicz(ContinuousProblem):
    """Michalewicz function.

    Args:
        n_dim (int): Number of dimensions.

    """
    def __init__(self, n_dim):
        min_vals = np.array([0.0] * n_dim, np.float)
        max_vals = np.array([np.pi] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        if n_dim == 2:
            known_min = -1.8013
        elif n_dim == 5:
            known_min = -4.687658
        elif n_dim == 10:
            known_min = -9.66015
        else:
            known_min = None
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        m = 10
        i = np.array(range(1, n+1), np.float)
        part1 = np.sin(solution)
        part2 = np.power(np.sin(i * solution * solution * (1 / np.pi)), 2 * m)
        return -1.0 * np.sum(part1 * part2)


# --------------------------------------------------------------------------- #
#                                     Others                                  #
# --------------------------------------------------------------------------- #


class Beale(ContinuousProblem):
    """Beale function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-4.5] * n_dim, np.float)
        max_vals = np.array([4.5] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        part1 = np.power(1.5 - x1 + x1 * x2, 2)
        part2 = np.power(2.25 - x1 + x1 * x2 * x2, 2)
        part3 = np.power(2.625 - x1 + x1 * x2 * x2 * x2, 2)
        return part1 + part2 + part3


class Branin(ContinuousProblem):
    """Branin function."""
    def __init__(self):
        n_dim = 2
        min_vals = np.array([-4.5] * n_dim, np.float)
        max_vals = np.array([4.5] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        a = 1.0
        b = 5.1 / (4 * np.pi * np.pi)
        c = 5 / np.pi
        r = 6
        s = 10
        t = 1 / (8 * np.pi)
        x1 = solution[0]
        x2 = solution[1]
        part1 = x2 - b * x1 * x1 + c * x1 - r
        part2 = s * (1 - t) * np.cos(x1) + s
        return a * np.power(part1, 2) + part2


class Colville(ContinuousProblem):
    """Colville function."""
    def __init__(self):
        n_dim = 4
        min_vals = np.array([-10] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x1 = solution[0]
        x2 = solution[1]
        x3 = solution[2]
        x4 = solution[3]
        part1 = 100 * np.power(x1 * x1 - x2, 2)
        part2 = np.power(x1 - 1, 2)
        part3 = np.power(x3 - 1, 2)
        part4 = 90 * np.power(x3 * x3 - x4, 2)
        part5 = 10.1 * (np.power(x2 - 1, 2) + np.power(x4 - 1, 2))
        part6 = 19.8 * (x2 - 1) * (x4 - 1)
        return part1 + part2 + part3 + part4 + part5 + part6


class Forrester(ContinuousProblem):
    """Forrester et Al. function."""
    def __init__(self):
        n_dim = 1
        min_vals = np.array([0] * n_dim, np.float)
        max_vals = np.array([1] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        known_min = None
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        x = solution[0]
        part1 = np.power(6 * x - 2, 2)
        part2 = np.sin(12 * x - 4)
        return part1 * part2


class GoldsteinPrice(ContinuousProblem):
    """Goldstein-Price function.

    Args:
        rescaled_form (bool): True if the rescaled form of the Goldstein-Price
            function is to be used. Default is False.

    """
    def __init__(self, rescaled_form=False):
        self.rescaled_form = rescaled_form
        n_dim = 2
        min_vals = np.array([-2] * n_dim, np.float)
        max_vals = np.array([2] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        if self.rescaled_form:
            known_min = None
        else:
            known_min = 3.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        if self.rescaled_form:
            return self._eval_rescaled(solution)
        else:
            return self._eval_not_rescaled(solution)

    def _eval_rescaled(self, solution):
        n_sol = 4 * solution - 2
        part1 = self._eval_not_rescaled(n_sol)
        return (1/2.427) * (np.log(part1) - 8.693)

    def _eval_not_rescaled(self, solution):
        x1 = solution[0]
        x1_2 = x1 * x1
        x2 = solution[1]
        x2_2 = x2 * x2
        part1 = (1 + np.power(x1 + x2 + 1, 2) * (19 - 14 * x1 + 3 * x1_2 - 14 *
                                                 x2 + 6 * x1 * x2 + 3 * x2_2))
        part2 = (30 + np.power(2 * x1 - 3 * x2, 2) * (18 - 32 * x1 + 12 * x1_2
                                                      + 48 * x2 - 36 * x1 * x2
                                                      + 27 * x2_2))
        return part1 * part2


class Hartmann3D(ContinuousProblem):
    """Hartmann 3-Dimensional function."""
    def __init__(self):
        n_dim = 3
        min_vals = np.array([0] * n_dim, np.float)
        max_vals = np.array([1] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        known_min = -3.86278
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        alpha = np.array([1.0, 1.2, 3.0, 3.2], np.float)
        A = np.array([[3.0, 10, 30],
                      [0.1, 10, 35],
                      [3.0, 10, 30],
                      [0.1, 10, 35]], np.float)
        P = 0.0001 * np.array([[3689, 1170, 2673],
                               [4699, 4387, 7470],
                               [1091, 8732, 5547],
                               [381, 5743, 8828]], np.float)
        part1 = -1 * np.sum(A + np.power(solution - P, 2), axis=1)
        return (-1 * np.sum(alpha * np.exp(part1)))


class Hartmann6D(ContinuousProblem):
    """Hartmann 6-Dimensional function.

    Args:
        rescaled_form (bool): True if the rescaled form of the function is used
            False otherwise. Default is False.

    """
    def __init__(self, rescaled_form=False):
        self.rescaled_form = rescaled_form
        n_dim = 6
        min_vals = np.array([0] * n_dim, np.float)
        max_vals = np.array([1] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        if self.rescaled_form:
            known_min = None
        else:
            known_min = -3.32237
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        alpha = np.array([1.0, 1.2, 3.0, 3.2], np.float)
        A = np.array([[10, 3.0, 17, 3.5, 1.7, 8],
                      [0.05, 10, 17, 0.1, 8, 14],
                      [3, 3.5, 1.7, 10, 17, 8],
                      [17, 8, 0.05, 10, 0.1, 14]], np.float)
        P = 0.0001 * np.array([[1312, 1696, 5569,  124, 8283, 5886],
                               [2329, 4135, 8307, 3736, 1004, 9991],
                               [2348, 1451, 3522, 2883, 3047, 6650],
                               [4047, 8828, 8732, 5743, 1091,  381]], np.float)
        part1 = np.sum(A + np.power(solution - P, 2), axis=1)
        if self.rescaled_form:
            return ((-1 / 1.94) * (2.58 + part1))
        else:
            return -1 * np.sum(alpha * np.exp(part1))


class Perm(ContinuousProblem):
    """Perm d,B function.

    Args:
        n_dim (int): Number of dimensions.
        beta (float): Argument of the function.

    """
    def __init__(self, n_dim, beta):
        self.beta = beta
        min_vals = np.array([-1 * n_dim] * n_dim, np.float)
        max_vals = np.array([n_dim] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, n_dim/10.)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution)
        j = np.array(range(1, n+1), np.float)
        s_mat = np.zeros((n, n), np.float)
        j_mat = np.zeros((n, n), np.float)
        j_mat2 = np.zeros((n, n), np.float)
        for i in range(n):
            s_mat[i] += np.power(solution, i+1)
            j_mat[i] += 1 / np.power(j, i+1)
            j_mat2[i] += np.power(j, i+1)
        part1 = np.sum((j_mat2 + self.beta) * (s_mat - 1.0 * j_mat), axis=1)
        return np.sum(np.power(part1, 2))


class Powell(ContinuousProblem):
    """Powell function.

    Args:
        n_dim (int): Number of dimensions. Must be a multiple of 4.

    """
    def __init__(self, n_dim):
        if n_dim % 4 != 0:
            raise ValueError("The number of dimensions must be a "
                             "multiple of 4")
        min_vals = np.array([-4] * n_dim, np.float)
        max_vals = np.array([5] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 0.1)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        n = len(solution) // 4
        n_sol = solution.copy()
        n_sol.resize((n, 4))
        value = 0.0
        for i in range(n):
            x0 = n_sol[i][0]
            x1 = n_sol[i][1]
            x2 = n_sol[i][2]
            x3 = n_sol[i][3]
            value += np.power(x0 + 10 * x1, 2)
            value += 5 * np.power(x2 - x0, 2)
            value += np.power(x1 - 2 * x2, 4)
            value += 10 * np.power(x0 - x3, 4)
        return value


class Shekel(ContinuousProblem):
    """Shekel function."""
    def __init__(self):
        n_dim = 4
        min_vals = np.array([0] * n_dim, np.float)
        max_vals = np.array([10] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = -10.5364
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        m = 10
        beta = 1/10 * np.array([1, 2, 2, 4, 4, 6, 3, 7, 5, 5], np.float)
        C = np.array([[4, 1, 8, 6, 3, 2, 5, 8, 6, 7],
                      [4, 1, 8, 6, 7, 9, 3, 1, 2, 3],
                      [4, 1, 8, 6, 3, 2, 5, 8, 6, 7],
                      [4, 1, 8, 6, 7, 9, 3, 1, 2, 3]], np.float)
        outer = 0.0
        for i in range(m):
            inner = 0.0
            for j in range(4):
                inner += np.power(solution[j] - C[j][i], 2) + beta[i]
            inner = np.power(inner, -1)
            outer += inner
        return -1 * outer


class StyblinskiTang(ContinuousProblem):
    """Styblinski-Tang function.

    Args:
        n_dim (int): Number of dimensions. Must be a multiple of 4.

    """
    def __init__(self, n_dim):
        min_vals = np.array([-5] * n_dim, np.float)
        max_vals = np.array([5] * n_dim, np.float)
        move_range = ContinuousLogMoveRange(0.01, 1.0)
        known_min = 0.0
        super().__init__(n_dim, min_vals, max_vals, move_range, known_min)

    def _eval_func(self, solution):
        s_4 = np.power(solution, 4)
        s_2 = np.power(solution, 2)
        return (1/2) * np.sum(s_4 - 16 * s_2 + 5 * solution)
