import pytest
import math
from spectral.frame_analysis import (
    calculate_frame_duration,
    calculate_frame_pitch,
    calculate_frame_f1_f2,
)
import json
import os
from array import array

# Load the JSON file
with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/frames.json"), "r"
) as file:
    frame_data = json.load(file)


def test_speed_voiced_frame():
    assert (
        calculate_frame_duration(
            array("h", frame_data["voiced-1"]["data"]), frame_data["voiced-1"]["fs"]
        )
        == 0.04
    ), "Expected duration for voiced frame to be 0.04 seconds"


def test_speed_unvoiced_frame():
    assert (
        calculate_frame_duration(
            array("h", frame_data["unvoiced-1"]["data"]), frame_data["unvoiced-1"]["fs"]
        )
        == 0.04
    ), "Expected duration for unvoiced frame to be 0.04 seconds"


def test_speed_noise_frame():
    assert (
        calculate_frame_duration(
            array("h", frame_data["noise-1"]["data"]), frame_data["noise-1"]["fs"]
        )
        == 0.04
    ), "Expected duration for noise frame to be 0.04 seconds"


def test_speed_empty_frame():
    assert (
        calculate_frame_duration(array("h", []), 48000) == 0
    ), "Expected duration for empty frame to be 0 seconds"


def test_pitch_voiced():
    assert calculate_frame_pitch(
        array("h", frame_data["voiced-1"]["data"]), frame_data["voiced-1"]["fs"]
    ) == pytest.approx(
        115.64, 0.01
    ), "Expected pitch for voiced frame to be approximately 115.64 Hz"


def test_pitch_unvoiced():
    assert math.isnan(
        calculate_frame_pitch(
            array("h", frame_data["unvoiced-1"]["data"]), frame_data["unvoiced-1"]["fs"]
        )
    )


def test_pitch_noise():
    assert math.isnan(
        calculate_frame_pitch(
            array("h", frame_data["noise-1"]["data"]), frame_data["noise-1"]["fs"]
        )
    ), "Expected pitch for noise frame to be NaN"


def test_pitch_empty_frame():
    assert math.isnan(
        calculate_frame_pitch(array("h", []), 48000)
    ), "Expected pitch for empty frame to be NaN"


def test_formants_voiced_frame():
    formants = calculate_frame_f1_f2(
        array("h", frame_data["voiced-1"]["data"]), frame_data["voiced-1"]["fs"]
    )
    assert len(formants) == 2, "Expected two formants for voiced frame"
    assert formants[0] == pytest.approx(
        474.43, 0.01
    ), "Expected first formant (f1) for voiced frame to be approximately 474.43 Hz"
    assert formants[1] == pytest.approx(
        1924.64, 0.01
    ), "Expected second formant (f2) for voiced frame to be approximately 1924.64 Hz"


def test_formants_unvoiced_frame():
    formants = calculate_frame_f1_f2(
        array("h", frame_data["unvoiced-1"]["data"]), frame_data["unvoiced-1"]["fs"]
    )
    assert len(formants) == 2, "Expected two formants for unvoiced frame"
    assert formants[0] == pytest.approx(
        1495.43, 0.01
    ), "Expected first formant (f1) for unvoiced frame to be approximately 1495.43 Hz"
    assert formants[1] == pytest.approx(
        2157.37, 0.01
    ), "Expected second formant (f2) for unvoiced frame to be approximately 2157.37 Hz"


def test_formants_noise_frame():
    formants = calculate_frame_f1_f2(
        array("h", frame_data["noise-1"]["data"]), frame_data["noise-1"]["fs"]
    )

    assert len(formants) == 2, "Expected two formants for noise frame"
    assert formants[0] == pytest.approx(
        192.72, 0.01
    ), "Expected first formant (f1) for noise frame to be approximately 192.72 Hz"
    assert formants[1] == pytest.approx(
        1864.27, 0.01
    ), "Expected second formant (f2) for noise frame to be approximately 1864.27 Hz"


def test_formants_empty_frame():
    formants = calculate_frame_f1_f2(array("h", []), 0)
    assert len(formants) == 2, "Expected two formants for empty frame"
    assert math.isnan(
        formants[0]
    ), "Expected first formant (f1) for empty frame to be NaN"
    assert math.isnan(
        formants[1]
    ), "Expected second formant (f2) for empty frame to be NaN"
