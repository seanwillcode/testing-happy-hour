from unittest import TestCase

import pytest


def sum(x, y):
    return x + y


class TestExample(TestCase):
    def setUp(self):
        self.x = 1
        self.y = 2

    def test_sum_1_and_2_equals_3(self):
        self.assertEqual(sum(self.x, self.y), 3)


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (1, 2, 3),
        (2, 2, 4),
    ],
)
def test_example(x, y, expected):
    assert sum(x, y) == expected
