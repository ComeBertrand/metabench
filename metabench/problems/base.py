class Problem(object):
    """ Abstract class for problems to be solved by metaheuristics.

    """

    def generate(self, **kwargs):
        """ Creation of possible solution within the search space.

        """
        raise NotImplementedError(
            "Generate function not implemented for this Problem.")

    def handle_constaint(self, solution, **kwargs):
        """ Check and manage the constraint on the search space.

        Args:
            solution : a candidate solution.

        Returns:
            solution or None

        """
        raise NotImplementedError(
            "Handle constraint function not implemented for this Problem.")

    def evaluate(self, solution, **kwargs):
        """ Evaluate the fitness of a candidate solution.

        Args:
            solution : a candidate solution.

        Returns:
            tuple : the fitness of the individual.

        """
        raise NotImplementedError(
            "Evaluate function not implemented for this Problem.")

    def neighbor_operator(self, solution):
        """
        """
        pass

    def distance(self, solution_a, solution_b):
        """
        """
        pass
