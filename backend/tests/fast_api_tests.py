import pytest
from spectral.main import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)

# Load the JSON file
with open("data/frames.json", "r") as file:
    frame_data = json.load(file)


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


def test_negative_fs():
    response = client.post("/frames/analyze", json={"data": [], "fs": 0})
    assert response.status_code == 400
