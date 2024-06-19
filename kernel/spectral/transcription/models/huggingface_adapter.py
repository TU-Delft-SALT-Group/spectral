"""Interface to load arbitrary* HF models."""

from collections.abc import Callable
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from spectral import signal_analysis
from spectral.types import TranscriptionType


@lru_cache
def _get_model_by_name(model_name: str) -> tuple:
    if model_name != "torgo":
        raise RuntimeError("""We don't support any other model besides
                           'torgo' one for now: some models on huggingface
                           require manual patching, and this model in particular
                           is the jindaznb/torgo_tiny_finetune_F01_frozen_encoder
                           patched with tiny whisper tokenizer...""")

    path = Path(__file__).parent / Path(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(path, local_files_only=True)
    processor = WhisperProcessor.from_pretrained(path, local_files_only=True)
    return (model, processor)


@lru_cache
def get_transcribe_fn(model_name: str) -> Callable[[bytes], str]:
    """Return a complete prediction function, that adheres to the usual API."""
    model, processor = _get_model_by_name(model_name)
    required_sr = 16000

    def transcribe_fn(data: bytes) -> str:
        audio = signal_analysis.get_audio({"data": data})
        # trick from https://github.com/openai/whisper/discussions/983
        data = np.frombuffer(audio.raw_data, np.int16).flatten().astype(np.float32) / 32768.0  # type: ignore
        input_features = processor(
            data, sampling_rate=required_sr, return_tensors="pt"
        ).input_features  # type: ignore

        # Generate transcription
        with torch.no_grad():
            predicted_ids = model.generate(input_features)  # type: ignore
            return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]  # type: ignore

    return transcribe_fn


def hf_transcription(data: bytes, model_name: str) -> TranscriptionType:
    """
    Get transcription from hf given wav bytes representation.

    Args:
    ----
        data (bytes): list of data bytes representing a WAV audio signal

    Returns:
    -------
        list[dict]: list of dictionaries containing start, end and value

    """
    try:
        transcription = get_transcribe_fn(model_name)(data)
        duration = signal_analysis.calculate_signal_duration(
            signal_analysis.get_audio({"data": data})
        )
    except RuntimeError:
        return {}
    else:
        return {
            "language": "??",
            "transcription": [{"value": transcription, "start": 0, "end": duration}],
        }
