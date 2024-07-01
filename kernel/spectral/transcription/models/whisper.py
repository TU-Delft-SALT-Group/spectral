"""Whisper model APIs."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from openai import OpenAI

from spectral.types import TranscriptionType


def whisper_transcription(data: bytes, api_key: str | None = None) -> TranscriptionType:
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
        transcription = get_whisper_transcription(data, api_key)

    except Exception as e:
        raise HTTPException(status_code=401, detail="Something went wrong when transcribing") from e
    else:
        res = []

        if hasattr(transcription, "words"):
            words = transcription.words  # pyright: ignore[reportAttributeAccessIssue]

            res = [
                {"value": word["word"], "start": word["start"], "end": word["end"]}
                for word in words
            ]

        return {"language": transcription.language, "transcription": res}


def get_whisper_transcription(data: bytes, apikey: str | None = None) -> Any:
    """
    Get the Transcription from whisper.

    Args:
    ----
        data (bytes): list of data bytes representing a WAV audio signal

    Returns:
    -------
        Any: Transcription object from OpenAi

    """
    client = OpenAI(api_key=apikey)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav.write(data)
        temp_wav_filename = temp_wav.name

    with Path(temp_wav_filename).open("rb") as f:
        return client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["word"],
        )
