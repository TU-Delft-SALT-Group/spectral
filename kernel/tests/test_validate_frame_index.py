import pytest
from fastapi import HTTPException
from spectral.main import validate_frame_index


def test_validate_frame_index_valid():
    data = [0] * 100
    frame_index = validate_frame_index(data, 10, 20)
    assert frame_index == {"startIndex": 10, "endIndex": 20}


def test_validate_frame_index_missing_start_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(data, None, 20)


def test_validate_frame_index_missing_end_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(data, 10, None)


def test_validate_frame_index_start_index_greater_than_end_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(data, 20, 10)


def test_validate_frame_index_negative_start_index():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(data, -1, 10)


def test_validate_frame_index_end_index_too_large():
    data = [0] * 100
    with pytest.raises(HTTPException):
        validate_frame_index(data, 10, 200)
