import pytest
from spectral.database import Database
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
    mock.__class__ = Database

    yield mock


@pytest.fixture(autouse=True)
def override_dependency(db_mock):
    app.dependency_overrides[get_db] = lambda: db_mock
    yield
    app.dependency_overrides = {}


def test_signal_correct_mode_file_not_found(db_mock, file_state):
    db_mock.fetch_file.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 404
    ), "Expected status code 404 when file is not found"
    assert (
        response.json()["detail"] == "File not found"
    ), "Expected detail message 'File not found'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_correct_simple_info(db_mock, file_state):
    file_state["frame"] = None
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert response.status_code == 200, "Expected status code 200 for simple info mode"
    result = response.json()
    assert result["fileSize"] == 146158, "Expected file size to be 146158"
    assert (
        result["fileCreationDate"] == "1970-01-01T00:00:01Z"
    ), "Expected creation date to be '1970-01-01T00:00:01Z'"
    assert result["frame"] is None, "Expected frame to be None"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_correct_spectrogram(db_mock, file_state):
    response = client.post("/signals/modes/spectrogram", json={"fileState": file_state})
    assert response.status_code == 200, "Expected status code 200 for spectrogram mode"
    assert response.json() is None, "Expected response to be None"
    assert db_mock.fetch_file.call_count == 0, "Expected fetch_file not to be called"


def test_signal_correct_waveform(db_mock, file_state):
    response = client.post("/signals/modes/waveform", json={"fileState": file_state})
    assert response.status_code == 200, "Expected status code 200 for waveform mode"
    result = response.json()
    assert result is None, "Expected response to be None"
    assert db_mock.fetch_file.call_count == 0, "Expected fetch_file not to be called"


def test_signal_correct_vowel_space(db_mock, file_state):
    response = client.post("/signals/modes/vowel-space", json={"fileState": file_state})
    assert response.status_code == 200, "Expected status code 200 for vowel-space mode"
    assert response.json() == {
        "f1": 1242.857422568559,
        "f2": 2503.8350190318893,
    }, "Expected f1 and f2 values"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_correct_transcription(db_mock, file_state):
    response = client.post(
        "/signals/modes/transcription", json={"fileState": file_state}
    )
    assert (
        response.status_code == 200
    ), "Expected status code 200 for transcription mode"
    assert response.json() is None, "Expected response to be None"


def test_signal_mode_wrong_mode(db_mock, file_state):
    response = client.post("/signals/modes/wrongmode", json={"fileState": file_state})
    assert response.status_code == 422, "Expected status code 422 for wrong mode"
    assert db_mock.fetch_file.call_count == 0, "Expected fetch_file not to be called"


