from time import clock
from random import random

import numpy as np
from deap import base, tools

from metabench.meta.base import Metaheuristic
from metabench.base.stat import IterStat


class BasicGeneticAlgorithm(Metaheuristic):
    def __init__(self, problem, pop_size=100, nbgen=100, cxpb=0.5,
                 cxindpb=0.5, mutpb=0.2, mutindpb=0.2):
        super().__init__(problem)
        self.pop_size = pop_size
        self.nbgen = nbgen
        self.cxpb = cxpb
        self.cxindpb = cxindpb
        self.mutpb = mutpb
        self.mutindpb = mutindpb

        self._toolbox = base.Toolbox()
        self._toolbox.register("individual", self.problem.generate)
        self._toolbox.register("population", tools.initRepeat,
                               list, self._toolbox.individual)

        self._toolbox.register("mate", self.problem.mate)
        self._toolbox.register("mutate", self.problem.mutate)
        self._toolbox.register("select", tools.selTournament, tournsize=3)
        self._toolbox.register("evaluate", self.problem.evaluate)

        self._stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        self._stats.register("avg", np.mean)
        self._stats.register("std", np.std)
        self._stats.register("min", np.min)
        self._stats.register("max", np.max)

    def __iter__(self):
        self._pop = self._toolbox.population(n=self.pop_size)
        fitnesses = map(self._toolbox.evaluate, self._pop)
        for ind, fit in zip(self._pop, fitnesses):
            ind.fitness.values = fit

        for g in range(self.nbgen):
            time_start = clock()

            offspring = self._toolbox.select(self._pop, len(self._pop))
            offspring = list(map(self._toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random() < self.cxpb:
                    self._toolbox.mate(child1, child2, cxindpb=self.cxindpb)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random() < self.mutpb:
                    self._toolbox.mutate(mutant, mutindpb=self.mutindpb)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(self._toolbox.evaluate, invalid_ind))
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            self._pop[:] = offspring

            time_iter = clock() - time_start

            record = self._stats.compile(self._pop)

            iter_stat = IterStat(g+1,
                                 best=record["max"],
                                 lowest=record["min"],
                                 avg=record["avg"],
                                 std=record["std"],
                                 time=time_iter)
            yield iter_stat
