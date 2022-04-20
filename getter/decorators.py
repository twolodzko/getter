import inspect
from functools import wraps
from typing import Any, Callable, Iterable, Mapping, Optional

import numpy as np

from .getter import AttributeGetter, ItemGetter, MaybeNames, Parameter


def _extract_parameters(func: Callable) -> Iterable[Parameter]:
    """
    Extract list of parameters of a function
    """
    params = []
    for param in inspect.signature(func).parameters.values():
        if param.kind == param.POSITIONAL_ONLY:
            raise ValueError("Positional only parameters are not supported")
        if param.kind in {param.VAR_POSITIONAL, param.VAR_KEYWORD}:
            continue
        params.append(Parameter(param.name, param.default))
    return params


def fields(_func: Optional[Callable] = None, *, names: MaybeNames = None) -> Callable:
    """
    Decorate a function so that it takes as an argument data object and the function arguments
    are collected from the object

    :param names: optional list of the names of the data fields
        or mappings from parameter names to names of the data fields

    Access named elements of an object:

    >>> @fields
    ... def get(x, y):
    ...     return x, y
    >>> get({"x": 1, "y": 2, "z": 3})
    (1, 2)

    Provide names for the positional elements of an object:

    >>> @fields(names=["x", "y"])
    ... def get(x, y):
    ...     return x, y
    >>> get([1, 2])
    (1, 2)
    """

    def wrapper(func: Callable) -> Callable:
        getter = ItemGetter(_extract_parameters(func), names)

        @wraps(func)
        def with_data_as_argument(data) -> Any:
            args = getter.collect_from(data)
            return func(**args)

        return with_data_as_argument

    if _func is None:
        return wrapper
    else:
        return wrapper(_func)


def _to_arrays(objs: Mapping[str, Any]) -> Mapping[str, np.ndarray]:
    """
    Convert values in the key -> value mapping to np.ndarray type
    """
    return {key: np.asarray(value) for key, value in objs.items()}


def asarrays(
    _func: Optional[Callable] = None,
    *,
    names: MaybeNames = None,
) -> Callable:
    """
    Decorate a function so that it takes as an argument data object and the function arguments
    are collected from the object

    :param names: optional list of the names of the data fields
        or mappings from parameter names to names of the data fields

    >>> import pandas as pd
    >>> @asarrays
    ... def add(x, y):
    ...     return x + y
    >>> df = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 30]})
    >>> add(df)
    array([11, 22, 33])
    """

    def wrapper(func: Callable) -> Callable:
        getter = ItemGetter(_extract_parameters(func), names)

        @wraps(func)
        def with_data_as_argument(data) -> Any:
            args = getter.collect_from(data)
            args = _to_arrays(args)
            return func(**args)

        return with_data_as_argument

    if _func is None:
        return wrapper
    else:
        return wrapper(_func)


def attributes(_func: Optional[Callable] = None, *, names: MaybeNames = None) -> Callable:
    """
    Decorate a function so that it takes as an argument data object and the function arguments
    are collected from the object

    :param names: optional list of the names of the data fields
        or mappings from parameter names to names of the data fields

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Measurements:
    ...     weight: float
    ...     height: float
    >>> @attributes
    ... def bmi(weight, height):
    ...     return weight / (height / 100) ** 2
    >>> bmi(Measurements(68, 165))
    24.97...
    """

    def wrapper(func: Callable) -> Callable:
        getter = AttributeGetter(_extract_parameters(func), names)

        @wraps(func)
        def with_data_as_argument(data) -> Any:
            args = getter.collect_from(data)
            return func(**args)

        return with_data_as_argument

    if _func is None:
        return wrapper
    else:
        return wrapper(_func)
