from src.app.utils import calculate_gaps
import pytest

def test_calculate_gaps_basic():
    assert calculate_gaps([1,3,4,8]) == [2,1,4]

def test_calculate_gaps_single_element():
    assert calculate_gaps([5]) == []

def test_calculate_gaps_bad_type():
    with pytest.raises(TypeError):
        calculate_gaps('not-a-list')
