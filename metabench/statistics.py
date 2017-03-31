"""
File: statistics.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Statistics computation tools that will be the result of the
benchmark computation.
"""

import numpy as np


class Statistics(object):
    """Compilation of statistics on a benchmark of a metaheuristic run.

    Args:
        nb_run (int): Number of runs that will be made of a metaheuristic on
            the same problem. Strictly positive.
        base_size (int): Base size for the arrays that will hold the data from
            the iterations of the metaheuristic. Default is 256. Strictly
            positive.

    Attributes:
        nb_run (int): number of runs on which statistics are compiled.
        nb_iter_per_run (np.array): Array of size 'nb_run' that holds the
            number of iteration made by the metaheuristic for each run.
        nb_iter_total (int): Total number of iterations made in all the runs.

        best_values (nb.array): Array of size 'nb_run' that hold the best
            fitness of each run.
        best_value (float): Best fitness in all the runs.
        worst_value (float): Worst fitness of the best fitnesses computed
            at each run.
        mean_value (float): Mean best fitness recorded for each run.
        std_value (float): Standard deviation on the best fitness of each
            run.

        best_time_iter (float): Best time (lower is better) of iteration
            computation in all the runs. (in s).
        worst_time_iter (float): Worst time (lower is better) of iteration
            computation in all the runs. (in s).
        mean_time_iter (float): Mean time taken by the iteration computation.
            (in s.)
        std_time_iter (float): Standard deviation of the time taken by the
            iterations computation.

        best_time_tot (float): Best time (lower is better) of computation of
            a full run. (in s).
        worst_time_tot (float): Worst time (lower is better) of computation of
            a full run. (in s).
        mean_time_tot (float): Mean time taken by the full run computation.
            (in s).
        std_time_tot (float): Standard deviation of the time taken by the
            full run computation.

    """
    def __init__(self, nb_run, base_size=256):
        if nb_run <= 0:
            raise ValueError("The number of runs must be strictly positive")
        if base_size <= 0:
            raise ValueError("The base size must be strictly positive")

        self._nb_iter = np.zeros(nb_run, np.int)
        self._nb_iter_tot = 0
        self._nb_run = nb_run

        self._current_size_value = base_size
        self._current_size_time = base_size

        # Values records are indexed by runs.
        self._values = np.zeros((nb_run, base_size), np.float)
        # Iter time records are all in the same array.
        self._time = np.zeros(base_size, np.float)
        self._time_tot = np.zeros(nb_run, np.float)

    def record_iter_stat(self, num_run, best_solution, time_iteration):
        """Record a statistic concerning an iteration.

        Args:
            num_run (int): Index of the run in which the iteration took place.
            best_solution (Solution): Best solution computed at the end of the
                iteration. It has to be evaluated.
            time_iteration (float): Time in second taken to compute the
                iteration.

        """
        if best_solution.fitness is None:
            raise ValueError("Statistics cannot be recorded on solutions that "
                             "have not been evaluated.")
        if self._nb_iter[num_run] >= self._current_size_value:
            self._current_size_value *= 2
            self._values.resize((self._nb_run, self._current_size_value))

        if self._nb_iter_tot >= self._current_size_time:
            self._current_size_time *= 2
            self._time.resize((self._current_size_time,))

        self._values[num_run][self._nb_iter[num_run]] = best_solution.fitness
        self._time[self._nb_iter_tot] = time_iteration

        self._nb_iter[num_run] += 1
        self._nb_iter_tot += 1

    def record_time_computation(self, num_run, time_computation):
        """Record the time taken by a full metaheuristic run.

        Args:
            num_run (int): Index of the run in which the iteration took place.
            time_computation (float): Time in second taken to compute the
                full run.

        """
        self._time_tot[num_run] = time_computation

    @property
    def nb_run(self):
        return self._nb_run

    @property
    def nb_iter_per_run(self):
        return self._nb_iter

    @property
    def nb_iter_total(self):
        return self._nb_iter_tot

    @property
    def best_values(self):
        return np.array([self._values[i][max_iter - 1] for i, max_iter
                         in enumerate(self._nb_iter) if max_iter > 0],
                        np.float)

    @property
    def best_value(self):
        if len(self.best_values):
            return np.amin(self.best_values)
        return None

    @property
    def worst_value(self):
        if len(self.best_values):
            return np.amax(self.best_values)
        return None

    @property
    def mean_value(self):
        if len(self.best_values):
            return np.mean(self.best_values)
        return None

    @property
    def std_value(self):
        if len(self.best_values):
            return np.std(self.best_values)
        return None

    @property
    def best_time_iter(self):
        if self._nb_iter_tot:
            return np.amin(self._time[:self._nb_iter_tot])
        return None

    @property
    def worst_time_iter(self):
        if self._nb_iter_tot:
            return np.amax(self._time[:self._nb_iter_tot])
        return None

    @property
    def mean_time_iter(self):
        if self._nb_iter_tot:
            return np.mean(self._time[:self._nb_iter_tot])
        return None

    @property
    def std_time_iter(self):
        if self._nb_iter_tot:
            return np.std(self._time[:self._nb_iter_tot])
        return None

    @property
    def best_time_tot(self):
        if np.any(self._time_tot):
            return np.amin(self._time_tot)
        return None

    @property
    def worst_time_tot(self):
        if np.any(self._time_tot):
            return np.amax(self._time_tot)
        return None

    @property
    def mean_time_tot(self):
        if np.any(self._time_tot):
            return np.mean(self._time_tot)
        return None

    @property
    def std_time_tot(self):
        if np.any(self._time_tot):
            return np.std(self._time_tot)
        return None

    def __str__(self):
        st_c = "|{0}|{1}|{2}|{3}|\n"
        line = "".join(["-"]*62) + "\n"
        stat_str = ""
        stat_str += line
        stat_str += ("|{}|\n".format("fitness".center(60)))
        stat_str += line
        stat_str += ("|{}|{}|{}|{}|\n".format("worst".center(14),
                                              "mean".center(14),
                                              "best".center(14),
                                              "std".center(15)))
        stat_str += line
        stat_str += (st_c.format(str(self.worst_value).center(14),
                                 str(self.mean_value).center(14),
                                 str(self.best_value).center(14),
                                 str(self.std_value).center(15)))
        stat_str += line
        stat_str += ("|{}|\n".format("nb_iterations".center(60)))
        stat_str += line
        stat_str += ("|{}|{}|{}|{}|\n".format("worst".center(14),
                                              "mean".center(14),
                                              "best".center(14),
                                              "std".center(15)))
        stat_str += line
        stat_str += (st_c.format(str(np.amax(self.nb_iter_per_run)).center(14),
                                 str(np.mean(self.nb_iter_per_run)).center(14),
                                 str(np.amin(self.nb_iter_per_run)).center(14),
                                 str(np.std(self.nb_iter_per_run)).center(15)))
        stat_str += line
        stat_str += ("|{}|\n".format("time_per_iteration".center(60)))
        stat_str += line
        stat_str += ("|{}|{}|{}|{}|\n".format("worst".center(14),
                                              "mean".center(14),
                                              "best".center(14),
                                              "std".center(15)))
        stat_str += line
        stat_str += (st_c.format(str(self.worst_time_iter).center(14),
                                 str(self.mean_time_iter).center(14),
                                 str(self.best_time_iter).center(14),
                                 str(self.std_time_iter).center(15)))
        stat_str += line
        stat_str += ("|{}|\n".format("time_per_run".center(60)))
        stat_str += line
        stat_str += ("|{}|{}|{}|{}|\n".format("worst".center(14),
                                              "mean".center(14),
                                              "best".center(14),
                                              "std".center(15)))
        stat_str += line
        stat_str += (st_c.format(str(self.worst_time_tot).center(14),
                                 str(self.mean_time_tot).center(14),
                                 str(self.best_time_tot).center(14),
                                 str(self.std_time_tot).center(15)))
        stat_str += line
        return stat_str
