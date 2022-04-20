import copy
from collections import defaultdict, namedtuple
from dataclasses import dataclass

import getter as get
import numpy as np
import pandas as pd

data = [
    [65.78331, 112.9925],
    [71.51521, 136.4873],
    [69.39874, 153.0269],
    [68.2166, 142.3354],
    [67.78781, 144.2971],
    [68.69784, 123.3024],
]
expected = [
    18.355807678302504,
    18.76077310684635,
    22.33674748017829,
    21.50245817220586,
    22.075457913890467,
    18.36710423289858,
]


def test_lists():

    data_list = copy.deepcopy(data)

    @get.foreach
    @get.fields(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_list), expected)


def test_dict():

    data_dict = defaultdict(list)

    for i in range(len(data)):
        for j, name in enumerate(["height", "weight"]):
            data_dict[name].append(data[i][j])

    @get.asarrays
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_dict), expected)


def test_numpy():

    data_arr = np.asarray(data)

    @get.foreach
    @get.fields(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_arr), expected)


def test_numpy_transposed():

    data_arr = np.asarray(data).T

    @get.fields(names=["height", "weight"])
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_arr), expected)


def test_pandas():

    data_df = pd.DataFrame(data, columns=["height", "weight"])

    @get.fields
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_df), expected)


def test_pandas_apply():

    data_df = pd.DataFrame(data, columns=["height", "weight"])

    @get.fields
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(data_df.apply(bmi, axis=1), expected)


def test_dataclass():
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


def test_namedtuple():
    Measurements = namedtuple("Measurements", ["height", "weight"])

    data_dcs = []
    for row in data:
        data_dcs.append(Measurements(*row))

    @get.foreach
    @get.attributes
    def bmi(weight, height):
        return weight / height**2 * 703

    np.testing.assert_allclose(bmi(data_dcs), expected)
