# test_capitalize.py

import pytest

from kommons import get_trailing_number


def test_get_trailing_number():
    assert get_trailing_number("Batman1234") == 1234


def test_get_trailing_number_none():
    assert get_trailing_number("Batman1234c") is None
