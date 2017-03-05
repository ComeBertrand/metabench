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
        item = args[0]
        item_type = item.__class__.__name__
        item_type = item_type.lower()
        match = True

        for type_name in type_names:
            if type_name.lower() == item_type:
                match = False

        if not match:
            raise NotImplementedError('Function {0.__name__} is not'
                                      ' implemented for {1}'.format(f,
                                                                    item_type))
        else:
            return f(*args, **kwargs)
    return wrapper


def implemented_for(*type_names):
    @decorator
    def wrapper(f, *args, **kwargs):
        item = args[0]
        item_type = item.__class__.__name__
        item_type = item_type.lower()
        match = False

        for type_name in type_names:
            if type_name.lower() == item_type:
                match = True

        if not match:
            raise NotImplementedError('Function {0.__name__} is only '
                                      'implemented for {1}'.format(f,
                                                                   type_names))
        else:
            return f(*args, **kwargs)
    return wrapper
