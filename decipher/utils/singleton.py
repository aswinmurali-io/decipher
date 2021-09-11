"""
Singleton meta class implementation in python.
"""

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
