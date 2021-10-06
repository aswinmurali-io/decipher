"""
Singleton meta class implementation in python.
"""

import warnings
import functools

from typing import Dict, Any


class Singleton(type):
    """
    Singeton implementation in python to prevent multiple
    instance of a class to exist.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs) -> Dict[type, Any]:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func
