
import os

def read_data(filename: str) -> str:
    """Function to return the whole of the string contents of a file."""
    with open(os.path.join("puzzle_inputs", filename), 'r') as file:
        data = "".join(file.readlines())
    return data


def test_read_data():
    assert read_data('day_.txt') == """testing
testING1
TESTING  2 2 2 

That seems pretty conclusive!!"""