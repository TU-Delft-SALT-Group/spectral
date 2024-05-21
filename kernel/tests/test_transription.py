import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from spectral.transcription import get_transcription, deepgram_transcription
import os


def test_get_transcription_model_not_found():
    with pytest.raises(HTTPException) as excinfo:
        get_transcription("non_existent_model", {"data": b"audio data"})
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Model was not found"


@patch("spectral.transcription.deepgram_transcription")
def test_get_transcription_deepgram(mock_deepgram_transcription):
    mock_deepgram_transcription.return_value = [
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "word2", "start": 1.5, "end": 2.0},
    ]
    result = get_transcription("deepgram", {"data": b"audio data"})
    assert result == [
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "word2", "start": 1.5, "end": 2.0},
    ]
    mock_deepgram_transcription.assert_called_once_with(b"audio data")


@patch.dict(os.environ, {"DG_KEY": "test_key"}, clear=True)
@patch("spectral.transcription.DeepgramClient")
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
    assert result == [
        {"value": "word1", "start": 0.5, "end": 1.0},
        {"value": "word2", "start": 1.5, "end": 2.0},
    ]
    mock_deepgram_client.assert_called_once_with("test_key")
    mock_client_instance.listen.prerecorded.v("1").transcribe_file.assert_called_once()


@patch.dict(os.environ, {}, clear=True)
def test_deepgram_transcription_no_api_key(capfd):
    deepgram_transcription(b"audio data")
    captured = capfd.readouterr()
    assert "No API key for Deepgram is found" in captured.out
