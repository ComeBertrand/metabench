"""
File: parameters.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Describe and hold the parameters for the metaheuristics and the
problems.
"""


class Parameter(object):
    """Description of a parameter.

    Args:
        name (str): Name of the parameter.
        description (str): Description of the parameter.
        default (any): Default value of the parameter.

    Attributes:
        name (str): Name of the parameter.
        description (str): Description of the parameter.
        default (any): Default value of the parameter.

    """
    def __init__(self, name, description, default):
        self.name = name
        self.description = description
        self.default = default

    def check_value(self, value):
        raise NotImplementedError("Abstract Class")


class ParameterInt(Parameter):
    """Description of an integer parameter.

    Args:
        min_val (int): Minimum value that can be taken by the parameter. If
            None, there is no minimum value.
        max_val (int): Maximum value that can be taken by the parameter. If
            None, there is no maximum value.

    Attributes:
        min_val (int): Minimum value that can be taken by the parameter. If
            None, there is no minimum value.
        max_val (int): Maximum value that can be taken by the parameter. If
            None, there is no maximum value.

    """
    def __init__(self, name, description, min_val, max_val, default):
        super().__init__(name, description, default)
        self.min_val = min_val
        self.max_val = max_val

    def check_value(self, value):
        if not isinstance(value, int):
            raise TypeError("The value for the parameter {} should be an "
                            "integer ({} instead)".format(self.name,
                                                          value.__class__))

        if self.min_val is not None and value < self.min_val:
            raise ValueError("The minimum value that can be given to the "
                             "parameter {} is {:d}. ({:d} "
                             "instead)".format(self.name,
                                               self.min_val,
                                               value))

        if self.max_val is not None and value > self.max_val:
            raise ValueError("The maximum value that can be given to the "
                             "parameter {} is {:d}. ({:d} "
                             "instead)".format(self.name,
                                               self.max_val,
                                               value))


class ParameterFloat(Parameter):
    def __init__(self, name, description, min_val, max_val, default):
        super().__init__(name, description, default)
        self.min_val = min_val
        self.max_val = max_val

    def check_value(self, value):
        if not isinstance(value, float):
            raise TypeError("The value for the parameter {} should be an "
                            "float ({} instead)".format(self.name,
                                                        value.__class__))

        if self.min_val is not None and value < self.min_val:
            raise ValueError("The minimum value that can be given to the "
                             "parameter {} is {:.2f}. ({:.2f} "
                             "instead)".format(self.name,
                                               self.min_val,
                                               value))

        if self.max_val is not None and value > self.max_val:
            raise ValueError("The maximum value that can be given to the "
                             "parameter {} is {:.2f}. ({:.2f} "
                             "instead)".format(self.name,
                                               self.max_val,
                                               value))


class ParameterStr(Parameter):
    def __init__(self, name, description, default):
        super().__init__(name, description, default)

    def check_value(self, value):
        if not isinstance(value, str):
            raise TypeError("The value for the parameter {} should be an "
                            "string ({} instead)".format(self.name,
                                                         value.__class__))


class ParameterEnum(Parameter):
    def __init__(self, name, description, allowed_val, default):
        super().__init__(name, description, default)
        self.allowed_val = allowed_val

    def check_value(self, value):
        if value not in self.allowed_val:
            raise ValueError("The value for the parameter {} should be one of "
                             "the allowed values ({}). ({} "
                             "instead)".format(self.name,
                                               str(self.allowed_val),
                                               value))


class Parameters(object):
    __parameters = [
        ParameterInt('attr_int',
                     'An integer attribute',
                     0,
                     None,
                     15),
        ParameterFloat('attr_float',
                       'A float attribute',
                       -100.0,
                       100.0,
                       0.0),
        ParameterStr('attr_str',
                     'A string attribute',
                     'default_value'),
        ParameterEnum('attr_enum',
                      'An enum attribute',
                      ['A', 0, object, None],
                      0)
    ]

    def __init__(self, *args, **kwargs):
        self._values = {}
        for i, value in enumerate(args):
            self.__parameters[i].check_value(value)
            self._values[self.__parameters[i].name] = value

        for key, value in kwargs.items():
            self._values[key] = value

        for parameter in self.__parameters:
            if parameter.name not in self._values:
                self._values[parameter.name] = parameter.default

    def __getitem__(self, key):
        if key not in self._values:
            raise AttributeError('No parameter is named {}'.format(key))
        return self._values[key]
