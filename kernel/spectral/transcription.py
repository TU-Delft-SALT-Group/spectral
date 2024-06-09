from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from fastapi import HTTPException
from jiwer import process_words, process_characters
from .signal_analysis import get_audio, calculate_signal_duration
from allosaurus.app import read_recognizer  # type: ignore
import tempfile
import os


def calculate_error_rates(reference_annotations, hypothesis_annotations):
    """
    Calculate error rates between the reference transcription and annotations.

    This function calculates both word-level and character-level error rates
    based on the provided reference transcription and annotations.

    Parameters:
    - reference (str): The reference transcription.
    - annotations (list of dict): The list of annotations where each annotation is a dictionary with a "value" key.

    Returns:
    - dict: A dictionary containing word-level and character-level error rates.

    """
    reference = annotation_to_sentence(reference_annotations)
    hypothesis = annotation_to_sentence(hypothesis_annotations)
    word_level = word_level_processing(reference, hypothesis)
    character_level = character_level_processing(reference, hypothesis)

    return {"wordLevel": word_level, "characterLevel": character_level}


def annotation_to_sentence(annotations):
    """
    Convert annotations to a single hypothesis string.

    This function concatenates the values from the annotations list to form a hypothesis string.

    Parameters:
    - annotations (list of dict): The list of annotations where each annotation is a dictionary with a "value" key.

    Returns:
    - str: A single concatenated hypothesis string.

    """
    res = ""
    if len(annotations) == 0:
        return res

    for annotation in annotations:
        if annotation["value"] == "":
            continue
        res += annotation["value"] + " "

    print(res[: len(res) - 1])

    return res[: len(res) - 1]


def word_level_processing(reference, hypothesis):
    """
    Process word-level error metrics between the reference and hypothesis.

    This function processes word-level metrics.

    Parameters:
    - reference (str): The reference transcription.
    - hypothesis (str): The hypothesis transcription.

    Returns:
    - dict: A dictionary containing word-level error metrics and alignments.

    """
    processed_data = process_words(reference=reference, hypothesis=hypothesis)
    result = {
        "wer": processed_data.wer,
        "mer": processed_data.mer,
        "wil": processed_data.wil,
        "wip": processed_data.wip,
        "hits": processed_data.hits,
        "substitutions": processed_data.substitutions,
        "insertions": processed_data.insertions,
        "deletions": processed_data.deletions,
        "reference": processed_data.references[0],
        "hypothesis": processed_data.hypotheses[0],
        "alignments": get_alignments(processed_data.alignments[0]),
    }

    return result


def character_level_processing(reference, hypothesis):
    """
    Process character-level error metrics between the reference and hypothesis.

    This function processes character-level metrics.

    Parameters:
    - reference (str): The reference transcription.
    - hypothesis (str): The hypothesis transcription.

    Returns:
    - dict: A dictionary containing character-level error metrics and alignments.

    """
    processed_data = process_characters(reference=reference, hypothesis=hypothesis)

    result = {
        "cer": processed_data.cer,
        "hits": processed_data.hits,
        "substitutions": processed_data.substitutions,
        "insertions": processed_data.insertions,
        "deletions": processed_data.deletions,
        "reference": processed_data.references[0],
        "hypothesis": processed_data.hypotheses[0],
        "alignments": get_alignments(processed_data.alignments[0]),
    }

    return result


def get_alignments(unparsed_alignments):
    """
    Convert unparsed alignments into a structured format.

    This function processes unparsed alignment data and converts it into a list of dictionaries
    with detailed alignment information.

    Parameters:
    - unparsed_alignments (list): A list of unparsed alignment objects.

    Returns:
    - list of dict: A list of dictionaries where each dictionary contains alignment information.

    """
    alignments = []

    for alignment in unparsed_alignments:
        alignment_dict = {
            "type": alignment.type,
            "referenceStartIndex": alignment.ref_start_idx,
            "referenceEndIndex": alignment.ref_end_idx,
            "hypothesisStartIndex": alignment.hyp_start_idx,
            "hypothesisEndIndex": alignment.hyp_end_idx,
        }
        alignments.append(alignment_dict)

    return alignments


def get_transcription(model, file):
    """
    Get transcription of an audio file using the specified model.

    This function gets the transcription of an audio file using the specified model.

    Parameters:
    - model (str): The transcription model to use.
    - file (dict): The file object containing the audio data.

    Returns:
    - list: A list of transcriptions containing words with their start and end times.

    Raises:
    - HTTPException: If the specified model is not found.
    """
    if model == "deepgram":
        return fill_gaps(deepgram_transcription(file["data"]), file)
    if model == "allosaurus":
        return fill_gaps(allosaurs_transcription(file), file)
    raise HTTPException(status_code=404, detail="Model was not found")


def fill_gaps(transcriptions, file):
    res = []

    audio = get_audio(file)
    duration = calculate_signal_duration(audio)

    if len(transcriptions) == 0:
        return [{"value": "", "start": 0, "end": duration}]

    time = 0

    for transcription in transcriptions:
        if time != transcription["start"]:
            res.append({"value": "", "start": time, "end": transcription["start"]})
        time = transcription["end"]
        res.append(transcription)

    if time != duration:
        res.append({"value": "", "start": time, "end": duration})

    return res


def deepgram_transcription(data):
    """
    Transcribe audio data using Deepgram API.

    This function transcribes audio data using the Deepgram API.

    Parameters:
    - data (bytes): The audio data to transcribe.

    Returns:
    - list: A list of transcriptions containing words with their start and end times.

    Raises:
    - Exception: If an error occurs during the transcription process.
    """
    try:
        # STEP 1: Create a Deepgram client using the API key
        key = os.getenv("DG_KEY")
        deepgram = None
        if key is None:
            raise Exception("No API key for Deepgram is found")
        else:
            deepgram = DeepgramClient(key)

        payload: FileSource = {
            "buffer": data,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            profanity_filter=False,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        res = []
        for word in response["results"]["channels"][0]["alternatives"][0]["words"]:
            res.append(
                {"value": word["word"], "start": word["start"], "end": word["end"]}
            )
        return res

    except Exception as e:
        print(f"Exception: {e}")


def allosaurs_transcription(file):
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


def get_phoneme_word_splits(word_level_transcription, phoneme_level_parsed):
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


def get_phoneme_transcriptions(phoneme_word_splits):
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
