"""
File: move_functions.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Move functions for space discovery.
"""

from itertools import combinations, product

import numpy as np

from metabench.algorithmic.utils import implemented_for
from metabench.common.fitness import Modifs


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
