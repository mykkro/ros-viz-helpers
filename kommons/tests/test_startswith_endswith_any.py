# test_capitalize.py

import pytest

from kommons import startswith_any, endswith_any


def test_startswith_any():
    assert startswith_any("coconut", ["c", "koko", "nut", "coco", "coc"])


def test_endswith_any():
    assert startswith_any("coconut", ["c", "koko", "nut", "coco", "coc"]) 
