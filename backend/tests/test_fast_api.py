import pytest
from spectral.main import app
from fastapi.testclient import TestClient
import json
from scipy.io import wavfile as wv
import os

client = TestClient(app)

# Load the JSON file
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/frames.json"), "r") as file:
    frame_data = json.load(file)

typical_1_fs, typical_1_data = wv.read(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/torgo-dataset/MC02_control_head_sentence1.wav")
)
typical_1_data = typical_1_data.tolist()


def test_voiced_frame():
    response = client.post("/frames/analyze", json=frame_data["voiced-1"])
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["duration"] == pytest.approx(0.04)
    assert response_data["pitch"] == pytest.approx(115.64, 0.01)
    assert response_data["f1"] == pytest.approx(474.43, 0.01)
    assert response_data["f2"] == pytest.approx(1924.64, 0.01)


def test_noise_frame():
    response = client.post("/frames/analyze", json=frame_data["noise-1"])
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["duration"] == pytest.approx(0.04)
    assert response_data["pitch"] is None
    assert response_data["f1"] == pytest.approx(192.72, 0.01)
    assert response_data["f2"] == pytest.approx(1864.27, 0.01)


def test_empty_frame():
    response = client.post("/frames/analyze", json={"data": [], "fs": 48000})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["duration"] == 0
    assert response_data["pitch"] is None
    assert response_data["f1"] is None
    assert response_data["f2"] is None


def test_missing_argument():
    response = client.post("/frames/analyze", json={"fs": 48000})
    assert response.status_code == 422


def test_zero_fs():
    response = client.post("/frames/analyze", json={"data": [], "fs": 0})
    assert response.status_code == 400


def test_fundamental_features_typical_speech():
    response = client.post(
        "/signals/analyze", json={"data": typical_1_data, "fs": typical_1_fs}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is not None
    assert result["spectogram"] is not None
    assert result["formants"] is not None


def test_fundamental_features_missing_params():
    response = client.post("/signals/analyze", json={"data": typical_1_data})
    assert response.status_code == 422
    response = client.post("/signals/analyze", json={"fs": typical_1_fs})
    assert response.status_code == 422
    response = client.post("/signals/analyze", json={})
    assert response.status_code == 422


def test_fundamental_features_typical_own_params_correct():
    response = client.post(
        "/signals/analyze",
        json={
            "data": typical_1_data,
            "fs": typical_1_fs,
            "pitch_time_step": 0.01,
            "spectogram_time_step": 0.004,
            "spectogram_window_length": 0.0025,
            "spectogram_frequency_step": 15.0,
            "formants_time_step": 0.003,
            "formants_window_length": 0.015,
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is not None
    assert result["pitch"]["time_step"] == pytest.approx(0.01)
    assert result["spectogram"] is not None
    assert result["spectogram"]["time_step"] == pytest.approx(0.004)
    assert result["spectogram"]["window_length"] == pytest.approx(0.0025)
    assert result["spectogram"]["frequency_step"] == pytest.approx(15)
    assert result["formants"] is not None
    assert result["formants"]["time_step"] == pytest.approx(0.003)
    assert result["formants"]["window_length"] == pytest.approx(0.015)


def test_fundamental_features_typical_own_params_errors():
    response = client.post(
        "/signals/analyze",
        json={"data": typical_1_data, "fs": typical_1_fs, "pitch_time_step": 0},
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is None
    assert result["spectogram"] is not None
    assert result["formants"] is not None
    response = client.post(
        "/signals/analyze",
        json={
            "data": typical_1_data,
            "fs": typical_1_fs,
            "spectogram_time_step": 0,
            "formants_time_step": 0,
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is not None
    assert result["spectogram"] is None
    assert result["formants"] is None


def test_fundamental_features_fs_zero():
    response = client.post("/signals/analyze", json={"data": typical_1_data, "fs": 0})
    assert response.status_code == 400


def test_fundamental_features_empty_signal():
    response = client.post("/signals/analyze", json={"data": [], "fs": 48000})
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == 0
    assert result["pitch"] is None
    assert result["spectogram"] is None
    assert result["formants"] is None
