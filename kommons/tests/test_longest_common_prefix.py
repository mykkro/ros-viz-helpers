# test_capitalize.py

import pytest

from kommons import longest_common_prefix


def test_longest_common_prefix():
    assert longest_common_prefix("Bat/man1234", "Bat/3") == "Bat/"

