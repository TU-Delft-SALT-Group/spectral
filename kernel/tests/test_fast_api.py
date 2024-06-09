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
    assert result["fileSize"] == 146158
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
    assert result["fileSize"] == 146158
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
            {"value": "", "start": 0, "end": 0.5},
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "", "start": 1.0, "end": 1.5},
            {"value": "word2", "start": 1.5, "end": 2.0},
            {"end": 4.565, "start": 2.0, "value": ""},
        ]
        assert db_mock.fetch_file.call_count == 1


def test_transcription_model_not_found(db_mock):
    response = client.get("/transcription/non_existant_model/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model was not found"
    assert db_mock.fetch_file.call_count == 1


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


@pytest.mark.skip(reason="Protocol is being changed")
def test_error_rate_no_ground_truth(db_mock, file_state):
    db_mock.fetch_file.return_value["groundTruth"] = None
    response = client.get(
        "/signals/modes/error-rate", params={"fileState": json.dumps(file_state)}
    )

    assert response.status_code == 200
    assert response.json() is None
    assert db_mock.fetch_file.call_count == 1
    assert db_mock.get_transcriptions.call_count == 0


@pytest.mark.skip(reason="Protocol is being changed")
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
    file_state["reference"] = [{"value": "hai test"}]
    file_state["hypothesis"] = [{"value": "hi"}]
    response = client.get(
        "/signals/modes/error-rate", params={"fileState": json.dumps(file_state)}
    )

    assert response.status_code == 200
    result = response.json()

    word_level = result["errorRate"]["wordLevel"]

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

    character_level = result["errorRate"]["characterLevel"]

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


def test_phone_transcription(db_mock, file_state):
    with patch(
        "spectral.transcription.deepgram_transcription"
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
        assert response.status_code == 200
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
        ]
        assert db_mock.fetch_file.call_count == 1


def test_phone_transcription_no_words(db_mock, file_state):
    with patch(
        "spectral.transcription.deepgram_transcription"
    ) as mock_deepgram_transcription:
        mock_deepgram_transcription.return_value = []
        response = client.get("/transcription/allosaurus/1")
        assert response.status_code == 200
        result = response.json()
        assert result == [
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
        assert db_mock.fetch_file.call_count == 1
