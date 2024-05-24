import pytest
from spectral.main import app, get_db
from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
from scipy.io import wavfile as wv
import os
from unittest.mock import Mock, patch

client = TestClient(app)

# Load the JSON file
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
with open(os.path.join(data_dir, "frames.json"), "r") as file:
    frame_data = json.load(file)

typical_1_fs, typical_1_data = wv.read(
    os.path.join(data_dir, "torgo-dataset/MC02_control_head_sentence1.wav")
)
typical_1_data = typical_1_data.tolist()

with open(
    os.path.join(data_dir, "torgo-dataset/MC02_control_head_sentence1.wav"), mode="rb"
) as f:
    control_sentence = f.read()


@pytest.fixture
def db_mock():
    mock = Mock()
    mock.fetch_file.return_value = {"data": control_sentence, "creationTime": 1, "groundTruth": "hai test"}
    mock.get_transcriptions.return_value = [[{"value": "hi", "start": 0, "end": 1}]]

    yield mock


@pytest.fixture(autouse=True)
def override_dependency(db_mock):
    app.dependency_overrides[get_db] = lambda: db_mock
    yield
    app.dependency_overrides = {}


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
    assert response.json()["detail"] == "Input data did not meet requirements"


def test_fundamental_features_typical_speech():
    response = client.post(
        "/signals/analyze", json={"data": typical_1_data, "fs": typical_1_fs}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is not None
    assert result["pitch"]["time_step"] is not None
    assert result["pitch"]["start_time"] is not None
    assert result["pitch"]["data"] is not None
    assert result["spectrogram"] is not None
    assert result["formants"] is not None
    assert result["formants"]["time_step"] is not None
    assert result["formants"]["window_length"] is not None
    assert result["formants"]["start_time"] is not None
    assert result["formants"]["data"] is not None


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
            "spectrogram_time_step": 0.004,
            "spectrogram_window_length": 0.0025,
            "spectrogram_frequency_step": 15.0,
            "formants_time_step": 0.003,
            "formants_window_length": 0.015,
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is not None
    assert result["pitch"]["time_step"] == pytest.approx(0.01)
    assert result["spectrogram"] is not None
    assert result["spectrogram"]["time_step"] == pytest.approx(0.004)
    assert result["spectrogram"]["window_length"] == pytest.approx(0.0025)
    assert result["spectrogram"]["frequency_step"] == pytest.approx(15)
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
    assert result["spectrogram"] is not None
    assert result["formants"] is not None

    response = client.post(
        "/signals/analyze",
        json={
            "data": typical_1_data,
            "fs": typical_1_fs,
            "spectrogram_time_step": 0,
            "formants_time_step": 0,
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["pitch"] is not None
    assert result["spectrogram"] is None
    assert result["formants"] is None


def test_fundamental_features_fs_zero():
    response = client.post("/signals/analyze", json={"data": typical_1_data, "fs": 0})
    assert response.status_code == 400
    assert response.json()["detail"] == "Input data did not meet requirements"


def test_fundamental_features_empty_signal():
    response = client.post("/signals/analyze", json={"data": [], "fs": 48000})
    assert response.status_code == 200
    result = response.json()
    assert result["duration"] == 0
    assert result["pitch"] is None
    assert result["spectrogram"] is None
    assert result["formants"] is None


def test_signal_correct_mode_file_not_found(db_mock):
    db_mock.fetch_file.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    response = client.get("/signals/modes/simple-info/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_simple_info(db_mock):
    response = client.get("/signals/modes/simple-info/1")
    assert response.status_code == 200
    result = response.json()
    assert result["fileSize"] == 146124
    assert result["fileCreationDate"] == '1970-01-01T00:00:01Z'
    assert result["frame"] is None
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_spectrogram(db_mock):
    response = client.get("/signals/modes/spectrogram/1")
    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_waveform(db_mock):
    response = client.get("/signals/modes/waveform/1")
    assert response.status_code == 200
    result = response.json()
    assert result is None
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_vowel_space(db_mock):
    response = client.get("/signals/modes/vowel-space/1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Vowel-space mode was not given frame"
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_transcription(db_mock):
    response = client.get("/signals/modes/transcription/1")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0][0]["value"] == "hi"
    assert result[0][0]["start"] == 0
    assert result[0][0]["end"] == 1
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 1


def test_signal_transcription_not_found(db_mock):
    db_mock.get_transcriptions.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    response = client.get("/signals/modes/transcription/1")
    assert response.status_code == 500
    assert response.json()["detail"] == "Something went wrong when retrieving the transcriptions of this file"
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 1


def test_signal_mode_wrong_mode(db_mock):
    response = client.get("/signals/modes/wrongmode/1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Mode not found"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_start_index_missing(db_mock):
    response = client.get("/signals/modes/simple-info/1", params={"endIndex": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "no startIndex provided"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_end_index_missing(db_mock):
    response = client.get("/signals/modes/simple-info/1", params={"startIndex": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "no endIndex provided"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_start_index_bigger_than_end_index(db_mock):
    response = client.get(
        "/signals/modes/simple-info/1", params={"startIndex": 2, "endIndex": 1}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "startIndex should be strictly lower than endIndex"
    assert db_mock.fetch_file.call_count == 1

def test_signal_mode_frame_start_index_bigger_than_end_index_equal_numbers(db_mock):
    response = client.get(
        "/signals/modes/simple-info/1", params={"startIndex": 2, "endIndex": 2}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "startIndex should be strictly lower than endIndex"
    assert db_mock.fetch_file.call_count == 1

def test_signal_mode_frame_negative_start_index(db_mock):
    response = client.get(
        "/signals/modes/simple-info/1", params={"startIndex": -1, "endIndex": 1}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "startIndex should be larger or equal to 0"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_too_large_end_index(db_mock):
    response = client.get(
        "/signals/modes/simple-info/1",
        params={
            "startIndex": 0,
            "endIndex": 73041,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "endIndex should be lower than the file length"
    assert db_mock.fetch_file.call_count == 1
    
def test_signal_mode_frame_too_large_boundary(db_mock):
    response = client.get(
        "/signals/modes/simple-info/1",
        params={
            "startIndex": 0,
            "endIndex": 73040,
        },
    )
    assert response.status_code == 200
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_simple_info_with_frame(db_mock):
    response = client.get(
        "/signals/modes/simple-info/1", params={"startIndex": 22500, "endIndex": 23250}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["fileSize"] == 146124
    assert result["fileCreationDate"] == '1970-01-01T00:00:01Z'
    assert result["averagePitch"] == pytest.approx(34.38,0.1)
    assert result["duration"] == pytest.approx(4.565,0.01)
    assert result["frame"] is not None
    assert result["frame"]["duration"] == pytest.approx(0.046875)
    assert result["frame"]["f1"] == pytest.approx(623.19, 0.1)
    assert result["frame"]["f2"] == pytest.approx(1635.4, 0.1)
    assert result["frame"]["pitch"] == pytest.approx(591.6, 0.1)
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_vowel_space_mode_with_frame(db_mock):
    response = client.get(
        "/signals/modes/vowel-space/1", params={"startIndex": 22500, "endIndex": 23250}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["f1"] == pytest.approx(623.19, 0.1)
    assert result["f2"] == pytest.approx(1635.4, 0.1)
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_transcription_db_problem(db_mock):
    db_mock.fetch_file.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    response = client.get("/transcription/deepgram/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert db_mock.fetch_file.call_count == 1


def test_transcription_model_found(db_mock):
    with patch(
        "spectral.transcription.deepgram_transcription"
    ) as mock_deepgram_transcription:
        mock_deepgram_transcription.return_value = [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ]
        response = client.get("/transcription/deepgram/1")
        assert response.status_code == 200
        result = response.json()
        assert result == [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ]
        assert db_mock.fetch_file.call_count == 1
        assert db_mock.store_transcription.call_count == 1


def test_transcription_storing_error(db_mock):
    db_mock.store_transcription.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    with patch(
        "spectral.transcription.deepgram_transcription"
    ) as mock_deepgram_transcription:
        mock_deepgram_transcription.return_value = [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ]
        response = client.get("/transcription/deepgram/1")
        assert response.status_code == 500
        assert response.json()["detail"] == "Something went wrong while storing the transcription"
        assert db_mock.fetch_file.call_count == 1
        assert db_mock.store_transcription.call_count == 1


def test_transcription_model_not_found(db_mock):
    response = client.get("/transcription/non_existant_model/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model was not found"
    assert db_mock.fetch_file.call_count == 1


def test_frame_analyze_invalid_data():
    response = client.post("/frames/analyze", json={"data": "invalid", "fs": 48000})
    assert response.status_code == 422


def test_signal_analyze_invalid_data():
    response = client.post("/signals/analyze", json={"data": "invalid", "fs": 48000})
    assert response.status_code == 422

def test_analyze_signal_mode_invalid_id(db_mock):
    db_mock.fetch_file.side_effect = Exception("Database error")
    response = client.get("/signals/modes/simple-info/invalid_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert db_mock.fetch_file.call_count == 1


def test_transcribe_file_invalid_model(db_mock):
    response = client.get("/transcription/invalid_model/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model was not found"
    assert db_mock.fetch_file.call_count == 1


@pytest.mark.skip(reason="Not implemented")
def test_transcribe_file_no_api_key(db_mock):
    with patch("spectral.transcription.os.getenv") as mock_getenv:
        mock_getenv.return_value = None
        response = client.get("/transcription/deepgram/1")
        assert response.status_code == 500
        assert db_mock.fetch_file.call_count == 1


@pytest.fixture
def mock_db(mocker):
    mock_db_class = mocker.patch("spectral.database.Database")
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.connection = Mock()
    mock_db_instance.close = Mock()
    return mock_db_instance

def test_error_rate_no_ground_truth(db_mock):
    db_mock.fetch_file.return_value["groundTruth"] = None
    
    response = client.get("/signals/modes/error-rate/1")
    
    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 0
    
def test_analyze_error_rate_mode_transcription_retrieval_failure(db_mock):
    db_mock.get_transcriptions.side_effect = Exception("Database error")
    response = client.get("/signals/modes/error-rate/1")
    assert response.status_code == 500
    assert response.json()["detail"] == "Something went wrong when retrieving the transcriptions of this file"
    assert db_mock.fetch_file.call_count == 1
    
def test_error_rate_no_transcription(db_mock):
    db_mock.get_transcriptions.return_value = [[]]
    
    response = client.get("/signals/modes/error-rate/1")
    
    assert response.status_code == 200
    
    result = response.json()
    
    assert result[0]["wordLevel"]["wer"] == 1.0
    assert result[0]["wordLevel"]["mer"] == 1.0
    assert result[0]["wordLevel"]["wil"] == 1.0
    assert result[0]["wordLevel"]["wip"] == 0
    assert result[0]["wordLevel"]["hits"] == 0
    assert result[0]["wordLevel"]["substitutions"] == 0
    assert result[0]["wordLevel"]["insertions"] == 0
    assert result[0]["wordLevel"]["deletions"] == 2
    assert result[0]["wordLevel"]["reference"] == ['hai', 'test']
    assert result[0]["wordLevel"]["hypothesis"] == []
    assert len(result[0]["wordLevel"]["alignments"]) == 1
    assert result[0]["wordLevel"]["alignments"][0] == {'type': 'delete', 'referenceStartIndex': 0, 'referenceEndIndex': 2, 'hypothesisStartIndex': 0, 'hypothesisEndIndex': 0}
    
    assert result[0]["characterLevel"]["cer"] == 1
    assert result[0]["characterLevel"]["hits"] == 0
    assert result[0]["characterLevel"]["substitutions"] == 0
    assert result[0]["characterLevel"]["insertions"] == 0
    assert result[0]["characterLevel"]["deletions"] == 8
    assert result[0]["characterLevel"]["reference"] == ['h', 'a', 'i', ' ', 't', 'e', 's', 't']
    assert result[0]["characterLevel"]["hypothesis"] == []
    assert len(result[0]["characterLevel"]["alignments"]) == 1
    assert result[0]["characterLevel"]["alignments"][0] == {'type': 'delete', 'referenceStartIndex': 0, 'referenceEndIndex':8, 'hypothesisStartIndex': 0, 'hypothesisEndIndex': 0}
    
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 1
    
def test_error_rate_ground_truth(db_mock):    
    response = client.get("/signals/modes/error-rate/1")
    
    assert response.status_code == 200
    result = response.json()
    
    assert result[0]["wordLevel"]["wer"] == 1.0
    assert result[0]["wordLevel"]["mer"] == 1.0
    assert result[0]["wordLevel"]["wil"] == 1.0
    assert result[0]["wordLevel"]["wip"] == 0
    assert result[0]["wordLevel"]["hits"] == 0
    assert result[0]["wordLevel"]["substitutions"] == 1
    assert result[0]["wordLevel"]["insertions"] == 0
    assert result[0]["wordLevel"]["deletions"] == 1
    assert result[0]["wordLevel"]["reference"] == ['hai', 'test']
    assert result[0]["wordLevel"]["hypothesis"] == ['hi']
    assert len(result[0]["wordLevel"]["alignments"]) == 2
    assert result[0]["wordLevel"]["alignments"][0] == {'type': 'substitute', 'referenceStartIndex': 0, 'referenceEndIndex': 1, 'hypothesisStartIndex': 0, 'hypothesisEndIndex': 1}
    assert result[0]["wordLevel"]["alignments"][1] == {'type': 'delete', 'referenceStartIndex': 1, 'referenceEndIndex': 2, 'hypothesisStartIndex': 1, 'hypothesisEndIndex': 1}
    
    assert result[0]["characterLevel"]["cer"] == 0.75
    assert result[0]["characterLevel"]["hits"] == 2
    assert result[0]["characterLevel"]["substitutions"] == 0
    assert result[0]["characterLevel"]["insertions"] == 0
    assert result[0]["characterLevel"]["deletions"] == 6
    assert len(result[0]["characterLevel"]["alignments"]) == 4
    assert result[0]["characterLevel"]["reference"] == ['h', 'a', 'i', ' ', 't', 'e', 's', 't']
    assert result[0]["characterLevel"]["hypothesis"] == ['h', 'i']
    assert result[0]["characterLevel"]["alignments"][0] == {'type': 'equal', 'referenceStartIndex': 0, 'referenceEndIndex': 1, 'hypothesisStartIndex': 0, 'hypothesisEndIndex': 1}
    assert result[0]["characterLevel"]["alignments"][1] == {'type': 'delete', 'referenceStartIndex': 1, 'referenceEndIndex': 2, 'hypothesisStartIndex': 1, 'hypothesisEndIndex': 1}
    assert result[0]["characterLevel"]["alignments"][2] == {'type': 'equal', 'referenceStartIndex': 2, 'referenceEndIndex': 3, 'hypothesisStartIndex': 1, 'hypothesisEndIndex': 2}
    assert result[0]["characterLevel"]["alignments"][3] == {'type': 'delete', 'referenceStartIndex': 3, 'referenceEndIndex': 8, 'hypothesisStartIndex': 2, 'hypothesisEndIndex': 2}
    
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 1