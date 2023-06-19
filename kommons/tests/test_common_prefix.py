# test_capitalize.py

import pytest

from kommons import common_prefix


def test_common_prefix():
    assert common_prefix(["Bat/man1234", "Bat/3", "Batman", "Ba"]) == "Ba"

