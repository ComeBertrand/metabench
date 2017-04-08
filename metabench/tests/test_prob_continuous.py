import pytest

import metabench as mb


def _perform_continuous_problem_test(cp):
    s = cp.generate_solution()
    cp.evaluate(s)
    for n, m in cp.get_neighbors(s, 0.5):
        cp.evaluate(n, m)


def test_ackleys():
    cp = mb.prob.Ackleys(10)
    _perform_continuous_problem_test(cp)


def test_bukin6():
    cp = mb.prob.Bukin6()
    _perform_continuous_problem_test(cp)


def test_crossintray():
    cp = mb.prob.CrossInTray()
    _perform_continuous_problem_test(cp)


def test_drop_wave():
    cp = mb.prob.DropWave()
    _perform_continuous_problem_test(cp)


def test_eggholder():
    cp = mb.prob.Eggholder()
    _perform_continuous_problem_test(cp)


def test_gramacy_lee():
    cp = mb.prob.GramacyLee()
    _perform_continuous_problem_test(cp)


def test_griewank():
    cp = mb.prob.Griewank(10)
    _perform_continuous_problem_test(cp)


def test_holder_table():
    cp = mb.prob.HolderTable()
    _perform_continuous_problem_test(cp)


def test_langermann():
    cp = mb.prob.Langermann()
    _perform_continuous_problem_test(cp)


def test_levy():
    cp = mb.prob.Levy(10)
    _perform_continuous_problem_test(cp)


def test_levy13():
    cp = mb.prob.Levy13()
    _perform_continuous_problem_test(cp)


def test_rastrigin():
    cp = mb.prob.Rastrigin(10)
    _perform_continuous_problem_test(cp)


def test_schaffer2():
    cp = mb.prob.Schaffer2()
    _perform_continuous_problem_test(cp)


def test_schaffer4():
    cp = mb.prob.Schaffer4()
    _perform_continuous_problem_test(cp)


def test_schwefel():
    cp = mb.prob.Schwefel(10)
    _perform_continuous_problem_test(cp)


def test_shubert():
    cp = mb.prob.Shubert()
    _perform_continuous_problem_test(cp)


def test_bohachevsky():
    cp = mb.prob.Bohachevsky(1)
    _perform_continuous_problem_test(cp)
    cp = mb.prob.Bohachevsky(2)
    _perform_continuous_problem_test(cp)
    cp = mb.prob.Bohachevsky(3)
    _perform_continuous_problem_test(cp)
    with pytest.raises(ValueError):
        mb.prob.Bohachevsky(4)


def test_perm0():
    cp = mb.prob.Perm0(10, 0.7)
    _perform_continuous_problem_test(cp)
    cp = mb.prob.Perm0(10, -23.)
    _perform_continuous_problem_test(cp)


def test_rotated_hyper_ellipsoid():
    cp = mb.prob.RotatedHyperEllipsoid(10)
    _perform_continuous_problem_test(cp)


def test_sphere():
    cp = mb.prob.Sphere(10)
    _perform_continuous_problem_test(cp)


def test_sum_diff_power():
    cp = mb.prob.SumDiffPower(10)
    _perform_continuous_problem_test(cp)


def test_sum_square():
    cp = mb.prob.SumSquare(10)
    _perform_continuous_problem_test(cp)


def test_trid():
    cp = mb.prob.Trid(10)
    _perform_continuous_problem_test(cp)


def test_booth():
    cp = mb.prob.Booth()
    _perform_continuous_problem_test(cp)


def test_matyas():
    cp = mb.prob.Matyas()
    _perform_continuous_problem_test(cp)


def test_mc_cormick():
    cp = mb.prob.McCormick()
    _perform_continuous_problem_test(cp)


def test_power_sum():
    cp = mb.prob.PowerSum()
    _perform_continuous_problem_test(cp)


def test_zahkarov():
    cp = mb.prob.Zakharov(10)
    _perform_continuous_problem_test(cp)


def test_three_hump_camel():
    cp = mb.prob.ThreeHumpCamel()
    _perform_continuous_problem_test(cp)


def test_six_hump_camel():
    cp = mb.prob.SixHumpCamel()
    _perform_continuous_problem_test(cp)


def test_dixon_price():
    cp = mb.prob.DixonPrice(10)
    _perform_continuous_problem_test(cp)


def test_rosenbrock():
    cp = mb.prob.Rosenbrock(10)
    _perform_continuous_problem_test(cp)


def test_dejong5():
    cp = mb.prob.DeJong5()
    _perform_continuous_problem_test(cp)


def test_easom():
    cp = mb.prob.Easom()
    _perform_continuous_problem_test(cp)


def test_michalewicz():
    cp = mb.prob.Michalewicz(10)
    _perform_continuous_problem_test(cp)


def test_beale():
    cp = mb.prob.Beale()
    _perform_continuous_problem_test(cp)


def test_branin():
    cp = mb.prob.Branin()
    _perform_continuous_problem_test(cp)


def test_colville():
    cp = mb.prob.Colville()
    _perform_continuous_problem_test(cp)


def test_forrester():
    cp = mb.prob.Forrester()
    _perform_continuous_problem_test(cp)


def test_goldstein_price():
    cp = mb.prob.GoldsteinPrice(False)
    _perform_continuous_problem_test(cp)
    cp = mb.prob.GoldsteinPrice(True)
    _perform_continuous_problem_test(cp)


def test_hartmann3d():
    cp = mb.prob.Hartmann3D()
    _perform_continuous_problem_test(cp)


def test_hartmann6d():
    cp = mb.prob.Hartmann6D(False)
    _perform_continuous_problem_test(cp)
    cp = mb.prob.Hartmann6D(True)
    _perform_continuous_problem_test(cp)


def test_perm():
    cp = mb.prob.Perm(10, 0.7)
    _perform_continuous_problem_test(cp)


def test_powell():
    cp = mb.prob.Powell(12)
    _perform_continuous_problem_test(cp)
    with pytest.raises(ValueError):
        mb.prob.Powell(10)


def test_shekel():
    cp = mb.prob.Shekel()
    _perform_continuous_problem_test(cp)


def test_styblinski_tang():
    cp = mb.prob.StyblinskiTang(10)
    _perform_continuous_problem_test(cp)