def test_signal_mode_frame_start_index_missing(db_mock, file_state):
    file_state["frame"] = {"endIndex": 1}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 400
    ), "Expected status code 400 when startIndex is missing"
    assert (
        response.json()["detail"] == "no startIndex provided"
    ), "Expected detail message 'no startIndex provided'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_frame_end_index_missing(db_mock, file_state):
    file_state["frame"] = {"startIndex": 1}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 400
    ), "Expected status code 400 when endIndex is missing"
    assert (
        response.json()["detail"] == "no endIndex provided"
    ), "Expected detail message 'no endIndex provided'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_frame_start_index_bigger_than_end_index(db_mock, file_state):
    file_state["frame"] = {"startIndex": 2, "endIndex": 1}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 400
    ), "Expected status code 400 when startIndex is bigger than endIndex"
    assert (
        response.json()["detail"] == "startIndex should be strictly lower than endIndex"
    ), "Expected detail message 'startIndex should be strictly lower than endIndex'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_frame_start_index_bigger_than_end_index_equal_numbers(
    db_mock, file_state
):
    file_state["frame"] = {"startIndex": 2, "endIndex": 2}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 400
    ), "Expected status code 400 when startIndex is equal to endIndex"
    assert (
        response.json()["detail"] == "startIndex should be strictly lower than endIndex"
    ), "Expected detail message 'startIndex should be strictly lower than endIndex'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_frame_negative_start_index(db_mock, file_state):
    file_state["frame"] = {"startIndex": -1, "endIndex": 2}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 400
    ), "Expected status code 400 when startIndex is negative"
    assert (
        response.json()["detail"] == "startIndex should be larger or equal to 0"
    ), "Expected detail message 'startIndex should be larger or equal to 0'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_frame_too_large_end_index(db_mock, file_state):
    file_state["frame"] = {"startIndex": 0, "endIndex": 73041}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 400
    ), "Expected status code 400 when endIndex is too large"
    assert (
        response.json()["detail"] == "endIndex should be lower than the file length"
    ), "Expected detail message 'endIndex should be lower than the file length'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_frame_too_large_boundary(db_mock, file_state):
    file_state["frame"] = {"startIndex": 0, "endIndex": 73040}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 200
    ), "Expected status code 200 when frame boundaries are valid"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_simple_info_with_frame(db_mock, file_state):
    file_state["frame"] = {"startIndex": 22500, "endIndex": 23250}
    response = client.post("/signals/modes/simple-info", json={"fileState": file_state})
    assert (
        response.status_code == 200
    ), "Expected status code 200 for simple info mode with frame"
    result = response.json()
    assert result["fileSize"] == 146158, "Expected file size to be 146158"
    assert (
        result["fileCreationDate"] == "1970-01-01T00:00:01Z"
    ), "Expected creation date to be '1970-01-01T00:00:01Z'"
    assert result["averagePitch"] == pytest.approx(
        34.38, 0.1
    ), "Expected average pitch to be approximately 34.38"
    assert result["duration"] == pytest.approx(
        4.565, 0.01
    ), "Expected duration to be approximately 4.565"
    assert result["frame"] is not None, "Expected frame to be not None"
    assert result["frame"]["duration"] == pytest.approx(
        0.046875
    ), "Expected frame duration to be approximately 0.046875"
    assert result["frame"]["f1"] == pytest.approx(
        623.19, 0.1
    ), "Expected frame f1 to be approximately 623.19"
    assert result["frame"]["f2"] == pytest.approx(
        1635.4, 0.1
    ), "Expected frame f2 to be approximately 1635.4"
    assert result["frame"]["pitch"] == pytest.approx(
        591.6, 0.1
    ), "Expected frame pitch to be approximately 591.6"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_vowel_space_mode_with_frame(db_mock, file_state):
    file_state["frame"] = {"startIndex": 22500, "endIndex": 23250}
    response = client.post("/signals/modes/vowel-space", json={"fileState": file_state})
    assert (
        response.status_code == 200
    ), "Expected status code 200 for vowel-space mode with frame"
    result = response.json()
    assert result["f1"] == pytest.approx(
        623.19, 0.1
    ), "Expected frame f1 to be approximately 623.19"
    assert result["f2"] == pytest.approx(
        1635.4, 0.1
    ), "Expected frame f2 to be approximately 1635.4"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_signal_mode_transcription_db_problem(db_mock):
    db_mock.fetch_file.side_effect = HTTPException(
        status_code=500, detail="database error"
    )
    response = client.get("/transcription/deepgram/1")
    assert (
        response.status_code == 404
    ), "Expected status code 404 when there is a database error"
    assert (
        response.json()["detail"] == "File not found"
    ), "Expected detail message 'File not found'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_transcription_model_found(db_mock):
    with patch(
        "spectral.transcription.transcription.deepgram_transcription"
    ) as mock_deepgram_transcription:
        mock_deepgram_transcription.return_value = [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ]
        response = client.get("/transcription/deepgram/1")
        assert (
            response.status_code == 200
        ), "Expected status code 200 for deepgram transcription"
        result = response.json()
        assert result == [
            {"value": "", "start": 0, "end": 0.5},
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "", "start": 1.0, "end": 1.5},
            {"value": "word2", "start": 1.5, "end": 2.0},
            {"end": 4.565, "start": 2.0, "value": ""},
        ], "Expected transcription result to match the mock return value"
        assert (
            db_mock.fetch_file.call_count == 1
        ), "Expected fetch_file to be called once"


def test_transcription_model_not_found(db_mock):
    response = client.get("/transcription/non_existant_model/1")
    assert (
        response.status_code == 404
    ), "Expected status code 404 when model is not found"
    assert (
        response.json()["detail"] == "Model was not found"
    ), "Expected detail message 'Model was not found'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_analyze_signal_mode_invalid_id(db_mock, file_state):
    file_state["id"] = "invalid_id"
    db_mock.fetch_file.side_effect = Exception("Database error")
    response = client.post("/signals/modes/vowel-space", json={"fileState": file_state})
    assert (
        response.status_code == 404
    ), "Expected status code 404 when file ID is invalid"
    assert (
        response.json()["detail"] == "File not found"
    ), "Expected detail message 'File not found'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


