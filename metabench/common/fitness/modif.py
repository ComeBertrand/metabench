"""
File: modif.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Recorder of modifications made on a solution.
"""

from collections import OrderedDict


class Modifs(OrderedDict):
    """Keep track of the modifications made on a solution.

    The Modifs will be used to compute the fitness of a modified solution
    in a partial manner.

    Each key of a Modifs is the index of where the change was made, each
    value is a tuple of (value_before, value_after).

    """
    def __init__(self):
        super().__init__()

    def add_modif(self, index, val_before, val_after):
        """Add a modification to the list of moves.

        A new modif on an existing indexed move will see its new val_before
        dropped and its former val_after replaced. This insure that the modifs
        will always keep the first and last value of an attribute.

        Args:
            index (int): Index where the change was made in the solution.
            val_before (any): Previous value at the index.
            val_after (any): New value at the index.

        """
        cur_val = self.get(index, None)
        if cur_val is not None:
            super().__setitem__(index, (cur_val[0], val_after))
        else:
            super().__setitem__(index, (val_before, val_after))

    def __setitem__(self, key, value):
        """Only allow the setting of values through the add_modif method."""
        raise NotImplementedError("Use the add_modif method instead")
