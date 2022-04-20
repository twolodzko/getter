from collections import namedtuple
from dataclasses import dataclass

import getter as get
import numpy as np
import pandas as pd
import pytest


def test_arrays_with_default():
    @get.asarrays
    def add(x, y=100):
        return x + y

    data = {
        "x": [1, 2],
        "z": [2, 3],
    }

    np.testing.assert_array_almost_equal(add(data), np.asarray([101, 102]))


@pytest.mark.parametrize(
    "example",
    [
        {
            "y": [1, 2],
            "z": [2, 3],
        },
        pd.DataFrame.from_dict(
            {
                "y": [1, 2],
                "z": [2, 3],
            }
        ),
    ],
)
def test_arrays_missing_column(example):
    @get.fields
    def add(x, y=100):
        return x + y

    with pytest.raises(KeyError):
        add(example)


@pytest.mark.parametrize(
    "example, names, expected",
    [
        (
            {
                "x": [1, 2],
                "y": [10, 20],
            },
            None,
            np.asarray([11, 22]),
        ),
        (
            pd.DataFrame.from_dict(
                {
                    "x": [1, 2],
                    "y": [10, 20],
                }
            ),
            None,
            np.asarray([11, 22]),
        ),
        (
            [
                [1, 2],
                [10, 20],
            ],
            ["x", "y"],
            np.asarray([11, 22]),
        ),
        (
            [
                [1, 2],
                [10, 20],
                [100, 200],  # should ignore this
            ],
            {"x": 0, "y": 1},
            np.asarray([11, 22]),
        ),
        (
            pd.DataFrame.from_dict(
                {
                    "x_with_a_long_name": [1, 2],
                    "y_with_a_long_name": [10, 20],
                }
            ),
            {"x": "x_with_a_long_name", "y": "y_with_a_long_name"},
            np.asarray([11, 22]),
        ),
    ],
)
def test_arrays(example, names, expected):
    @get.asarrays(names=names)
    def add(x, y):
        return x + y

    result = add(example)
    np.testing.assert_almost_equal(result, expected)


def test_with_dataclass():
    @dataclass
    class Measurements:
        weight: float
        height: float

    @get.attributes
    def bmi(weight, height):
        return weight / (height / 100) ** 2

    assert (bmi(Measurements(68, 165)) - 24.98) < 0.1


def test_with_namedtuple():
    Measurements = namedtuple("Measurements", ["weight", "height"])

    @get.attributes
    def bmi(weight, height):
        return weight / (height / 100) ** 2

    assert (bmi(Measurements(68, 165)) - 24.98) < 0.1
