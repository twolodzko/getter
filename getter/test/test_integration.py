from collections import defaultdict, namedtuple
from dataclasses import dataclass

import getter as get
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def data():
    return [
        [65.78331, 112.9925],
        [71.51521, 136.4873],
        [69.39874, 153.0269],
        [68.2166, 142.3354],
        [67.78781, 144.2971],
        [68.69784, 123.3024],
    ]


@pytest.fixture
def expected():
    return [
        18.355807678302504,
        18.76077310684635,
        22.33674748017829,
        21.50245817220586,
        22.075457913890467,
        18.36710423289858,
    ]


def test_list_of_records(data, expected):
    @get.foreach
    @get.fields(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data), expected)


def test_list_of_lists(data, expected):

    data_list = [[], []]
    for i in range(len(data)):
        for j in range(2):
            data_list[j].append(data[i][j])
    # [ [65, ...], [112, ...] ]

    @get.asarrays(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_list), expected)


def test_dict(data, expected):

    data_dict = defaultdict(list)

    for i in range(len(data)):
        for j, name in enumerate(["height", "weight"]):
            data_dict[name].append(data[i][j])
    # { "height": [...], "weight": [...] }

    @get.asarrays
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_dict), expected)


def test_list_of_dicts(data, expected):

    data_dicts = []
    for row in data:
        data_dicts.append(dict(zip(["height", "weight"], row)))
    # [ { "height": 65, "weight": 112 }, { "height": ... }, ... ]

    @get.foreach
    @get.fields
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_dicts), expected)


def test_numpy(data, expected):

    # column major
    data_arr = np.asarray(data)

    @get.foreach
    @get.fields(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_arr), expected)


def test_numpy_transposed(data, expected):

    # row major, Numpy convention
    data_arr = np.asarray(data).T

    @get.fields(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_arr), expected)


def test_pandas(data, expected):

    data_df = pd.DataFrame(data, columns=["height", "weight"])

    @get.fields
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_df), expected)


def test_pandas_apply(data, expected):

    data_df = pd.DataFrame(data, columns=["height", "weight"])

    @get.fields
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(data_df.apply(bmi, axis=1), expected)


def test_dataclass(data, expected):
    @dataclass
    class Measurements:
        height: float
        weight: float

    data_dcs = []
    for row in data:
        data_dcs.append(Measurements(*row))

    @get.foreach
    @get.attributes
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_dcs), expected)


def test_namedtuple(data, expected):

    Measurements = namedtuple("Measurements", ["height", "weight"])

    data_dcs = []
    for row in data:
        data_dcs.append(Measurements(*row))

    @get.foreach
    @get.attributes
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_dcs), expected)
