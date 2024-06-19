"""Orchestrates different trancribing methods."""

from fastapi import HTTPException

from spectral.types import FileStateType, TranscriptionType

from .models.allosaurus import allosaurus_transcription
from .models.deepgram import deepgram_transcription
from .models.huggingface_adapter import hf_transcription
from .models.whisper import whisper_transcription
from .transcription_utils import fill_gaps


def get_transcription(model: str, file: FileStateType) -> TranscriptionType:
    """
    Get transcription of an audio file using the specified model.

    This function gets the transcription of an audio file using the specified model.

    Parameters
    ----------
    - model (str): The transcription model to use.
    - file (dict): The file object containing the audio data.

    Returns
    -------
    - list: A list of transcriptions containing words with their start and end times.

    Raises
    ------
    - HTTPException: If the specified model is not found.

    """
    if model == "deepgram":
        return fill_gaps(deepgram_transcription(file["data"]), file)
    if model == "whisper":
        return fill_gaps(whisper_transcription(file["data"]), file)
    if model == "whisper-torgo-1-epoch":
        # name torgo here does not correspond to an actual hf model, it is the path to the local
        # folder containing the model. We do this because most hf models require patching.
        # If you want to change this, look into hf_transcription implementation, it has more info
        return fill_gaps(hf_transcription(file["data"], model_name="torgo"), file)
    if model == "allosaurus":
        return fill_gaps(allosaurus_transcription(file), file)
    raise HTTPException(status_code=404, detail="Model was not found")
