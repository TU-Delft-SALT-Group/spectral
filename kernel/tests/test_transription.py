import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from spectral.transcription.transcription import (
    get_transcription,
    deepgram_transcription,
)
from spectral.transcription.models.allosaurus import (
    get_phoneme_transcriptions,
    get_phoneme_word_splits,
)
from spectral.transcription.models.whisper import whisper_transcription
import os


def test_get_transcription_model_not_found():
    with pytest.raises(HTTPException) as excinfo:
        get_transcription("non_existent_model", {"data": b"audio data"})
    assert (
        excinfo.value.status_code == 404
    ), f"Expected status code 404 but got {excinfo.value.status_code}"
    assert (
        excinfo.value.detail == "Model was not found"
    ), f"Expected detail 'Model was not found' but got {excinfo.value.detail}"


@patch("spectral.transcription.transcription.deepgram_transcription")
@patch("spectral.transcription.transcription_utils.get_audio")
@patch("spectral.transcription.transcription_utils.calculate_signal_duration")
def test_get_transcription_deepgram(
    mock_calculate_signal_duration, mock_get_audio, mock_deepgram_transcription
):
    mock_deepgram_transcription.return_value = [
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "word2", "start": 1.5, "end": 2.0},
    ]
    mock_get_audio.return_value = Mock()
    mock_calculate_signal_duration.return_value = 4.565
    result = get_transcription("deepgram", {"data": b"audio data"})

    expected_result = [
        {"value": "", "start": 0, "end": 0.5},
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "", "start": 1.0, "end": 1.5},
        {"value": "word2", "start": 1.5, "end": 2.0},
        {"value": "", "start": 2.0, "end": 4.565},
    ]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    (mock_deepgram_transcription.assert_called_once_with(b"audio data"))


@patch.dict(os.environ, {"DG_KEY": "test_key"}, clear=True)
@patch("spectral.transcription.models.deepgram.DeepgramClient")
def test_deepgram_transcription(mock_deepgram_client):
    mock_client_instance = Mock()
    mock_deepgram_client.return_value = mock_client_instance
    mock_response = {
        "results": {
            "channels": [
                {
                    "alternatives": [
                        {
                            "words": [
                                {"word": "word1", "start": 0.5, "end": 1.0},
                                {"word": "word2", "start": 1.5, "end": 2.0},
                            ]
                        }
                    ]
                }
            ]
        }
    }
    mock_client_instance.listen.prerecorded.v(
        "1"
    ).transcribe_file.return_value = mock_response

    data = b"audio data"
    result = deepgram_transcription(data)

    expected_result = [
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "word2", "start": 1.5, "end": 2.0},
    ]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    (mock_deepgram_client.assert_called_once_with("test_key"))
    (
        mock_client_instance.listen.prerecorded.v(
            "1"
        ).transcribe_file.assert_called_once()
    )


@patch.dict(os.environ, {}, clear=True)
def test_deepgram_transcription_no_api_key(capfd):
    deepgram_transcription(b"audio data")
    captured = capfd.readouterr()

    expected_message = "No API key for Deepgram is found"
    assert (
        expected_message in captured.out
    ), f"Expected output '{expected_message}' but got {captured.out}"


def test_get_phoneme_transcription_empty_transcription():
    result = get_phoneme_transcriptions([{}])
    expected_result = []

    assert result == expected_result, f"Expected an empty list, but got {result}"


def test_get_phoneme_word_splits_empty():
    result = get_phoneme_word_splits([], [[]])
    expected_result = []

    assert result == expected_result, f"Expected an empty list, but got {result}"


@patch("spectral.transcription.models.whisper.get_whisper_transcription")
@patch("spectral.transcription.transcription_utils.get_audio")
@patch("spectral.transcription.transcription_utils.calculate_signal_duration")
def test_get_transcription_whisper(
    mock_calculate_signal_duration, mock_get_audio, mock_whisper_transcription
):
    mock = Mock()
    mock.words = [
        {"word": "word1", "start": 0.5, "end": 1.0},
        {"word": "word2", "start": 1.5, "end": 2.0},
    ]
    mock_whisper_transcription.return_value = mock

    mock_get_audio.return_value = Mock()
    mock_calculate_signal_duration.return_value = 4.565
    result = get_transcription("whisper", {"data": b"audio data"})

    expected_result = [
        {"value": "", "start": 0, "end": 0.5},
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "", "start": 1.0, "end": 1.5},
        {"value": "word2", "start": 1.5, "end": 2.0},
        {"value": "", "start": 2.0, "end": 4.565},
    ]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    (mock_whisper_transcription.assert_called_once_with(b"audio data"))


@patch.dict(os.environ, {}, clear=True)
def test_whisper_transcription_no_api_key(capfd):
    whisper_transcription(b"audio data")
    captured = capfd.readouterr()

    expected_message = "Exception: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable\n"
    assert (
        expected_message in captured.out
    ), f"Expected output '{expected_message}' but got {captured.out}"


@patch.dict(os.environ, {"WHISPER_KEY": "test_key"}, clear=True)
@patch("spectral.transcription.models.whisper.OpenAI")
def test_whisper_transcription(mock_whisper_client):
    mock_client_instance = Mock()
    mock_whisper_client.return_value = mock_client_instance
    mock_response = Mock()
    mock_response.words = [
        {"word": "word1", "start": 0.5, "end": 1.0},
        {"word": "word2", "start": 1.5, "end": 2.0},
    ]
    mock_client_instance.audio.transcriptions.create.return_value = mock_response

    data = b"0"
    result = whisper_transcription(data)

    expected_result = [
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "word2", "start": 1.5, "end": 2.0},
    ]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    (mock_whisper_client.assert_called_once_with(api_key="test_key"))
    (mock_client_instance.audio.transcriptions.create.assert_called_once())
