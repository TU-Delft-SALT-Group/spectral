"""
Interface to load arbitrary* HF models.

Some notes:

Most of the models from HF we tried require patching by hand to be run. Don't
be the person who is not capable of checking the correctness of export of their model!
If the model is exported very well, you can use just a single line (with transformers.pipeline)
to run it, which is very convenient. But, the current model we use requires patching of its
tokenizer by hand, which is *very* annoying. And this is the reason for such an awkward loading
of the model, where we don't load it from the huggingface, but load it from the local folder.

Creating such a folder is actually not thaaat hard:
clone the whisper tiny:  git clone https://huggingface.co/openai/whisper-tiny
clone the torgo-whatever model: git clone https://huggingface.co/jindaznb/torgo_tiny_finetune_F01_frozen_encoder

Make sure you run ```git lfs pull``` in each repo, this will pull the actual weights. You might need
to install the git-lfs as a system package, with something like ```apt install git-lfs```.

Afterwards, you need to copy these files from the "whisper" folder into the "torgo-whatever" folder:
* merges.txt
* vocab.json
* tokenizer.json
* tokenizer_config.json

And then rename the folder torgo-whatever into just torgo.
Now the support for the torgo transcription mode should be present.
"""

from collections.abc import Callable
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from spectral import signal_analysis
from spectral.types import TranscriptionType

from fastapi import HTTPException


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
    required_sr = 16000  # magic number, requirement of the model

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
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Something went wrong when transcribing using custom HF model, sorry.",
        ) from e
    else:
        return {
            "language": "unk",
            "transcription": [{"value": transcription, "start": 0, "end": duration}],
        }
