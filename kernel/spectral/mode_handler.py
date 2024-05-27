from fastapi import HTTPException

from .signal_analysis import simple_signal_info
from .frame_analysis import simple_frame_info, calculate_frame_f1_f2
from .transcription import calculate_error_rates

def simple_info_mode(data, fs, file, frame_index):
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
    result = simple_signal_info(data, fs)
    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]
    result["frame"] = simple_frame_info(data, fs, frame_index)
    return result


def spectrogram_mode(data, fs, frame_index):
    """
    TBD
    """
    return None


def vowel_space_mode(data, fs, frame_index):
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
    if frame_index is None:
        return None
    frame_data = data[frame_index["startIndex"] : frame_index["endIndex"]]
    formants = calculate_frame_f1_f2(frame_data, fs)
    return {"f1": formants[0], "f2": formants[1]}


def transcription_mode(id, database):
    """
    Retrieve transcriptions of a file from the database.

    This function retrieves transcriptions associated with a file from the database.

    Parameters:
    - id (str): The ID of the file.
    - database (Database): An instance of the Database class for interacting with the database.

    Returns:
    - list: A list of transcriptions associated with the file.

    Raises:
    - HTTPException: If something goes wrong when retrieving the transcriptions of the file.
    """
    try:
        return database.get_transcriptions(id)
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong when retrieving the transcriptions of this file",
        )

def error_rate_mode(id, database, file):
    
    if file["groundTruth"] is None:
        return None
    
    try:
        transcriptions = database.get_transcriptions(id)
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong when retrieving the transcriptions of this file",
        )
        
    errorRates = []
    
    for transcription in transcriptions:
        errorRates.append(calculate_error_rates(file["groundTruth"], transcription))
        
    return {"groundTruth": file["groundTruth"], "errorRates": errorRates}