def test_transcribe_file_invalid_model(db_mock):
    response = client.get("/transcription/invalid_model/1")
    assert (
        response.status_code == 404
    ), "Expected status code 404 when transcription model is invalid"
    assert (
        response.json()["detail"] == "Model was not found"
    ), "Expected detail message 'Model was not found'"
    assert db_mock.fetch_file.call_count == 1, "Expected fetch_file to be called once"


@pytest.mark.skip(reason="Not implemented")
def test_transcribe_file_no_api_key(db_mock):
    with patch("spectral.transcription.models.deepgram.os.getenv") as mock_getenv:
        mock_getenv.return_value = None
        response = client.get("/transcription/deepgram/1")
        assert (
            response.status_code == 500
        ), "Expected status code 500 when API key is missing"
        assert (
            db_mock.fetch_file.call_count == 1
        ), "Expected fetch_file to be called once"


@pytest.fixture
def mock_db(mocker):
    mock_db_class = mocker.patch("spectral.database.Database")
    mock_db_instance = mock_db_class.return_value
    mock_db_instance.connection = Mock()
    mock_db_instance.close = Mock()
    return mock_db_instance


def test_error_rate_no_reference(db_mock, file_state):
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert (
        response.status_code == 200
    ), "Expected status code 200 when ground truth is missing"
    assert response.json() is None, "Expected response to be None"
    assert db_mock.fetch_file.call_count == 0, "Expected fetch_file to be called never"


def test_error_rate_reference_None(file_state):
    file_state["reference"] = None
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert (
        response.status_code == 200
    ), "Expected status code 200 when ground truth is missing"
    assert response.json() is None, "Expected response to be None"


def test_error_rate_no_reference_caption(db_mock, file_state):
    file_state["reference"] = {}
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_no_hypothesis(db_mock, file_state):
    file_state["reference"] = {"captions": [{"value": "Hi"}]}
    file_state["hypothesis"] = None
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_hypothesis_None(db_mock, file_state):
    file_state["reference"] = {"captions": [{"value": "Hi"}]}
    file_state["hypothesis"] = None
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_no_hypothesis_caption(db_mock, file_state):
    file_state["reference"] = {"captions": [{"value": "Hi"}]}
    file_state["hypothesis"] = {}
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_empty_reference_array(db_mock, file_state):
    file_state["reference"] = {"captions": []}
    file_state["hypothesis"] = {"captions": [{"value": "Hi"}]}
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_empty_hypothesis_array(db_mock, file_state):
    file_state["reference"] = {"captions": [{"value": "Hi"}]}
    file_state["hypothesis"] = {"captions": []}
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})

    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "wordLevel": {
            "wer": 1.0,
            "mer": 1.0,
            "wil": 1.0,
            "wip": 0.0,
            "hits": 0,
            "substitutions": 0,
            "insertions": 0,
            "deletions": 1,
            "reference": ["Hi"],
            "hypothesis": [],
            "alignments": [
                {
                    "type": "delete",
                    "referenceStartIndex": 0,
                    "referenceEndIndex": 1,
                    "hypothesisStartIndex": 0,
                    "hypothesisEndIndex": 0,
                }
            ],
        },
        "characterLevel": {
            "cer": 1.0,
            "hits": 0,
            "substitutions": 0,
            "insertions": 0,
            "deletions": 2,
            "reference": ["H", "i"],
            "hypothesis": [],
            "alignments": [
                {
                    "type": "delete",
                    "referenceStartIndex": 0,
                    "referenceEndIndex": 2,
                    "hypothesisStartIndex": 0,
                    "hypothesisEndIndex": 0,
                }
            ],
        },
    }, "the response was not the same"
    assert db_mock.get_transcriptions.call_count == 0


