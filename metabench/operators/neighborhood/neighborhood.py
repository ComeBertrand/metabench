"""
File: neighborhood.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Operators that create neighbors for a solution.
"""

from itertools import combinations, product

import numpy as np

from metabench.operators.utils.decorators import implemented_for
from metabench.common.objective.objective import Modifs


class MoveRange(object):
    """Defines the range of the steps that can be taken to explore the space.

    The role of the MoveRange class is to abstract the size of the step for the
    metaheuristics that will use steps to compute a neighborhood.

    This way, metaheuristics may vary the step between 0.0 and 1.0, and the
    MoveRange will convert the value into the proper one to use for the moves
    operators.

    MoveRange is an abstract class that has two main sub-classes:
    ContinuousMoveRange and DiscreteMoveRange.

    """
    def __init__(self):
        raise NotImplementedError("Abstract class")

    def convert(self, step):
        """Convert the normalized step of a metaheuristic to the real step.

        Shall be implemented in sub-classes.

        Args:
            step (float): The normalized step value provided by the
                metaheuristics. Stricly between 0.0 and 1.0.

        Returns:
            any: the step value to be used for the move operator.

        """
        raise NotImplementedError("Abstract class")

    def _check_step(self, step):
        """Check that the step value given is actually a normalized step value.

        Args:
            step (float): The normalized step value provided by the
                metaheuristics. Stricly between 0.0 and 1.0.

        Raises:
            TypeError: If the given step is not a float.
            ValueError: If the given step is not in the range [0.0, 1.0].

        """
        if not isinstance(step, float):
            raise TypeError("A MoveRange can only convert a normalized step "
                            "of type float")
        if step > 1. or step < 0.:
            raise ValueError("A MoveRange can only convert a normalized step "
                             "that range in [0.0, 1.0]")


class ContinuousMoveRange(MoveRange):
    """MoveRange for continuous step values.

    A ContinuousMoveRange will convert a normalized step value in a value
    ranging from a lower bound to a higher bound.

    The conversion will be linear.

    Args:
        low (float): The lower bound of the move range.
        high (float): The higher bound of the move range.

    Attributes:
        low (float): The lower bound of the move range.
        high (float): The higher bound of the move range.

    Raises:
        ValueError: If the higher bound is strictly inferior to the lower
            bound.
        TypeError: If low or high are not float values.

    Example:
        >>> range_c = ContinuousMoveRange(1.0, 10.0)
        >>> range_c.convert(0.0)
        1.0
        >>> range_c.convert(0.5)
        5.5
        >>> range_c.convert(1.0)
        10.0

    """
    def __init__(self, low, high):
        if high < low:
            raise ValueError("High value for move range must be superior or "
                             "equal to the low value")
        if not isinstance(low, float):
            raise TypeError("Low bound of ContinuousMoveRange must be a float")
        if not isinstance(high, float):
            raise TypeError("High bound of ContinuousMoveRange must be a "
                            "float")

        self.low = low
        self.high = high

    def convert(self, step):
        """Linearily convert a normalized step to its continuous value."""
        self._check_step(step)
        return self.low + (self.high - self.low) * step


class ContinuousLogMoveRange(ContinuousMoveRange):
    """ContinuousMoveRange with logarithmic conversion of normalized step.

    Example:
        >>> range_c_log = ContinuousLogMoveRange(0.001, 10.0)
        >>> range_c_log.convert(0.0)
        0.001
        >>> range_c_log.convert(0.3)
        0.015848931924611134
        >>> range_c_log.convert(0.6)
        0.25118864315095796
        >>> range_c_log.convert(0.9)
        3.9810717055348731
        >>> range_c_log.convert(1.0)
        10.0

    """
    def convert(self, step):
        """Logarithmic convert a normalized step to its continuous value."""
        self._check_step(step)
        log_low = np.log10(self.low)
        log_high = np.log10(self.high)
        power_value = log_low + (log_high - log_low) * step
        return 10 ** power_value


