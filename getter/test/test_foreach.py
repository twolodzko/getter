import getter as get
from getter.foreach import foreach


def test_foreach():
    example = [
        ["1", "A"],
        ["2", "B"],
        ["3", "C"],
    ]

    expected = ["1A", "2B", "3C"]

    @foreach
    def paste(args):
        return "".join(args)

    assert paste(example) == expected


def test_foreach_and_getter():

    example = [
        {"x": 1, "y": 10},
        {"x": 2, "y": 20},
        {"x": 3, "y": 30},
        {"x": 4, "y": 40},
    ]

    @foreach
    @get.fields
    def add(x, y):
        return x + y

    assert add(example) == [11, 22, 33, 44]
