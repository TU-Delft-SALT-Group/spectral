"""The functionality related to the Deepgram transription models."""

from __future__ import annotations

import os

from deepgram import DeepgramClient, PrerecordedOptions


def deepgram_transcription(data: bytes) -> list[dict]:
    """
    Transcribe audio data using Deepgram API.

    This function transcribes audio data using the Deepgram API.

    Parameters
    ----------
    - data (bytes): The audio data to transcribe.

    Returns
    -------
    - list: A list of transcriptions containing words with their start and end times.

    Raises
    ------
    - Exception: If an error occurs during the transcription process.

    """
    # STEP 1: Create a Deepgram client using the API key
    key = os.getenv("DG_KEY")
    deepgram = None
    if key is None:
        raise RuntimeError("No API key for Deepgram is found")
    deepgram = DeepgramClient(key)  # type: ignore

    payload = {
        "buffer": data,
    }

    # STEP 2: Configure Deepgram options for audio analysis
    options = PrerecordedOptions(  # type: ignore
        model="nova-2",
        smart_format=True,
        profanity_filter=False,
    )

    # STEP 3: Call the transcribe_file method with the text payload and options
    response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

    return [
        {"value": word["word"], "start": word["start"], "end": word["end"]}
        for word in response["results"]["channels"][0]["alternatives"][0]["words"]
    ]
