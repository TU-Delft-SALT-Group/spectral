import pytest
import torch
from unittest.mock import Mock, patch
from fastapi import HTTPException
from spectral.transcription.models.huggingface_adapter import hf_transcription
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
    assert excinfo.value.status_code == 404, f"Expected status code 404 but got {excinfo.value.status_code}"
    assert (
        excinfo.value.detail == "Model was not found"
    ), f"Expected detail 'Model was not found' but got {excinfo.value.detail}"


@patch("spectral.transcription.transcription.deepgram_transcription")
@patch("spectral.transcription.transcription_utils.get_audio")
@patch("spectral.transcription.transcription_utils.calculate_signal_duration")
def test_get_transcription_deepgram(mock_calculate_signal_duration, mock_get_audio, mock_deepgram_transcription):
    mock_deepgram_transcription.return_value = {
        "language": "en",
        "transcription": [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ],
    }
    mock_get_audio.return_value = Mock()
    mock_calculate_signal_duration.return_value = 4.565
    result = get_transcription("deepgram", {"data": b"audio data"}, api_key="abc")

    expected_result = {
        "language": "en",
        "transcription": [
            {"value": "", "start": 0, "end": 0.5},
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "", "start": 1.0, "end": 1.5},
            {"value": "word2", "start": 1.5, "end": 2.0},
            {"value": "", "start": 2.0, "end": 4.565},
        ],
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"


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
                    ],
                    "detected_language": "en",
                }
            ]
        }
    }
    mock_client_instance.listen.prerecorded.v("1").transcribe_file.return_value = mock_response

    data = b"audio data"
    result = deepgram_transcription(data, "test_key")

    expected_result = {
        "language": "en",
        "transcription": [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ],
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    (mock_deepgram_client.assert_called_once_with("test_key"))
    (mock_client_instance.listen.prerecorded.v("1").transcribe_file.assert_called_once())


def test_deepgram_transcription_no_api_key():
    try:
        deepgram_transcription(b"audio data")
        assert "Should respond with 401 code"
    except HTTPException as e:
        assert e.status_code == 401


def test_get_phoneme_transcription_empty_transcription():
    result = get_phoneme_transcriptions("test-lang", [{}])
    expected_result = {"language": "test-lang", "transcription": []}

    assert result == expected_result, f"Expected an empty list, but got {result}"


def test_get_phoneme_word_splits_empty():
    result = get_phoneme_word_splits([], [[]])
    expected_result = []

    assert result == expected_result, f"Expected an empty list, but got {result}"


@patch("spectral.transcription.models.whisper.get_whisper_transcription")
@patch("spectral.transcription.transcription_utils.get_audio")
@patch("spectral.transcription.transcription_utils.calculate_signal_duration")
def test_get_transcription_whisper(mock_calculate_signal_duration, mock_get_audio, mock_whisper_transcription):
    mock = Mock()
    mock.words = [
        {"word": "word1", "start": 0.5, "end": 1.0},
        {"word": "word2", "start": 1.5, "end": 2.0},
    ]
    mock.language = "english"
    mock_whisper_transcription.return_value = mock

    mock_get_audio.return_value = Mock()
    mock_calculate_signal_duration.return_value = 4.565
    result = get_transcription("whisper", {"data": b"audio data"})

    expected_result = {
        "language": "english",
        "transcription": [
            {"value": "", "start": 0, "end": 0.5},
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "", "start": 1.0, "end": 1.5},
            {"value": "word2", "start": 1.5, "end": 2.0},
            {"value": "", "start": 2.0, "end": 4.565},
        ],
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"


@pytest.mark.skip("TODO: fix message")
@patch.dict(os.environ, {}, clear=True)
def test_whisper_transcription_no_api_key(capfd):
    whisper_transcription(b"audio data")
    captured = capfd.readouterr()

    expected_message = "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable\n"  # noqa
    assert expected_message in captured.out, f"Expected output '{expected_message}' but got {captured.out}"


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
    mock_response.language = "english"
    mock_client_instance.audio.transcriptions.create.return_value = mock_response

    data = b"0"
    result = whisper_transcription(data, api_key="test_key")

    expected_result = {
        "language": "english",
        "transcription": [
            {"value": "word1", "start": 0.5, "end": 1.0},
            {"value": "word2", "start": 1.5, "end": 2.0},
        ],
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    (mock_whisper_client.assert_called_once_with(api_key="test_key"))
    (mock_client_instance.audio.transcriptions.create.assert_called_once())


def test_hf_transcription_no_model():
    with pytest.raises(HTTPException) as httpException:
        hf_transcription(b"audio data", "arst")
    assert httpException.value.status_code == 401
    assert httpException.value.detail == "Something went wrong when transcribing using custom HF model, sorry."


@patch("spectral.signal_analysis.get_audio")
@patch("spectral.signal_analysis.calculate_signal_duration")
@patch("spectral.transcription.models.huggingface_adapter._get_model_by_name")
def test_hf_transcription_basic(mock_model_getter, sig_duration, get_audio):
    fake_audio = Mock()
    get_audio.return_value = fake_audio
    fake_audio.raw_data = b""
    sig_duration.return_value = 1.5
    mock_model = Mock()
    mock_processor = Mock()
    mock_model_getter.return_value = (mock_model, mock_processor)
    mock_model.generate.return_value = torch.tensor([1, 2, 3])
    mock_input = Mock()
    mock_processor.return_value = mock_input
    mock_input.return_value = None

    def fake_decode(input, *args, **kws):
        assert torch.allclose(input, torch.tensor([1, 2, 3]))
        return "i love apples"

    mock_processor.batch_decode = fake_decode

    assert hf_transcription(b"data", "torgo") == {
        "language": "unk",
        "transcription": [{"end": 1.5, "start": 0, "value": "i"}],
    }
