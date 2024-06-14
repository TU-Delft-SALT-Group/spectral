"""Useful utilities for transcription processing."""

from __future__ import annotations

from spectral.signal_analysis import calculate_signal_duration, get_audio


def fill_gaps(
    transcriptions_and_language: dict[str, str | list[dict]],
    file: dict,
) -> dict[str, str | list[dict]]:
    """
    Fill the gaps between consecutive transcription dictionaries such that all
    time is accounted for.

    Args:
    ----
        transcriptions_and_language (dict): contains a language string and a list of transcriptions
                                            with possible gaps in time.
        file (dict): The state of the file that is being transcribed.

    Returns:
    -------
        dict: a dictionary with language and list of transcriptions with gaps
              filled with empty strings.

    """
    transcriptions = transcriptions_and_language.get("transcription", [])
    res = []

    audio = get_audio(file)
    duration = calculate_signal_duration(audio)

    if not transcriptions:
        return {
            "language": transcriptions_and_language["language"],
            "transcription": [{"value": "", "start": 0, "end": duration}],
        }

    time = 0

    if isinstance(transcriptions, list):
        for transcription in transcriptions:
            if time != transcription["start"]:
                res.append({"value": "", "start": time, "end": transcription["start"]})
            time = transcription["end"]
            res.append(transcription)

        if time != duration:
            res.append({"value": "", "start": time, "end": duration})

    return {"language": transcriptions_and_language["language"], "transcription": res}
