"""
File: move_range.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Normalizer for range of move in the solution space.
"""

import numpy as np


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