def test_error_rate_with_reference_no_hypothesis(db_mock, file_state):
    file_state["reference"] = {}
    file_state["reference"]["captions"] = [{"value": "hai test"}]
    file_state["hypothesis"] = {}
    file_state["hypothesis"]["captions"] = []
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})
    assert (
        response.status_code == 200
    ), "Expected status code 200 when ground truth is provided"
    result = response.json()
    word_level = result["wordLevel"]
    assert word_level["wer"] == 1.0, "Expected word error rate (WER) to be 1.0"
    assert word_level["mer"] == 1.0, "Expected match error rate (MER) to be 1.0"
    assert word_level["wil"] == 1.0, "Expected word information lost (WIL) to be 1.0"
    assert word_level["wip"] == 0, "Expected word information preserved (WIP) to be 0"
    assert word_level["hits"] == 0, "Expected hits to be 0"
    assert word_level["substitutions"] == 0, "Expected substitutions to be 0"
    assert word_level["insertions"] == 0, "Expected insertions to be 0"
    assert word_level["deletions"] == 2, "Expected deletions to be 2"
    assert word_level["reference"] == [
        "hai",
        "test",
    ], "Expected reference to be ['hai', 'test']"
    assert word_level["hypothesis"] == [], "Expected hypothesis to be empty"
    assert len(word_level["alignments"]) == 1, "Expected one alignment"
    assert word_level["alignments"][0] == {
        "type": "delete",
        "referenceStartIndex": 0,
        "referenceEndIndex": 2,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 0,
    }, "Expected delete alignment"

    character_level = result["characterLevel"]

    assert character_level["cer"] == 1, "Expected character error rate (CER) to be 1"
    assert character_level["hits"] == 0, "Expected hits to be 0"
    assert character_level["substitutions"] == 0, "Expected substitutions to be 0"
    assert character_level["insertions"] == 0, "Expected insertions to be 0"
    assert character_level["deletions"] == 8, "Expected deletions to be 8"
    assert character_level["reference"] == [
        "h",
        "a",
        "i",
        " ",
        "t",
        "e",
        "s",
        "t",
    ], "Expected reference to be ['h', 'a', 'i', ' ', 't', 'e', 's', 't']"
    assert character_level["hypothesis"] == [], "Expected hypothesis to be empty"
    assert len(character_level["alignments"]) == 1, "Expected one alignment"
    assert character_level["alignments"][0] == {
        "type": "delete",
        "referenceStartIndex": 0,
        "referenceEndIndex": 8,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 0,
    }, "Expected delete alignment"

    assert db_mock.fetch_file.call_count == 0, "Expected fetch_file to be called once"


def test_error_rate_with_reference_and_hypothesis(db_mock, file_state):
    file_state["reference"] = {}
    file_state["reference"]["captions"] = [{"value": "hai test"}]
    file_state["hypothesis"] = {}
    file_state["hypothesis"]["captions"] = [{"value": "hi"}]
    response = client.post("/signals/modes/error-rate", json={"fileState": file_state})
    result = response.json()
    word_level = result["wordLevel"]
    assert word_level["wer"] == 1.0, "Expected word error rate (WER) to be 1.0"
    assert word_level["mer"] == 1.0, "Expected match error rate (MER) to be 1.0"
    assert word_level["wil"] == 1.0, "Expected word information lost (WIL) to be 1.0"
    assert word_level["wip"] == 0, "Expected word information preserved (WIP) to be 0"
    assert word_level["hits"] == 0, "Expected hits to be 0"
    assert word_level["substitutions"] == 1, "Expected substitutions to be 1"
    assert word_level["insertions"] == 0, "Expected insertions to be 0"
    assert word_level["deletions"] == 1, "Expected deletions to be 1"
    assert word_level["reference"] == [
        "hai",
        "test",
    ], "Expected reference to be ['hai', 'test']"
    assert word_level["hypothesis"] == ["hi"], "Expected hypothesis to be ['hi']"
    assert len(word_level["alignments"]) == 2, "Expected two alignments"
    assert word_level["alignments"][0] == {
        "type": "substitute",
        "referenceStartIndex": 0,
        "referenceEndIndex": 1,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 1,
    }, "Expected substitute alignment"
    assert word_level["alignments"][1] == {
        "type": "delete",
        "referenceStartIndex": 1,
        "referenceEndIndex": 2,
        "hypothesisStartIndex": 1,
        "hypothesisEndIndex": 1,
    }, "Expected delete alignment"

    character_level = result["characterLevel"]

    assert (
        character_level["cer"] == 0.75
    ), "Expected character error rate (CER) to be 0.75"
    assert character_level["hits"] == 2, "Expected hits to be 2"
    assert character_level["substitutions"] == 0, "Expected substitutions to be 0"
    assert character_level["insertions"] == 0, "Expected insertions to be 0"
    assert character_level["deletions"] == 6, "Expected deletions to be 6"
    assert len(character_level["alignments"]) == 4, "Expected four alignments"
    assert character_level["reference"] == [
        "h",
        "a",
        "i",
        " ",
        "t",
        "e",
        "s",
        "t",
    ], "Expected reference to be ['h', 'a', 'i', ' ', 't', 'e', 's', 't']"
    assert character_level["hypothesis"] == [
        "h",
        "i",
    ], "Expected hypothesis to be ['h', 'i']"
    assert character_level["alignments"][0] == {
        "type": "equal",
        "referenceStartIndex": 0,
        "referenceEndIndex": 1,
        "hypothesisStartIndex": 0,
        "hypothesisEndIndex": 1,
    }, "Expected equal alignment"
    assert character_level["alignments"][1] == {
        "type": "delete",
        "referenceStartIndex": 1,
        "referenceEndIndex": 2,
        "hypothesisStartIndex": 1,
        "hypothesisEndIndex": 1,
    }, "Expected delete alignment"
    assert character_level["alignments"][2] == {
        "type": "equal",
        "referenceStartIndex": 2,
        "referenceEndIndex": 3,
        "hypothesisStartIndex": 1,
        "hypothesisEndIndex": 2,
    }, "Expected equal alignment"
    assert character_level["alignments"][3] == {
        "type": "delete",
        "referenceStartIndex": 3,
        "referenceEndIndex": 8,
        "hypothesisStartIndex": 2,
        "hypothesisEndIndex": 2,
    }, "Expected delete alignment"

    assert db_mock.fetch_file.call_count == 0, "Expected fetch_file to be called never"


