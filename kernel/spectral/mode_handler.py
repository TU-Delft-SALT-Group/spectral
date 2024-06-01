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
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including frame indices.

    Returns:
    - dict: A dictionary containing the combined signal information, file size, file creation date,
            and frame information. If the frame index is invalid, it still includes the basic file information.

    Example:
    ```python
    result = simple_info_mode(database, file_state)
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
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including frame indices.

    Returns:
    - dict: A dictionary containing the first formant (f1) and the second formant (f2).
    - Returns None if the frame index is invalid.

    Example:
    ```python
    result = vowel_space_mode(database, file_state)
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
    """
    Calculate the error rates of transcriptions against the ground truth.

    Parameters:
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including transcriptions.

    Returns:
    - A dictionary with the ground truth and a list of error rates for each transcription.
    - Returns None if there are no transcriptions or if the ground truth is missing.

    Example:
    ```python
    result = error_rate_mode(database, file_state)
    ```
    """
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
    """
    Fetch a file from the database using the file_state information.

    Parameters:
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including its ID.

    Returns:
    - The file object fetched from the database.

    Raises:
    - HTTPException: If the 'id' is not in file_state or if the file is not found.

    Example:
    ```python
    file = get_file(database, file_state)
    ```
    """
    if "id" not in file_state:
        raise HTTPException(status_code=404, detail="file_state did not include id")

    try:
        file = database.fetch_file(file_state["id"])
    except Exception as _:
        raise HTTPException(status_code=404, detail="File not found")

    return file


def get_audio(file):
    """
    Extract audio data and sampling rate from the given file.

    Parameters:
    - file: A dictionary containing the file data, including audio bytes.

    Returns:
    - A tuple (fs, data) where fs is the sampling rate and data is the array of audio samples.

    Example:
    ```python
    fs, data = get_audio(file)
    ```
    """
    audio = AudioSegment.from_file(io.BytesIO(file["data"]))
    fs = audio.frame_rate
    data = audio.get_array_of_samples()

    return fs, data