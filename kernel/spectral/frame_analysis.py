import parselmouth
import numpy as np


def simple_frame_info(frame, fs, frame_info):
    """
    Extracts and returns basic information from a given audio frame.

    This function calculates and returns the duration, pitch, and first two formants (f1 and f2)
    of a specified segment within the audio frame.

    Parameters:
    - frame (list of int): The audio frame data.
    - fs (float): The sample frequency of the audio signal.
    - frame_info (dict): A dictionary containing the 'startIndex' and 'endIndex' that specify
                         the segment of the frame to analyze.

    Returns:
    - dict or None: A dictionary with the following keys and their corresponding values if
                    `frame_info` is provided, otherwise returns None:
                    - "duration" (float): Duration of the frame segment.
                    - "pitch" (float): Pitch of the frame segment.
                    - "f1" (float): The first formant frequency of the frame segment.
                    - "f2" (float): The second formant frequency of the frame segment.

    Example:
    ```python
    frame_info = {"startIndex": 0, "endIndex": 1000}
    result = simple_frame_info(frame, fs, frame_info)
    ```
    """
    if frame_info is None:
        return None
    data = frame[frame_info["startIndex"] : frame_info["endIndex"]]
    res = {}
    res["duration"] = calculate_frame_duration(data, fs)
    res["pitch"] = calculate_frame_pitch(data, fs)
    formants = calculate_frame_f1_f2(data, fs)
    res["f1"] = formants[0]
    res["f2"] = formants[1]
    return res


def calculate_frame_duration(frame, fs):
    """
    This method calculates the duration of a frame based on the frame and the sample frequency.

    Parameters:
    - frame (arr['float']): array of floats representing an audio frame.
    - fs (float): sample frequency of speech signal.

    Returns:
    - (return float): Duration of the frame.

    Example:
    ```python
    result = calculate_frame_duration(frame, fs)
    ```
    """
    return len(frame) / fs


def calculate_frame_pitch(frame, fs):
    """
    This method calculates the pitch of a frame.

    Parameters:
    - frame (arr['float']): array of floats representing an audio frame.
    - fs (float): sample frequency of speech signal.

    Returns:
    - (return float): Pitch of the frame.

    Example:
    ```python
    result = calculate_frame_pitch(frame, fs)
    ```
    """
    try:
        pitch = parselmouth.Sound(
            values=np.array(frame).astype("float64"), sampling_frequency=fs
        ).to_pitch(
            time_step=calculate_frame_duration(frame, fs) + 1
        )  # the + 1 ensures that the complete frame is considered as 1 frame
        return pitch.get_value_at_time(0)
    except Exception as _:
        return float("nan")


def calculate_frame_f1_f2(frame, fs):
    """
    This method calculates the first and second fromant of a frame.

    Parameters:
    - frame (arr['float']): array of floats representing an audio frame.
    - fs (float): sample frequency of speech signal.

    Returns:
    - (return arr['float']): with position 0 containing f1 and position 1 containing f2.

    Example:
    ```python
    result = calculate_frame_f1_f2(frame, fs)
    ```
    """
    try:
        formants = parselmouth.Sound(
            values=np.array(frame).astype("float64"), sampling_frequency=fs
        ).to_formant_burg(
            time_step=calculate_frame_duration(frame, fs) + 1
        )  # the + 1 ensures that the complete frame is considered as 1 frame
        return [
            formants.get_value_at_time(formant_number=1, time=0),
            formants.get_value_at_time(formant_number=2, time=0),
        ]
    except Exception as _:
        return [float("nan"), float("nan")]