def test_phone_transcription(db_mock, file_state):
    with patch(
        "spectral.transcription.models.allosaurus.deepgram_transcription"
    ) as mock_deepgram_transcription:
        mock_deepgram_transcription.return_value = [
            {"value": "", "start": 0.0, "end": 1.04},
            {"value": "the", "start": 1.04, "end": 1.36},
            {"value": "quick", "start": 1.36, "end": 1.68},
            {"value": "brown", "start": 1.68, "end": 2.0},
            {"value": "fox", "start": 2.0, "end": 2.3999999},
            {"value": "jumps", "start": 2.3999999, "end": 2.72},
            {"value": "over", "start": 2.72, "end": 3.04},
            {"value": "the", "start": 3.04, "end": 3.1999998},
            {"value": "lazy", "start": 3.1999998, "end": 3.52},
            {"value": "dog", "start": 3.52, "end": 4.02},
            {"value": "", "start": 4.02, "end": 4.565},
        ]
        response = client.get("/transcription/allosaurus/1")
        assert (
            response.status_code == 200
        ), "Expected status code 200 for allosaurus transcription"
        result = response.json()
        assert result == [
            {"value": "", "start": 0, "end": 1.04},
            {"value": "ð", "start": 1.04, "end": 1.275},
            {"value": "ə", "start": 1.275, "end": 1.36},
            {"value": "k", "start": 1.36, "end": 1.44},
            {"value": "uə", "start": 1.44, "end": 1.5},
            {"value": "ɪ", "start": 1.5, "end": 1.56},
            {"value": "tʰ", "start": 1.56, "end": 1.68},
            {"value": "b̥", "start": 1.68, "end": 1.77},
            {"value": "a", "start": 1.77, "end": 1.845},
            {"value": "l̪", "start": 1.845, "end": 2.0},
            {"value": "f", "start": 2.0, "end": 2.085},
            {"value": "ɑ", "start": 2.085, "end": 2.19},
            {"value": "k", "start": 2.19, "end": 2.31},
            {"value": "s", "start": 2.31, "end": 2.3999999},
            {"value": "d͡ʒ", "start": 2.3999999, "end": 2.505},
            {"value": "ʌ", "start": 2.505, "end": 2.565},
            {"value": "m", "start": 2.565, "end": 2.6100000000000003},
            {"value": "p", "start": 2.6100000000000003, "end": 2.67},
            {"value": "ʂ", "start": 2.67, "end": 2.72},
            {"value": "ə", "start": 2.72, "end": 2.76},
            {"value": "o", "start": 2.76, "end": 2.8049999999999997},
            {"value": "w", "start": 2.8049999999999997, "end": 2.8499999999999996},
            {"value": "v", "start": 2.8499999999999996, "end": 2.895},
            {"value": "ɾ", "start": 2.895, "end": 2.9400000000000004},
            {"value": "u", "start": 2.9400000000000004, "end": 3.04},
            {"value": "ð", "start": 3.04, "end": 3.075},
            {"value": "ə", "start": 3.075, "end": 3.135},
            {"value": "l", "start": 3.135, "end": 3.1999998},
            {"value": "i", "start": 3.1999998, "end": 3.3},
            {"value": "z", "start": 3.3, "end": 3.3899999999999997},
            {"value": "i", "start": 3.3899999999999997, "end": 3.52},
            {"value": "d", "start": 3.52, "end": 3.5700000000000003},
            {"value": "ʌ", "start": 3.5700000000000003, "end": 3.675},
            {"value": "g", "start": 3.675, "end": 4.02},
            {"value": "", "start": 4.02, "end": 4.565},
        ], "Expected phonetic transcription result to match the mock return value"
        assert (
            db_mock.fetch_file.call_count == 1
        ), "Expected fetch_file to be called once"


