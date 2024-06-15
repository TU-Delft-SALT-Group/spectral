from openai import OpenAI
import os
import tempfile
from typing import Any


def whisper_transcription(data: bytes) -> dict[str, str | list[dict]]:
    """Get transcription from whisper from an list of WAV bytes

    Args:
        data (bytes): list of data bytes representing a WAV audio signal

    Returns:
        list[dict]: list of dictionaries containing start, end and value
    """
    try:
        transcription = get_whisper_transcription(data)

        res = []

        if hasattr(transcription, "words"):
            words = transcription.words  # pyright: ignore[reportAttributeAccessIssue]

            for word in words:
                res.append(
                    {"value": word["word"], "start": word["start"], "end": word["end"]}
                )

        return {"language": transcription.language, "transcription": res}

    except Exception as e:
        print(f"Exception: {e}")
        return {"language": "", "transcription": []}


def get_whisper_transcription(data: bytes) -> Any:
    """Get the Transcription from whisper

    Args:
        data (bytes): list of data bytes representing a WAV audio signal

    Returns:
        Any: Transcription object from OpenAi
    """
    client = OpenAI(api_key=os.getenv("WHISPER_KEY"))
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav.write(data)
        temp_wav_filename = temp_wav.name

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(temp_wav_filename, "rb"),
        response_format="verbose_json",
        timestamp_granularities=["word"],
    )

    return transcription
