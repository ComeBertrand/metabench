from metabench.benchmark import Benchmark
from metabench.meta.sbase.hill_climbing import HillClimbing
from metabench.prob.base.continuous import Sphere


def main():
    b = Benchmark()
    b.add_meta(HillClimbing)
    b.add_problem(Sphere, 10, -100, 100)
    b.run()
    for meta in b.results:
        print("Result for Meta : {} on {}".format(meta.__class__.__name__,
                                                  meta.problem.__class__.__name__))
        print(" --------------------------------------------")
        for stat in b.results[meta]:
            print(stat.best)
        print(" --------------------------------------------")
        print(meta.solution)
        print("")


if __name__ == "__main__":
    main()
