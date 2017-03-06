"""
File: decorators.py
Author: Come Bertrand
Email: bertrand.cosme@gmail.com
Github: https://github.com/ComeBertrand
Description:
"""

from decorator import decorator


def not_implemented_for(*type_names):
    @decorator
    def wrapper(f, *args, **kwargs):
        solution = args[0]
        enc_type = solution.encoding.__class__.__name__
        enc_type = enc_type.lower()
        match = True

        for type_name in type_names:
            if type_name.lower() == enc_type:
                match = False
                break

        if not match:
            raise NotImplementedError('Function {0.__name__} is not'
                                      ' implemented for {1}'.format(f,
                                                                    enc_type))
        else:
            return f(*args, **kwargs)
    return wrapper


def implemented_for(*type_names):
    @decorator
    def wrapper(f, *args, **kwargs):
        solution = args[0]
        enc_type = solution.encoding.__class__.__name__
        enc_type = enc_type.lower()
        match = False

        for type_name in type_names:
            if type_name.lower() == enc_type:
                match = True
                break

        if not match:
            raise NotImplementedError('Function {0.__name__} is only '
                                      'implemented for {1}'.format(f,
                                                                   type_names))
        else:
            return f(*args, **kwargs)
    return wrapper
