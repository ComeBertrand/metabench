import pytest

import metabench as mb
from metabench.algorithmic.problem.continuous import *


def _perform_continuous_problem_test(cp):
    # TODO: it would be nice if this function was testing something
    s = cp.generate_solution()
    cp.evaluate(s)
    for n, m in cp.get_neighbors(s, 0.5):
        cp.evaluate(n, m)


def test_ackleys():
    cp = Ackleys(10)
    _perform_continuous_problem_test(cp)


def test_bukin6():
    cp = Bukin6()
    _perform_continuous_problem_test(cp)


def test_crossintray():
    cp = CrossInTray()
    _perform_continuous_problem_test(cp)


def test_drop_wave():
    cp = DropWave()
    _perform_continuous_problem_test(cp)


def test_eggholder():
    cp = Eggholder()
    _perform_continuous_problem_test(cp)


def test_gramacy_lee():
    cp = GramacyLee()
    _perform_continuous_problem_test(cp)


def test_griewank():
    cp = Griewank(10)
    _perform_continuous_problem_test(cp)


def test_holder_table():
    cp = HolderTable()
    _perform_continuous_problem_test(cp)


def test_langermann():
    cp = Langermann()
    _perform_continuous_problem_test(cp)


def test_levy():
    cp = Levy(10)
    _perform_continuous_problem_test(cp)


def test_levy13():
    cp = Levy13()
    _perform_continuous_problem_test(cp)


def test_rastrigin():
    cp = Rastrigin(10)
    _perform_continuous_problem_test(cp)


def test_schaffer2():
    cp = Schaffer2()
    _perform_continuous_problem_test(cp)


def test_schaffer4():
    cp = Schaffer4()
    _perform_continuous_problem_test(cp)


def test_schwefel():
    cp = Schwefel(10)
    _perform_continuous_problem_test(cp)


def test_shubert():
    cp = Shubert()
    _perform_continuous_problem_test(cp)


def test_bohachevsky():
    cp = Bohachevsky(1)
    _perform_continuous_problem_test(cp)
    cp = Bohachevsky(2)
    _perform_continuous_problem_test(cp)
    cp = Bohachevsky(3)
    _perform_continuous_problem_test(cp)
    with pytest.raises(ValueError):
        Bohachevsky(4)


def test_perm0():
    cp = Perm0(10, 0.7)
    _perform_continuous_problem_test(cp)
    cp = Perm0(10, -23.)
    _perform_continuous_problem_test(cp)


def test_rotated_hyper_ellipsoid():
    cp = RotatedHyperEllipsoid(10)
    _perform_continuous_problem_test(cp)


def test_sphere():
    cp = Sphere(10)
    _perform_continuous_problem_test(cp)


def test_sum_diff_power():
    cp = SumDiffPower(10)
    _perform_continuous_problem_test(cp)


def test_sum_square():
    cp = SumSquare(10)
    _perform_continuous_problem_test(cp)


def test_trid():
    cp = Trid(10)
    _perform_continuous_problem_test(cp)


def test_booth():
    cp = Booth()
    _perform_continuous_problem_test(cp)


def test_matyas():
    cp = Matyas()
    _perform_continuous_problem_test(cp)


def test_mc_cormick():
    cp = McCormick()
    _perform_continuous_problem_test(cp)


def test_power_sum():
    cp = PowerSum()
    _perform_continuous_problem_test(cp)


def test_zahkarov():
    cp = Zakharov(10)
    _perform_continuous_problem_test(cp)


def test_three_hump_camel():
    cp = ThreeHumpCamel()
    _perform_continuous_problem_test(cp)


def test_six_hump_camel():
    cp = SixHumpCamel()
    _perform_continuous_problem_test(cp)


def test_dixon_price():
    cp = DixonPrice(10)
    _perform_continuous_problem_test(cp)


def test_rosenbrock():
    cp = Rosenbrock(10)
    _perform_continuous_problem_test(cp)


def test_dejong5():
    cp = DeJong5()
    _perform_continuous_problem_test(cp)


def test_easom():
    cp = Easom()
    _perform_continuous_problem_test(cp)


def test_michalewicz():
    cp = Michalewicz(10)
    _perform_continuous_problem_test(cp)


def test_beale():
    cp = Beale()
    _perform_continuous_problem_test(cp)


def test_branin():
    cp = Branin()
    _perform_continuous_problem_test(cp)


def test_colville():
    cp = Colville()
    _perform_continuous_problem_test(cp)


def test_forrester():
    cp = Forrester()
    _perform_continuous_problem_test(cp)


def test_goldstein_price():
    cp = GoldsteinPrice(False)
    _perform_continuous_problem_test(cp)
    cp = GoldsteinPrice(True)
    _perform_continuous_problem_test(cp)


def test_hartmann3d():
    cp = Hartmann3D()
    _perform_continuous_problem_test(cp)


def test_hartmann6d():
    cp = Hartmann6D(False)
    _perform_continuous_problem_test(cp)
    cp = Hartmann6D(True)
    _perform_continuous_problem_test(cp)


def test_perm():
    cp = Perm(10, 0.7)
    _perform_continuous_problem_test(cp)


def test_powell():
    cp = Powell(12)
    _perform_continuous_problem_test(cp)
    with pytest.raises(ValueError):
        Powell(10)


def test_shekel():
    cp = Shekel()
    _perform_continuous_problem_test(cp)


def test_styblinski_tang():
    cp = StyblinskiTang(10)
    _perform_continuous_problem_test(cp)
