# test_capitalize.py

import pytest

from kommons import list_replace


def test_list_replace():
    assert list_replace(["a", "foo", "bar", "nut"], "bar", ["baz", "kokos"]) == ["a", "foo", "baz", "kokos", "nut"]

