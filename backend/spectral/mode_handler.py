from fastapi import HTTPException

from .signal_analysis import simple_signal_info
from .frame_analysis import (
    simple_frame_info,
    calculate_frame_f1_f2
)

def simple_info_mode(data,fs,file,frame_index):
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
    result = simple_signal_info(data,fs)
    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]
    result["frame"] = simple_frame_info(data,fs,frame_index)
    return result
    
def spectogram_mode(data,fs,frame_index):
    """ TBD
    Raises:
        HTTPException: 501 not implemented
    """
    raise HTTPException(
        status_code=501, detail="spectogram_mode is not implemented"
    )

def vowel_space_mode(data,fs,frame_index):
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

    Raises:
    - HTTPException: If `frame_index` is None, raises an HTTPException with status code 400
                     and a message indicating that a frame index was not provided.

    Example:
    ```python
    result = vowel_space_mode(data, fs, frame_index)
    ```
    """
    if frame_index is None:
        raise HTTPException(
            status_code=400, detail="Vowel-space mode was not given frame"
        )
    frame_data = data[frame_index["startIndex"]:frame_index["endIndex"]]
    formants = calculate_frame_f1_f2(frame_data,fs)
    return {"f1":formants[0],"f2":formants[1]}
    
    
    