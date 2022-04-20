from functools import wraps
from typing import Callable, Iterable, Sequence


def foreach(func: Callable) -> Callable:
    """
    Apply a function to all the elements of the list

    >>> @foreach
    ... def add1(x):
    ...     return x + 1
    >>> add1([1, 2, 3, 4])
    [2, 3, 4, 5]
    """

    @wraps(func)
    def wrapper(elements: Iterable) -> Sequence:
        results = []
        for elem in elements:
            results.append(func(elem))
        return results

    return wrapper