def test_phone_transcription_no_words(db_mock, file_state):
    with patch(
        "spectral.transcription.models.deepgram.deepgram_transcription"
    ) as mock_deepgram_transcription:
        mock_deepgram_transcription.return_value = []
        response = client.get("/transcription/allosaurus/1")
        assert (
            response.status_code == 200
        ), "Expected status code 200 for allosaurus transcription with no words"
        result = response.json()
        assert (
            result
            == [
                {"value": "ð", "start": 0, "end": 1.275},
                {"value": "ə", "start": 1.275, "end": 1.35},
                {"value": "k", "start": 1.35, "end": 1.44},
                {"value": "uə", "start": 1.44, "end": 1.5},
                {"value": "ɪ", "start": 1.5, "end": 1.56},
                {"value": "tʰ", "start": 1.56, "end": 1.665},
                {"value": "b̥", "start": 1.665, "end": 1.77},
                {"value": "a", "start": 1.77, "end": 1.845},
                {"value": "l̪", "start": 1.845, "end": 1.9649999999999999},
                {"value": "f", "start": 1.9649999999999999, "end": 2.085},
                {"value": "ɑ", "start": 2.085, "end": 2.19},
                {"value": "k", "start": 2.19, "end": 2.31},
                {"value": "s", "start": 2.31, "end": 2.415},
                {"value": "d͡ʒ", "start": 2.415, "end": 2.505},
                {"value": "ʌ", "start": 2.505, "end": 2.565},
                {"value": "m", "start": 2.565, "end": 2.6100000000000003},
                {"value": "p", "start": 2.6100000000000003, "end": 2.67},
                {"value": "ʂ", "start": 2.67, "end": 2.715},
                {"value": "ə", "start": 2.715, "end": 2.76},
                {"value": "o", "start": 2.76, "end": 2.8049999999999997},
                {"value": "w", "start": 2.8049999999999997, "end": 2.8499999999999996},
                {"value": "v", "start": 2.8499999999999996, "end": 2.895},
                {"value": "ɾ", "start": 2.895, "end": 2.9400000000000004},
                {"value": "u", "start": 2.9400000000000004, "end": 3.015},
                {"value": "ð", "start": 3.015, "end": 3.075},
                {"value": "ə", "start": 3.075, "end": 3.135},
                {"value": "l", "start": 3.135, "end": 3.21},
                {"value": "i", "start": 3.21, "end": 3.3},
                {"value": "z", "start": 3.3, "end": 3.3899999999999997},
                {"value": "i", "start": 3.3899999999999997, "end": 3.48},
                {"value": "d", "start": 3.48, "end": 3.5700000000000003},
                {"value": "ʌ", "start": 3.5700000000000003, "end": 3.675},
                {"value": "g", "start": 3.675, "end": 4.565},
            ]
        ), "Expected phonetic transcription result to match the mock return value when no words are provided"
        assert (
            db_mock.fetch_file.call_count == 1
        ), "Expected fetch_file to be called once"
