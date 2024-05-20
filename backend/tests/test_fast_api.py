import pytest
from spectral.main import app, get_db
from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
from scipy.io import wavfile as wv
import os
from spectral.database import Database
from mock import Mock, MagicMock

dbMock = None

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
 
def override_get_db():
    yield dbMock
       
def test_signal_correct_mode_file_not_found():
    global dbMock
    dbMock = MagicMock()
    dbMock.fetch_file.side_effect = HTTPException(status_code=500, detail='database error')
    app.dependency_overrides[get_db] = override_get_db
    response = client.get("/signals/modes/wrongmode/1")
    assert response.status_code == 404
    assert dbMock.fetch_file.call_count == 1
    
def setup_db_mock():
    global dbMock
    dbMock = MagicMock()
    
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/torgo-dataset/MC02_control_head_sentence1.wav"), mode="rb") as f:
        dbMock.fetch_file.return_value = {"data": f.read(), "creationTime": 1}
    
    dbMock.get_transcriptions.return_value = [{"value":"hi", "start": 0, "end": 1}]    
    app.dependency_overrides[get_db] = override_get_db
           
def test_signal_correct_simple_info():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1")
    assert response.status_code == 200
    result = response.json()
    assert result["fileSize"] == 146124
    assert result["fileCreationDate"] == 1
    assert result["frame"] is None
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_correct_spectogram():
    setup_db_mock()
    response = client.get("/signals/modes/spectogram/1")
    assert response.status_code == 501
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_correct_waveform():
    setup_db_mock()
    response = client.get("/signals/modes/waveform/1")
    assert response.status_code == 200
    result = response.json()
    assert result is None
    assert dbMock.fetch_file.call_count == 1

def test_signal_correct_vowel_space():
    setup_db_mock()
    response = client.get("/signals/modes/vowel-space/1")
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_correct_transcription():
    setup_db_mock()
    response = client.get("/signals/modes/transcription/1")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]["value"] == "hi"
    assert result[0]["start"] == 0
    assert result[0]["end"] == 1
    assert dbMock.fetch_file.call_count == 1
    assert dbMock.get_transcriptions.call_count == 1
    
def test_signal_mode_wrong_mode():
    setup_db_mock()
    response = client.get("/signals/modes/wrongmode/1")
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1


def test_signal_mode_frame_start_index_missing():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1", params={"endIndex": 1})
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1

def test_signal_mode_frame_end_index_missing():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1", params={"startIndex": 1})
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_mode_frame_start_index_bigger_than_end_index():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1", params={"startIndex": 2,"endIndex": 1})
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_mode_frame_negative_start_index():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1", params={"startIndex": -1,"endIndex": 1})
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_mode_frame_too_large_end_index():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1", params={"startIndex": 2,"endIndex": len(dbMock.fetch_file.return_value["data"])})
    assert response.status_code == 400
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_mode_simple_info_with_frame():
    setup_db_mock()
    response = client.get("/signals/modes/simple-info/1", params={"startIndex": 22500,"endIndex": 23250})
    assert response.status_code == 200
    result = response.json()
    assert result["fileSize"] == 146124
    assert result["fileCreationDate"] == 1
    assert result["frame"] is not None
    assert result["frame"]["duration"] == pytest.approx(0.046875)
    assert result["frame"]["f1"] == pytest.approx(623.19,0.1)
    assert result["frame"]["f2"] == pytest.approx(1635.4,0.1)
    assert result["frame"]["pitch"] == pytest.approx(591.6,0.1)
    assert dbMock.fetch_file.call_count == 1
    
def test_signal_mode_vowel_space_mode_with_frame():
    setup_db_mock()
    response = client.get("/signals/modes/vowel-space/1", params={"startIndex": 22500,"endIndex": 23250})
    assert response.status_code == 200
    result = response.json()
    assert result["f1"] == pytest.approx(623.19,0.1)
    assert result["f2"] == pytest.approx(1635.4,0.1)
    assert dbMock.fetch_file.call_count == 1