class DiscreteMoveRange(MoveRange):
    """MoveRange for discrete step values.

    A DiscreteMoveRange will convert a normalized step value in a value
    ranging from a lower bound to a higher bound.

    The conversion will be linear.

    Args:
        low (int): The lower bound of the move range (included in possible
            values).
        high (int): The higher bound of the move range (included in possible
            values).

    Attributes:
        values (list): of int, the possible step values.
        nb_values (int): number of values that can be taken.

    Raises:
        ValueError: If the higher bound is strictly inferior to the lower
            bound.
        TypeError: If low or high are not int values.

    Example:
        >>> range_d = DiscreteMoveRange(1, 3)
        >>> range_d.convert(0.0)
        1
        >>> range_d.convert(0.5)
        2
        >>> range_d.convert(1.0)
        3

    """
    def __init__(self, low, high):
        if high < low:
            raise ValueError("High value for move range must be superior or "
                             "equal to the low value")
        if not isinstance(low, int):
            raise TypeError("Low bound of DiscreteMoveRange must be an int")
        if not isinstance(high, int):
            raise TypeError("High bound of DiscreteMoveRange must be an int")
        self.values = [x for x in range(low, high + 1)]
        self.nb_values = high - low + 1

    def convert(self, step):
        """Linearily convert a normalized step to its discrete value."""
        self._check_step(step)
        float_value = self.nb_values * step
        # TODO: using floor might be a bad idea. In the case the range min and
        # max values are next to each other, it will only take the second value
        # if the step is 1.0 (while it should probably take it once you are
        # above 0.5).
        index = min(int(np.floor(float_value)), self.nb_values - 1)
        return self.values[index]


class DiscreteLogMoveRange(DiscreteMoveRange):
    """DiscreteMoveRange with logarithmic conversion of normalized step.

    Example:
        >>> range_d_log = DiscreteLogMoveRange(0, 10)
        >>> range_d_log.convert(0.0)
        0
        >>> range_d_log.convert(0.3)
        1
        >>> range_d_log.convert(0.6)
        3
        >>> range_d_log.convert(0.9)
        8
        >>> range_d_log.convert(1.0)
        10

    """
    def convert(self, step):
        """Logarithmic convert a normalized step to its discrete value."""
        self._check_step(step)
        float_value = np.log10(self.nb_values) * step
        index = int(np.round(10**float_value)) - 1
        return self.values[index]


class Neighborhood(object):
    """Compute the neighborhood for the solutions.

    Args:
        move (func): Move function that has to take a solution as its first
            argument, and return a Solution and a Modifs.
        move_range (MoveRange): Define the step range for the move function.
        max_nb_neighbors (int): Maximum number of neighbors that will be
            computed by a call to the neighborhood.

    Attributes:
        move (func): Move function that has to take a solution as its first
            argument, and return a Solution and a Modifs.
        move_range (MoveRange): Define the step range for the move function.
        max_nb_neighbors (int): Maximum number of neighbors that will be
            computed by a call to the neighborhood.

    Example:
        >>> encoding = BinaryEncoding(10)
        >>> solution = encoding.generate_random_solution()
        >>> solution
        Solution([0, 0, 0, 0, 1, 0, 0, 0, 1, 0])
        >>> neighborhood = Neighborhood(move_binary_flip,
        ... DiscreteMoveRange(1, 2), 5)
        >>> for neighbor, modifs in neighborhood(solution, 0.0):
        ...     print(neighbor)
        ...
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
        [0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        [0, 0, 0, 1, 1, 0, 0, 0, 1, 0]

    """
    def __init__(self, move, move_range, max_nb_neighbors):
        self.move = move
        self.move_range = move_range
        self.max_nb_neighbors = max_nb_neighbors

    def __call__(self, solution, step):
        """Compute the neighbors of a solution.

        Args:
            solution (Solution): Solution for which the neighbors must be
                computed.
            step (float): Normalized step given by the metaheuristic. Strictly
                between 0.0 and 1.0.

        Yield:
            Solution: neighbors to the given solution.
            Modifs: the modifications made on the solution to create the
                neighbor.

        """
        converted_step = self.move_range.convert(step)
        # TODO: remove the nb_neighbors from the move functions. Moves shall
        # be atomic and just make a modification on a solution and return a
        # neighbor and a modification. They shall probably have a state that
        # prevent them from returning twice the same solution, but that's all.
        for neighbor, modifs in self.move(solution,
                                          converted_step,
                                          self.max_nb_neighbors):
            yield neighbor, modifs


