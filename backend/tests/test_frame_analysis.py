import pytest
import math
from spectral.frame_analysis import (
    calculate_frame_duration,
    calculate_frame_pitch,
    calculate_frame_f1_f2,
)
import json
import os

# Load the JSON file
with open(os.path.join(os.path.realpath(__file__),"../data/frames.json"), "r") as file:
    frame_data = json.load(file)


def test_speed_voiced_frame():
    assert (
        calculate_frame_duration(
            frame_data["voiced-1"]["data"], frame_data["voiced-1"]["fs"]
        )
        == 0.04
    )


def test_speed_unvoiced_frame():
    assert (
        calculate_frame_duration(
            frame_data["unvoiced-1"]["data"], frame_data["unvoiced-1"]["fs"]
        )
        == 0.04
    )


def test_speed_noise_frame():
    assert (
        calculate_frame_duration(
            frame_data["noise-1"]["data"], frame_data["noise-1"]["fs"]
        )
        == 0.04
    )


def test_speed_empty_frame():
    assert calculate_frame_duration([], 48000) == 0


def test_pitch_voiced():
    assert calculate_frame_pitch(
        frame_data["voiced-1"]["data"], frame_data["voiced-1"]["fs"]
    ) == pytest.approx(115.64, 0.01)


def test_pitch_unvoiced():
    assert math.isnan(
        calculate_frame_pitch(
            frame_data["unvoiced-1"]["data"], frame_data["unvoiced-1"]["fs"]
        )
    )


def test_pitch_noise():
    assert math.isnan(
        calculate_frame_pitch(
            frame_data["noise-1"]["data"], frame_data["noise-1"]["fs"]
        )
    )


def test_pitch_empty_frame():
    assert math.isnan(calculate_frame_pitch([], 48000))


def test_formants_voiced_frame():
    formants = calculate_frame_f1_f2(
        frame_data["voiced-1"]["data"], frame_data["voiced-1"]["fs"]
    )
    assert len(formants) == 2
    assert formants[0] == pytest.approx(474.43, 0.01)
    assert formants[1] == pytest.approx(1924.64, 0.01)


def test_formants_unvoiced_frame():
    formants = calculate_frame_f1_f2(
        frame_data["unvoiced-1"]["data"], frame_data["unvoiced-1"]["fs"]
    )
    assert len(formants) == 2
    assert formants[0] == pytest.approx(1495.43, 0.01)
    assert formants[1] == pytest.approx(2157.37, 0.01)


def test_formants_noise_frame():
    formants = calculate_frame_f1_f2(
        frame_data["noise-1"]["data"], frame_data["noise-1"]["fs"]
    )
    assert len(formants) == 2
    assert formants[0] == pytest.approx(192.72, 0.01)
    assert formants[1] == pytest.approx(1864.27, 0.01)


def test_formants_empty_frame():
    formants = calculate_frame_f1_f2([], 0)
    assert len(formants) == 2
    assert math.isnan(formants[0])
    assert math.isnan(formants[1])
