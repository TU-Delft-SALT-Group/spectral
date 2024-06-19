"""Interface to load arbitrary* HF models."""

from functools import lru_cache

import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from spectral import signal_analysis
from spectral.types import TranscriptionType


@lru_cache
def _get_model_by_name(model_name):
    if model_name != "torgo":
        raise RuntimeError("""We don't support any other model besides
                           'torgo' one for now: some models on huggingface
                           require manual patching, and this model in particular
                           is the jindaznb/torgo_tiny_finetune_F01_frozen_encoder
                           patched with tiny whisper tokenizer...""")

    model = WhisperForConditionalGeneration.from_pretrained(model_name, local_files_only=True)
    processor = WhisperProcessor.from_pretrained(model_name, local_files_only=True)
    return (model, processor)


@lru_cache
def get_transcribe_fn(model_name):
    """Return a complete prediction function, that adheres to the usual API."""
    model, processor = _get_model_by_name(model_name)
    required_sr = 16000

    def transcribe_fn(data):
        input_features = processor(
            data, sampling_rate=required_sr, return_tensors="pt"
        ).input_features

        # Generate transcription
        with torch.no_grad():
            predicted_ids = model.generate(input_features)  # type: ignore
            return processor.batch_decode(predicted_ids, skip_special_tokens=False)

    return transcribe_fn


def hf_transcription(data: bytes, model_name: str) -> TranscriptionType:
    """
    Get transcription from whisper from an list of WAV bytes.

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
