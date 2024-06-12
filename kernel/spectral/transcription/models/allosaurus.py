import tempfile
from ...types import FileStateType
from ..transcription_utils import fill_gaps
from .deepgram import deepgram_transcription
from allosaurus.app import read_recognizer  # type: ignore


def allosaurus_transcription(file: FileStateType) -> list[dict]:
    """Calculate the transcription on phoneme level using the allosaurus model.

    Args:
        file (FileStateType): contains data about the file that is being transcribed.

    Returns:
        list[dict]: list of dictionaries containing a start, end and value.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav.write(file["data"])
        temp_wav_filename = temp_wav.name

    word_level_transcription = fill_gaps(deepgram_transcription(file["data"]), file)

    model = read_recognizer()
    phoneme_level_transcription = model.recognize(
        temp_wav_filename, timestamp=True, emit=1.2
    )

    phoneme_level_parsed = []

    for phoneme_string in phoneme_level_transcription.splitlines():
        phoneme_level_parsed.append(
            [float(phoneme_string.split(" ")[0]), phoneme_string.split(" ")[2]]
        )

    phoneme_word_splits = get_phoneme_word_splits(
        word_level_transcription, phoneme_level_parsed
    )
    return get_phoneme_transcriptions(phoneme_word_splits)


def get_phoneme_word_splits(
    word_level_transcription: list[dict], phoneme_level_parsed: list[list]
) -> list[dict]:
    """group the calculated phonemes in intervals based on word transcription

    Args:
        word_level_transcription (list[dict]): list of word level transcription
        phoneme_level_parsed (list[list]): list of phoneme level transcriptions

    Returns:
        list[dict]: list of dictionaries containing a list of phoneme transcription paired with a word level transcription
    """
    if len(word_level_transcription) == 0:
        return []

    word_pointer = 0
    phoneme_pointer = 0

    phoneme_word_splits = []

    current_split = {"phonemes": [], "word_transcription": None}

    while word_pointer < len(word_level_transcription) and phoneme_pointer < len(
        phoneme_level_parsed
    ):
        if (
            phoneme_level_parsed[phoneme_pointer][0]
            > word_level_transcription[word_pointer]["end"]
        ):
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
    """Convert the phoneme word groups to 1 list of phoneme transcriptions with adjusted start and end times

    Args:
        phoneme_word_splits (list[dict]): list of dictionaries containing a list of phoneme transcription paired with a word level transcription

    Returns:
        list[dict]: list of dictionaries containing start, end and value
    """
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
                start = (
                    phoneme_split["phonemes"][i - 1][0]
                    + phoneme_split["phonemes"][i][0]
                ) / 2

            end = 0
            if i + 1 == len(phoneme_split["phonemes"]):
                end = phoneme_split["word_transcription"]["end"]
            else:
                end = (
                    phoneme_split["phonemes"][i + 1][0]
                    + phoneme_split["phonemes"][i][0]
                ) / 2

            res.append(
                {"value": phoneme_split["phonemes"][i][1], "start": start, "end": end}
            )

    return res
