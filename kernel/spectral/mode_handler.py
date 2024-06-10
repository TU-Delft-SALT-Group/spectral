from fastapi import HTTPException

from .signal_analysis import simple_signal_info, get_audio

from .frame_analysis import (
    simple_frame_info,
    calculate_frame_f1_f2,
    validate_frame_index,
)
from .transcription import calculate_error_rates
import tempfile
import subprocess


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

    audio = get_audio(file)

    result = simple_signal_info(audio)

    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]

    frame_index = validate_frame_index(audio.get_array_of_samples(), file_state)

    result["frame"] = simple_frame_info(
        audio.get_array_of_samples(), audio.frame_rate, frame_index
    )

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
    audio = get_audio(file)
    data = audio.get_array_of_samples()
    frame_index = validate_frame_index(data, file_state)

    if frame_index is None:
        return None

    frame_data = data[frame_index["startIndex"] : frame_index["endIndex"]]
    formants = calculate_frame_f1_f2(frame_data, audio.frame_rate)
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
    if (
        "reference" not in file_state
        or file_state["reference"] is None
        or "captions" not in file_state["reference"]
        or file_state["reference"]["captions"] is None
        or "hypothesis" not in file_state
        or file_state["hypothesis"] is None
        or "captions" not in file_state["hypothesis"]
        or file_state["hypothesis"]["captions"] is None
    ):
        return None

    errorRate = calculate_error_rates(
        file_state["reference"]["captions"], file_state["hypothesis"]["captions"]
    )

    return errorRate


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

    file["data"] = convert_to_wav(file["data"])

    return file


def convert_to_wav(data):
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(data)
        temp_input.flush()  # Ensure data is written to disk
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_output:
            command = ["ffmpeg", "-y", "-i", temp_input.name, temp_output.name]
            subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            temp_output.seek(0)  # Rewind to the beginning of the file
            return temp_output.read()
