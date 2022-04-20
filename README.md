Imagine interacting with some data, where some operation needs to
be applied the different fields (columns) of it. For example, you
have the [weights and heights] data and want to [calculate the BMI].

```
height   weight
65.78331 112.9925
71.51521 136.4873
69.39874 153.0269
68.2166  142.3354
67.78781 144.2971
68.69784 123.3024
...
```

This data may be stored in different formats, for example a Python
list of lists, dictionary, Pandas DataFrame, etc. Interacting with
those data objects often leads to clumsy code like below.

```python
def bmi(data):
    return data["weight"] / data["height"]**2 * 703
```

It would be much easier if we could skip the getters in the code
and just write a function like this:

```python
def bmi(weight, height):
    return weight / height**2 * 703
```

The *getter* package implements [Python decorators] that enable 
you to use the "simple" functions without using the getters
explicitly in the code, as this is handled by the decorator.
The resulting code is:

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

The decorated function reads the data fields directly from
the data object, using the names of the function arguments
to identify appropriate fields in the data object.

It is also possible to interact with data object without
named fields by providing them to the decorator. In the
example below I also use the `foreach` decorator that 
applies the function to every element of the outer list.

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
pip install git+https://github.com/twolodzko/geetter.git#egg=getter
```

or clone the repository and run

```shell
make install
```


 [weights and heights]: https://www.kaggle.com/datasets/burnoutminer/heights-and-weights-dataset
 [calculate the BMI]: https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
 [Python decorators]: https://realpython.com/primer-on-python-decorators/
