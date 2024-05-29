from fastapi import HTTPException

from .signal_analysis import simple_signal_info
from .frame_analysis import (
    simple_frame_info,
    calculate_frame_f1_f2,
    validate_frame_index,
)
from .transcription import calculate_error_rates

from pydub import AudioSegment
import io


def simple_info_mode(database, file_state):
    """
    Extracts and returns basic information about a signal and its corresponding frame.

    This function combines the signal information, file metadata, and frame-specific details.

    Parameters:
    - data (list of int): The audio signal data.
    - fs (float): The sample frequency of the audio signal.
    - file (dict): A dictionary containing file metadata such as "data" and "creationTime".
    - frame_index (dict): A dictionary containing the 'startIndex' and 'endIndex' that specify
                          the segment of the signal to analyze.

    Returns:
    - dict: A dictionary containing the combined signal information, file size, file creation date,
            and frame information.

    Example:
    ```python
    result = simple_info_mode(data, fs, file, frame_index)
    ```
    """

    file = get_file(database, file_state)

    fs, data = get_audio(file)

    result = simple_signal_info(data, fs)

    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]

    frame_index = validate_frame_index(data, file_state)

    result["frame"] = simple_frame_info(data, fs, frame_index)

    return result


def spectrogram_mode(database, file_state):
    """
    TBD
    """
    return None


def waveform_mode(database, file_state):
    """
    TBD
    """
    return None


def vowel_space_mode(database, file_state):
    """
    Extracts and returns the first and second formants of a specified frame.

    This function calculates the first (f1) and second (f2) formants of a segment within the audio signal.

    Parameters:
    - data (list of int): The audio signal data.
    - fs (float): The sample frequency of the audio signal.
    - frame_index (dict): A dictionary containing the 'startIndex' and 'endIndex' that specify
                          the segment of the signal to analyze.

    Returns:
    - dict: A dictionary containing the first formant (f1) and the second formant (f2).

    Example:
    ```python
    result = vowel_space_mode(data, fs, frame_index)
    ```
    """

    file = get_file(database, file_state)
    fs, data = get_audio(file)
    frame_index = validate_frame_index(data, file_state)

    if frame_index is None:
        return None

    frame_data = data[frame_index["startIndex"] : frame_index["endIndex"]]
    formants = calculate_frame_f1_f2(frame_data, fs)
    return {"f1": formants[0], "f2": formants[1]}


def transcription_mode(database, file_state):
    """
    TBD
    """
    return None


def error_rate_mode(database, file_state):
    if "transcriptions" not in file_state:
        return None

    transcriptions = file_state["transcriptions"]

    file = get_file(database, file_state)

    if file["groundTruth"] is None or transcriptions is None:
        return None

    errorRates = []

    for transcription in transcriptions:
        errorRates.append(calculate_error_rates(file["groundTruth"], transcription))

    return {"groundTruth": file["groundTruth"], "errorRates": errorRates}


def get_file(database, file_state):
    if "id" not in file_state:
        raise HTTPException(status_code=404, detail="file_state did not include id")

    try:
        file = database.fetch_file(file_state["id"])
    except Exception as _:
        raise HTTPException(status_code=404, detail="File not found")

    return file


def get_audio(file):
    audio = AudioSegment.from_file(io.BytesIO(file["data"]))
    fs = audio.frame_rate
    data = audio.get_array_of_samples()

    return fs, data
