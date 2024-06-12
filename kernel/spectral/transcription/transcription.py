from fastapi import HTTPException

from ..types import FileStateType
from .models.allosaurus import allosaurus_transcription
from .models.deepgram import deepgram_transcription
from .models.whisper import whisper_transcription
from .transcription_utils import fill_gaps


def get_transcription(model: str, file: FileStateType):
    """Get transcription of an audio file using the specified model.

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
    if model == "allosaurus":
        return fill_gaps(allosaurus_transcription(file), file)
    raise HTTPException(status_code=404, detail="Model was not found")
