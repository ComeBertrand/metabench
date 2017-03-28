"""
File: parameters.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description: Describe and hold the parameters for the metaheuristics and the
problems.
"""


class ParameterDesc(object):
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
        """Check that a value can be the parameter.

        Should be implemented in sub-class.

        """
        raise NotImplementedError("Abstract Class")


class ParameterDescInt(ParameterDesc):
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
        """Check that a value can be an int parameter.

        Raises:
            TypeError: If the value is not an int.
            ValueError: If it does not respect the constraints.

        """
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


class ParameterDescFloat(ParameterDesc):
    """Description of a float parameter.

    Args:
        min_val (float): Minimum value that can be taken by the parameter. If
            None, there is no minimum value.
        max_val (float): Maximum value that can be taken by the parameter. If
            None, there is no maximum value.

    Attributes:
        min_val (float): Minimum value that can be taken by the parameter. If
            None, there is no minimum value.
        max_val (float): Maximum value that can be taken by the parameter. If
            None, there is no maximum value.

    """
    def __init__(self, name, description, min_val, max_val, default):
        super().__init__(name, description, default)
        self.min_val = min_val
        self.max_val = max_val

    def check_value(self, value):
        """Check that a value can be a float parameter.

        Raises:
            TypeError: If the value is not a float.
            ValueError: If it does not respect the constraints.

        """
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


class ParameterDescStr(ParameterDesc):
    """Description of a string parameter."""
    def __init__(self, name, description, default):
        super().__init__(name, description, default)

    def check_value(self, value):
        """Check that a value can be a string parameter.

        Raises:
            TypeError: If the value is not a string.

        """
        if not isinstance(value, str):
            raise TypeError("The value for the parameter {} should be an "
                            "string ({} instead)".format(self.name,
                                                         value.__class__))


class ParameterDescEnum(ParameterDesc):
    """Description of an enumerated parameter.

    Args:
        allowed_val (list): Of anything. It describes the list of values that
            can be taken by the parameter.

    Attributes:
        allowed_val (list): Of anything. It describes the list of values that
            can be taken by the parameter.

    """
    def __init__(self, name, description, allowed_val, default):
        super().__init__(name, description, default)
        self.allowed_val = allowed_val

    def check_value(self, value):
        """Check that a value can be a enum parameter.

        Raises:
            ValueError: If the value is not one of the allowed values.

        """
        if value not in self.allowed_val:
            raise ValueError("The value for the parameter {} should be one of "
                             "the allowed values ({}). ({} "
                             "instead)".format(self.name,
                                               str(self.allowed_val),
                                               value))


class Parameters(object):
    """Hold a list of parameters.

    Parameters are a list of attributes values, indexed by the name given to
    each parameter description in the __parameters attribute (which should be
    given for each sub-class).

    Parameter values can be fetched by attribute getting.

    Example:
        >>> p = Parameters(attr_int=4, attr_float=None)
        >>> p.attr_int
        4
        >>> p.attr_float
        0.0
        >>> p.attr_str
        'default_value'
        >>> p.attr_enum
        0


    Args:
        kwargs (dict): Key-values pair of parameters. The keys must follow the
            names given to the parameters descriptions. If a parameter is not
            given, the default value set in the parameter description will be
            used. If the value of a parameter is set to None, again the default
            value of the parameter description will be used.

    """
    # This attribute must be modified for the parameters sub-classes.
    __parameters = [
        ParameterDescInt('attr_int',
                         'An integer attribute',
                         0,
                         None,
                         15),
        ParameterDescFloat('attr_float',
                           'A float attribute',
                           -100.0,
                           100.0,
                           0.0),
        ParameterDescStr('attr_str',
                         'A string attribute',
                         'default_value'),
        ParameterDescEnum('attr_enum',
                          'An enum attribute',
                          ['A', 0, object, None],
                          0)
    ]

    def __init__(self, **kwargs):
        self._values = {}

        dict_params = {param_desc.name: param_desc for param_desc in
                       self.__parameters}

        for key, value in kwargs.items():
            if key in dict_params:
                parameter_desc = dict_params[key]
                if value is not None:
                    parameter_desc.check_value(value)
                    self._values[key] = value
                else:
                    self._values[key] = parameter_desc.default
            else:
                raise TypeError("'{}' is an invalid keyword for these "
                                "parameters".format(key))

        for parameter_desc in self.__parameters:
            if parameter_desc.name not in self._values:
                self._values[parameter_desc.name] = parameter_desc.default

    def __getattr__(self, key):
        if key not in self._values:
            raise AttributeError('No parameter is named {}'.format(key))
        return self._values[key]

    @classmethod
    def get_parameters_description(cls):
        """Getter for the list of parameters descriptions.

        Returns:
            list: of ParameterDesc.

        """
        return cls.__parameters
