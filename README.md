Imagine interacting with some data, where some operation needs to
be applied the different fields (columns) of it. For example, you
have the [weights and heights] data and want to [calculate the BMI].
The data may be stored as a Python list of lists, dictionary,
Pandas DataFrame, Numpy array, etc. To access appropriate fields
of the data object, you need to use the [`__getitem__`] methods.
The resulting code has repetitive calls to the getters.

```python
def bmi(data):
    return data["weight"] / data["height"]**2 * 703
```

Wouldn't it be nicer if instead we could skip the getters
and just write a function like below?

```python
def bmi(weight, height):
    return weight / height**2 * 703
```

The *getter* package implements [Python decorators] that transforms
the decorated functions so that they take the as argument the data
objects and extract the fields for us.

```python
import pandas as pd
import getter as get

data = pd.DataFrame(
    [[65.78331, 112.9925],
     [71.51521, 136.4873],
     [69.39874, 153.0269],
     [68.2166, 142.3354],
     [67.78781, 144.2971],
     [68.69784, 123.3024]],
  columns=["height", "weight"])

@get.fields
def bmi(weight, height):
    return weight / height**2 * 703

data["bmi"] = bmi(data)
```

It is also possible to interact with data object that
doesn't have named fields. In such a case, provide the names
as an argument to the decorator. In the example below, I
additionally use the `foreach` decorator that works like `map`
function, applying the decorated function to each element
of the sequence.

```python
data = [
 [65.78331, 112.9925],
 [71.51521, 136.4873],
 [69.39874, 153.0269],
 [68.2166, 142.3354],
 [67.78781, 144.2971],
 [68.69784, 123.3024]]

@get.foreach
@get.fields(names=["height", "weight"])
def bmi(weight, height):
    return weight / height**2 * 703

bmi(data)
```

## Installation

To install the package using pip run the following command:

```shell
pip install git+https://github.com/twolodzko/getter.git#egg=getter
```

or clone the repository and run

```shell
make install
```


 [weights and heights]: https://www.kaggle.com/datasets/burnoutminer/heights-and-weights-dataset
 [calculate the BMI]: https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
 [Python decorators]: https://realpython.com/primer-on-python-decorators/
 [`__getitem__`]: https://docs.python.org/3/reference/datamodel.html#object.__getitem__
