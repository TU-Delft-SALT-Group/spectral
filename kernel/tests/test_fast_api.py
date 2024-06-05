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
def file_state():
    return {
        "id": 1,
        "name": "something",
        "cycleEnabled": True,
        "frame": {
            "startIndex": 1,
            "endIndex": 200,
        },
        "transcriptions": [[]],
    }


@pytest.fixture
def db_mock():
    mock = Mock()
    mock.fetch_file.return_value = {
        "data": control_sentence,
        "creationTime": 1,
        "groundTruth": "hai test",
    }
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


def test_signal_correct_mode_file_not_found(db_mock, file_state):
    db_mock.fetch_file.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_simple_info(db_mock, file_state):
    file_state["frame"] = None
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["fileSize"] == 146124
    assert result["fileCreationDate"] == "1970-01-01T00:00:01Z"
    assert result["frame"] is None
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_spectrogram(db_mock, file_state):
    response = client.get(
        "/signals/modes/spectrogram", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.fetch_file.call_count == 0


def test_signal_correct_waveform(db_mock, file_state):
    response = client.get(
        "/signals/modes/waveform", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    result = response.json()
    assert result is None
    assert db_mock.fetch_file.call_count == 0


def test_signal_correct_vowel_space(db_mock, file_state):
    response = client.get(
        "/signals/modes/vowel-space", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    assert response.json() == {"f1": 1242.857422568559, "f2": 2503.8350190318893}
    assert db_mock.fetch_file.call_count == 1


def test_signal_correct_transcription(db_mock, file_state):
    response = client.get(
        "/signals/modes/transcription", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    assert response.json() is None


def test_signal_mode_wrong_mode(db_mock, file_state):
    response = client.get(
        "/signals/modes/wrongmode", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 422
    assert db_mock.fetch_file.call_count == 0


def test_signal_mode_frame_start_index_missing(db_mock, file_state):
    file_state["frame"] = {"endIndex": 1}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "no startIndex provided"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_end_index_missing(db_mock, file_state):
    file_state["frame"] = {"startIndex": 1}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "no endIndex provided"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_start_index_bigger_than_end_index(db_mock, file_state):
    file_state["frame"] = {"startIndex": 2, "endIndex": 1}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "startIndex should be strictly lower than endIndex"
    )
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_start_index_bigger_than_end_index_equal_numbers(
    db_mock, file_state
):
    file_state["frame"] = {"startIndex": 2, "endIndex": 2}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"] == "startIndex should be strictly lower than endIndex"
    )
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_negative_start_index(db_mock, file_state):
    file_state["frame"] = {"startIndex": -1, "endIndex": 2}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "startIndex should be larger or equal to 0"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_too_large_end_index(db_mock, file_state):
    file_state["frame"] = {"startIndex": 0, "endIndex": 73041}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "endIndex should be lower than the file length"
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_frame_too_large_boundary(db_mock, file_state):
    file_state["frame"] = {"startIndex": 0, "endIndex": 73040}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_simple_info_with_frame(db_mock, file_state):
    file_state["frame"] = {"startIndex": 22500, "endIndex": 23250}
    response = client.get(
        "/signals/modes/simple-info", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["fileSize"] == 146124
    assert result["fileCreationDate"] == "1970-01-01T00:00:01Z"
    assert result["averagePitch"] == pytest.approx(34.38, 0.1)
    assert result["duration"] == pytest.approx(4.565, 0.01)
    assert result["frame"] is not None
    assert result["frame"]["duration"] == pytest.approx(0.046875)
    assert result["frame"]["f1"] == pytest.approx(623.19, 0.1)
    assert result["frame"]["f2"] == pytest.approx(1635.4, 0.1)
    assert result["frame"]["pitch"] == pytest.approx(591.6, 0.1)
    assert db_mock.fetch_file.call_count == 1


def test_signal_mode_vowel_space_mode_with_frame(db_mock, file_state):
    file_state["frame"] = {"startIndex": 22500, "endIndex": 23250}
    response = client.get(
        "/signals/modes/vowel-space", params={"fileState": json.dumps(file_state)}
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
    response = client.get("/transcription/deepgram/session/1")
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
        response = client.get("/transcription/deepgram/session/1")
        assert response.status_code == 200
        result = response.json()
        assert result == [
            {"value": "", "start": 0, "end": 0.5},
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "", "start": 1.0, "end": 1.5},
            {"value": "word2", "start": 1.5, "end": 2.0},
            {"end": 4.565, "start": 2.0, "value": ""},
        ]
        assert db_mock.fetch_file.call_count == 1


def test_transcription_model_not_found(db_mock):
    response = client.get("/transcription/non_existant_model/session/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model was not found"
    assert db_mock.fetch_file.call_count == 1


def test_frame_analyze_invalid_data():
    response = client.post("/frames/analyze", json={"data": "invalid", "fs": 48000})
    assert response.status_code == 422


def test_signal_analyze_invalid_data():
    response = client.post("/signals/analyze", json={"data": "invalid", "fs": 48000})
    assert response.status_code == 422


def test_analyze_signal_mode_invalid_id(db_mock, file_state):
    file_state["id"] = "invalid_id"
    db_mock.fetch_file.side_effect = Exception("Database error")
    response = client.get(
        "/signals/modes/vowel-space", params={"fileState": json.dumps(file_state)}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"
    assert db_mock.fetch_file.call_count == 1


def test_transcribe_file_invalid_model(db_mock):
    response = client.get("/transcription/invalid_model/session/1")
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


def test_error_rate_no_ground_truth(db_mock, file_state):
    db_mock.fetch_file.return_value["groundTruth"] = None
    response = client.get(
        "/signals/modes/error-rate", params={"fileState": json.dumps(file_state)}
    )

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_no_transcription(db_mock, file_state):
    response = client.get(
        "/signals/modes/error-rate", params={"fileState": json.dumps(file_state)}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["groundTruth"] == "hai test"

    word_level = result["errorRates"][0]["wordLevel"]

    assert word_level["wer"] == 1.0
    assert word_level["mer"] == 1.0
    assert word_level["wil"] == 1.0
    assert word_level["wip"] == 0
    assert word_level["hits"] == 0
    assert word_level["substitutions"] == 0
    assert word_level["insertions"] == 0
    assert word_level["deletions"] == 2
    assert word_level["reference"] == ["hai", "test"]
    assert word_level["hypothesis"] == []
    assert len(word_level["alignments"]) == 1
    assert word_level["alignments"][0] == {
        "type": "delete",
        "referenceStartIndex": 0,
        "referenceEndIndex": 2,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 0,
    }

    character_level = result["errorRates"][0]["characterLevel"]

    assert character_level["cer"] == 1
    assert character_level["hits"] == 0
    assert character_level["substitutions"] == 0
    assert character_level["insertions"] == 0
    assert character_level["deletions"] == 8
    assert character_level["reference"] == ["h", "a", "i", " ", "t", "e", "s", "t"]
    assert character_level["hypothesis"] == []
    assert len(character_level["alignments"]) == 1
    assert character_level["alignments"][0] == {
        "type": "delete",
        "referenceStartIndex": 0,
        "referenceEndIndex": 8,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 0,
    }

    assert db_mock.fetch_file.call_count == 1


def test_error_rate_ground_truth(db_mock, file_state):
    file_state["transcriptions"] = [[{"value": "hi"}]]
    response = client.get(
        "/signals/modes/error-rate", params={"fileState": json.dumps(file_state)}
    )

    assert response.status_code == 200
    result = response.json()

    assert result["groundTruth"] == "hai test"

    word_level = result["errorRates"][0]["wordLevel"]

    assert word_level["wer"] == 1.0
    assert word_level["mer"] == 1.0
    assert word_level["wil"] == 1.0
    assert word_level["wip"] == 0
    assert word_level["hits"] == 0
    assert word_level["substitutions"] == 1
    assert word_level["insertions"] == 0
    assert word_level["deletions"] == 1
    assert word_level["reference"] == ["hai", "test"]
    assert word_level["hypothesis"] == ["hi"]
    assert len(word_level["alignments"]) == 2
    assert word_level["alignments"][0] == {
        "type": "substitute",
        "referenceStartIndex": 0,
        "referenceEndIndex": 1,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 1,
    }
    assert word_level["alignments"][1] == {
        "type": "delete",
        "referenceStartIndex": 1,
        "referenceEndIndex": 2,
        "hypothesisStartIndex": 1,
        "hypothesisEndIndex": 1,
    }

    character_level = result["errorRates"][0]["characterLevel"]

    assert character_level["cer"] == 0.75
    assert character_level["hits"] == 2
    assert character_level["substitutions"] == 0
    assert character_level["insertions"] == 0
    assert character_level["deletions"] == 6
    assert len(character_level["alignments"]) == 4
    assert character_level["reference"] == ["h", "a", "i", " ", "t", "e", "s", "t"]
    assert character_level["hypothesis"] == ["h", "i"]
    assert character_level["alignments"][0] == {
        "type": "equal",
        "referenceStartIndex": 0,
        "referenceEndIndex": 1,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 1,
    }
    assert character_level["alignments"][1] == {
        "type": "delete",
        "referenceStartIndex": 1,
        "referenceEndIndex": 2,
        "hypothesisStartIndex": 1,
        "hypothesisEndIndex": 1,
    }
    assert character_level["alignments"][2] == {
        "type": "equal",
        "referenceStartIndex": 2,
        "referenceEndIndex": 3,
        "hypothesisStartIndex": 1,
        "hypothesisEndIndex": 2,
    }
    assert character_level["alignments"][3] == {
        "type": "delete",
        "referenceStartIndex": 3,
        "referenceEndIndex": 8,
        "hypothesisStartIndex": 2,
        "hypothesisEndIndex": 2,
    }

    assert db_mock.fetch_file.call_count == 1
