"""
File: metaheuristic.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""


class Metaheuristic(object):

    """Docstring for Metaheuristic.

    Args:
        problem

    Attributes:
        problem

    """

    def __init__(self, problem, *args, **kwargs):
        self.problem = problem

    def run(self):
        """
        """
        raise NotImplementedError('Abstract Class')
