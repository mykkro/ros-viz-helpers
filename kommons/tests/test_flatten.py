# test_capitalize.py

import pytest

from kommons import flatten


def test_flatten():
    assert flatten([[1,2],[3],[4,5]]) == [1,2,3,4,5]