@implemented_for('BinaryEncoding')
def move_binary_flip(solution, step, nb_neighbors):
    """Compute the neighbors of binary encoded solution by flipping bits.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (int): Number of bits to be flipped to create the neighbors.
            Strictly positive.
        nb_neighbors (int): Number of neighbors to be generated. Stricly
            positive. If None, all the neighbors will be returned.

    Yield:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    # TODO: This is crazy to do this. Find a way to randomly iterate over the
    # combinations possibles
    all_flips = [x for x in combinations(range(len(solution)), r=step)]
    np.random.shuffle(all_flips)

    if nb_neighbors is None:
        nb_neighbors = len(all_flips)

    for list_flips in all_flips[:nb_neighbors]:
        neighbor = solution.copy(True)
        modifs = Modifs()
        for index_flip in list_flips:
            if neighbor[index_flip]:
                neighbor[index_flip] = 0
                modifs.add_modif(index_flip, 1, 0)
            else:
                neighbor[index_flip] = 1
                modifs.add_modif(index_flip, 0, 1)
        yield neighbor, modifs


@implemented_for('RealEncoding')
def move_distance_continuous(solution, step, nb_neighbors):
    """Compute the neighbors of real-encoded solution.

    Neighbors will be randomly taken on the hypersphere of center 'solution'
    and radius 'step'.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (float): Radius of the hypersphere.
        nb_neighbors (int): Number of neighbors to be generated. Strictly
            positive. Should not be None.

    Yield:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    for _ in range(nb_neighbors):
        vector = np.random.normal(0, 1, len(solution))
        vector /= np.linalg.norm(vector)
        # TODO: look at this and at the MoveRange (that do not start at 0),
        # this is very strange (and probably mathematically false).
        vector *= step
        neighbor = solution.copy(True)
        neighbor += vector
        neighbor.to_bounds()

        # Modifs is empty, since all attributes of the neighbor might be
        # modified. (Empty modifs means full fitness must be re-computed).
        modifs = Modifs()
        yield neighbor, modifs


@implemented_for('DiscreteEncoding')
def move_substitution(solution, step, nb_neighbors):
    """Create neighbors for solutions with a discrete encoding.

    Neighbors are created by substituting the value of one of the attribute by
    another allowed value. A neighbor will be created for each attribute and
    new possible value.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (int): Number of substitution to make. Strictly positive.
        nb_neighbors (int): Number of neighbors to be generated. Strictly
            positive. If None, all the substitutions possibles will be made.

    Yield:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    # TODO: very naive and inneficient method. Find a better way.
    all_possibilities = []
    for i, _ in enumerate(solution):
        allowed_values = set(range(solution.min_val(i),
                                   solution.max_val(i) + 1))
        allowed_values.remove(solution[i])
        allowed_values = list(allowed_values)
        np.random.shuffle(allowed_values)
        all_possibilities.append([(i, x) for x in allowed_values])

    # TODO: this will probably crash the memory with number a bit big.
    all_comb = [x for x in combinations(all_possibilities, r=step)]
    all_subst = []
    for comb in all_comb:
        all_subst += product(*comb)
    np.random.shuffle(all_subst)

    if nb_neighbors is None:
        nb_neighbors = len(all_subst)

    for list_subst in all_subst[:nb_neighbors]:
        neighbor = solution.copy(True)
        modifs = Modifs()
        for index, value in list_subst:
            neighbor[index] = value
            modifs.add_modif(index, solution[index], value)
        yield neighbor, modifs


@implemented_for('PermutationEncoding')
def move_swap(solution, step, nb_neighbors):
    """Create neighbors for solutions with a permutation encoding.

    The swap move consists in exchanging the value of two index. All the swaps
    possible will create the neighborhood for a solution.

    Args:
        solution (Solution): The solution for which neighbors are generated.
        step (int): Number of swaps to make. Strictly positive.
        nb_neighbors (int): Number of neighbors to be generated. Strictly
            positive. If None, all the swaps possibles will be made.

    Yield:
        Solution: neighbor.
        Modifs: The modifications from given solution to neighbor.

    """
    # TODO: again, naive and way too costly for the memory.
    all_swaps = []
    for i in range(len(solution)-1):
        all_possibilities = []
        for j in range(i+1, len(solution)):
            all_possibilities.append((i, j))
        all_swaps.append(all_possibilities)

    list_comb = [x for x in combinations(all_swaps, r=step)]

    def _test_swap_unicity(val):
        for x1, x2 in combinations(val, r=2):
            if set(x1) & set(x2):
                return False
        return True

    list_swaps = []
    for comb in list_comb:
        product_result = filter(_test_swap_unicity, [x for x in
                                                     product(*comb)])
        list_swaps += product_result
    np.random.shuffle(list_swaps)

    if nb_neighbors is None:
        nb_neighbors = len(list_swaps)

    for swaps in list_swaps[:nb_neighbors]:
        neighbor = solution.copy(True)
        modifs = Modifs()
        for index_1, index_2 in swaps:
            neighbor[index_1] = solution[index_2]
            neighbor[index_2] = solution[index_1]
            modifs.add_modif(index_1, solution[index_1], neighbor[index_1])
            modifs.add_modif(index_2, solution[index_2], neighbor[index_2])
        yield neighbor, modifs


@implemented_for('PermutationEncoding')
def move_opt(solution):
    raise NotImplementedError("TODO")


@implemented_for('PermutationEncoding')
def move_insertion(solution):
    raise NotImplementedError("TODO")


@implemented_for('PermutationEncoding')
def move_inversion(solution):
    raise NotImplementedError("TODO")
