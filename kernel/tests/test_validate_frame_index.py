import pytest
from fastapi import HTTPException
from spectral.frame_analysis import validate_frame_index
from array import array


def test_validate_frame_index_valid():
    data = [0] * 100
    frame_index = validate_frame_index(
        array("h", data), {"frame": {"startIndex": 10, "endIndex": 20}}
    )
    assert frame_index == {"startIndex": 10, "endIndex": 20}


def test_validate_frame_index_both_none_indices():
    data = [0] * 100
    assert (
        validate_frame_index(array("h", data), {"frame": {"startIndex": None, "endIndex": None}})
        is None
    )


def test_validate_frame_index_missing_start_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(array("h", data), {"frame": {"startIndex": None, "endIndex": 20}})


def test_validate_frame_index_missing_end_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(array("h", data), {"frame": {"startIndex": 10, "endIndex": None}})


def test_validate_frame_index_start_index_greater_than_end_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(array("h", data), {"frame": {"startIndex": 20, "endIndex": 10}})


def test_validate_frame_index_negative_start_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(array("h", data), {"frame": {"startIndex": -1, "endIndex": 20}})


def test_validate_frame_index_end_index_too_large():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(array("h", data), {"frame": {"startIndex": 10, "endIndex": 200}})


def test_frame_none():
    data = [0] * 100
    frame_index = validate_frame_index(array("h", data), {"frame": None})
    assert frame_index is None
