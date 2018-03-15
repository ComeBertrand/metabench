import pytest

from metabench.tests.fixtures import *
from metabench.parameters import *


def test_parameter_desc():
    p = ParameterDesc('test_param_desc', 'Used for testing purpose', 'Bla')
    assert p.name == 'test_param_desc'
    assert p.description == 'Used for testing purpose'
    assert p.default == 'Bla'

    with pytest.raises(NotImplementedError):
        p.check_value(0)


def test_parameter_desc_int():
    p_int = ParameterDescInt('test_param_desc_int', 'Used for testing purpose', 0, 10, 5)
    assert p_int.min_val == 0
    assert p_int.max_val == 10

    with pytest.raises(TypeError):
        p_int.check_value('a')
    with pytest.raises(TypeError):
        p_int.check_value(None)
    with pytest.raises(TypeError):
        p_int.check_value(1.0)

    p_int.check_value(0)
    with pytest.raises(ValueError):
        p_int.check_value(-1)

    p_int.check_value(10)
    with pytest.raises(ValueError):
        p_int.check_value(11)

    p_int = ParameterDescInt('test_param_desc_int', 'Used for testing purpose', None, 10, 5)
    p_int.check_value(-9999)
    p_int.check_value(10)
    with pytest.raises(ValueError):
        p_int.check_value(11)

    p_int = ParameterDescInt('test_param_desc_int', 'Used for testing purpose', 0, None, 5)
    p_int.check_value(9999)
    p_int.check_value(0)
    with pytest.raises(ValueError):
        p_int.check_value(-1)


def test_parameter_desc_float():
    p_float = ParameterDescFloat('test_param_desc_float', 'Used for testing purpose', 0.0, 10.0, 5.0)
    assert p_float.min_val == 0.0
    assert p_float.max_val == 10.0

    with pytest.raises(TypeError):
        p_float.check_value('a')
    with pytest.raises(TypeError):
        p_float.check_value(None)
    with pytest.raises(TypeError):
        p_float.check_value(1)

    p_float.check_value(0.0)
    with pytest.raises(ValueError):
        p_float.check_value(-0.1)

    p_float.check_value(10.0)
    with pytest.raises(ValueError):
        p_float.check_value(10.1)

    p_float = ParameterDescFloat('test_param_desc_float', 'Used for testing purpose', None, 10.0, 5.0)
    p_float.check_value(-9999.0)
    p_float.check_value(10.0)
    with pytest.raises(ValueError):
        p_float.check_value(10.1)

    p_float = ParameterDescFloat('test_param_desc_float', 'Used for testing purpose', 0.0, None, 5.0)
    p_float.check_value(9999.0)
    p_float.check_value(0.0)
    with pytest.raises(ValueError):
        p_float.check_value(-0.1)


def test_parameter_desc_str():
    p_str = ParameterDescStr('test_param_desc_str', 'Used for testing purpose', 'default_str')

    with pytest.raises(TypeError):
        p_str.check_value(0.1)
    with pytest.raises(TypeError):
        p_str.check_value(None)
    with pytest.raises(TypeError):
        p_str.check_value(1)


def test_parameter_desc_enum():
    p_enum = ParameterDescEnum('test_param_desc_float', 'Used for testing purpose', ['A', 0, object, None], 0)
    p_enum.check_value('A')
    p_enum.check_value(0)
    p_enum.check_value(object)
    p_enum.check_value(None)

    with pytest.raises(ValueError):
        p_enum.check_value('B')
    with pytest.raises(ValueError):
        p_enum.check_value(1)


def test_empty_parameters_creation():
    descs = Parameters.get_parameters_description()

    p = Parameters()
    for param_desc in descs:
        val = getattr(p, param_desc.name)
        assert val == param_desc.default


def test_some_parameters_creation(param_creation_some):
    descs = Parameters.get_parameters_description()

    p = Parameters(**param_creation_some)

    for param_desc in descs:
        val = getattr(p, param_desc.name)
        if param_desc.name in param_creation_some:
            assert val == param_creation_some[param_desc.name]
        else:
            assert val == param_desc.default


def test_all_parameters_creation(param_creation_all):
    descs = Parameters.get_parameters_description()

    p = Parameters(**param_creation_all)

    for param_desc in descs:
        val = getattr(p, param_desc.name)
        assert val == param_creation_all[param_desc.name]
