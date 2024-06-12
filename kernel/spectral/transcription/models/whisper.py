"""Functionality related to the Whisper OpenAI model."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from openai import OpenAI


def whisper_transcription(data: bytes) -> list[dict]:
    """Transcribes the given wav data using the whisper model."""
    try:
        client = OpenAI(api_key=os.getenv("WHISPER_KEY"))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav.write(data)
            temp_wav_filename = temp_wav.name

        with Path(temp_wav_filename).open("rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=file,
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )

        return [
            {"value": word["word"], "start": word["start"], "end": word["end"]}
            for word in getattr(transcription, "words", [])
        ]

    except Exception:
        return []
