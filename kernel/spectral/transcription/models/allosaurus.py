"""All the functionality related to the allosaurus transcription models."""

from __future__ import annotations

import tempfile

from allosaurus.app import read_recognizer  # type: ignore

from spectral.transcription.transcription_utils import fill_gaps
from spectral.types import FileStateType

from .deepgram import deepgram_transcription


def allosaurus_transcription(file: FileStateType) -> list[dict]:
    """Produce trancription of a wav file, the main access venue for the allosaurus."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav.write(file["data"])
        temp_wav_filename = temp_wav.name

    word_level_transcription = fill_gaps(deepgram_transcription(file["data"]), file)

    model = read_recognizer()
    phoneme_level_transcription = model.recognize(
        temp_wav_filename,
        timestamp=True,
        emit=1.2,
    )

    phoneme_level_parsed = [
        [float(phoneme_string.split(" ")[0]), phoneme_string.split(" ")[2]]
        for phoneme_string in phoneme_level_transcription.splitlines()
    ]

    phoneme_word_splits = get_phoneme_word_splits(
        word_level_transcription,
        phoneme_level_parsed,
    )
    return get_phoneme_transcriptions(phoneme_word_splits)


def get_phoneme_word_splits(
    word_level_transcription: list[dict],
    phoneme_level_parsed: list[list],
) -> list[dict]:
    """Aligns phonemes given word level transription."""
    if len(word_level_transcription) == 0:
        return []

    word_pointer = 0
    phoneme_pointer = 0

    phoneme_word_splits = []

    current_split = {"phonemes": [], "word_transcription": None}

    while word_pointer < len(word_level_transcription) and phoneme_pointer < len(
        phoneme_level_parsed,
    ):
        if phoneme_level_parsed[phoneme_pointer][0] > word_level_transcription[word_pointer]["end"]:
            current_split["word_transcription"] = word_level_transcription[word_pointer]
            phoneme_word_splits.append(current_split)
            current_split = {"phonemes": [], "word_transcription": None}
            word_pointer += 1
            continue

        current_split["phonemes"].append(phoneme_level_parsed[phoneme_pointer])
        phoneme_pointer += 1

    if phoneme_pointer == len(phoneme_level_parsed):
        current_split["word_transcription"] = word_level_transcription[word_pointer]
        phoneme_word_splits.append(current_split)

    return phoneme_word_splits


def get_phoneme_transcriptions(phoneme_word_splits: list[dict]) -> list[dict]:
    """Produce phonemes given word splits."""
    res = []

    for phoneme_split in phoneme_word_splits:
        if len(phoneme_split) == 0:
            continue

        for i in range(len(phoneme_split["phonemes"])):
            start = 0
            if i == 0:
                start = phoneme_split["word_transcription"]["start"]
            else:
                # this is an (educated) guess, it could be way off :D
                start = (phoneme_split["phonemes"][i - 1][0] + phoneme_split["phonemes"][i][0]) / 2

            end = 0
            if i + 1 == len(phoneme_split["phonemes"]):
                end = phoneme_split["word_transcription"]["end"]
            else:
                end = (phoneme_split["phonemes"][i + 1][0] + phoneme_split["phonemes"][i][0]) / 2

            res.append(
                {"value": phoneme_split["phonemes"][i][1], "start": start, "end": end},
            )

    return res
