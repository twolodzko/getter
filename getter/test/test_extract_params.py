import inspect

import pytest
from getter.decorators import _extract_parameters
from getter.getter import Parameter


def no_params():
    ...


def single_param(x):
    ...


def single_param_default(x=1):
    ...


def two_params(x, y):
    ...


def three_params_defaults(x, y=1, z=2):
    ...


@pytest.mark.parametrize(
    "func, expected",
    [
        (
            no_params,
            [],
        ),
        (
            single_param,
            [
                Parameter(
                    "x",
                    inspect.Parameter.empty,
                )
            ],
        ),
        (
            single_param_default,
            [
                Parameter(
                    "x",
                    1,
                )
            ],
        ),
        (
            two_params,
            [
                Parameter(
                    "x",
                    inspect.Parameter.empty,
                ),
                Parameter(
                    "y",
                    inspect.Parameter.empty,
                ),
            ],
        ),
        (
            three_params_defaults,
            [
                Parameter(
                    "x",
                    inspect.Parameter.empty,
                ),
                Parameter(
                    "y",
                    1,
                ),
                Parameter(
                    "z",
                    2,
                ),
            ],
        ),
    ],
)
def test_extract_parameters(func, expected):
    result = _extract_parameters(func)
    assert result == expected
