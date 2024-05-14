import parselmouth
import numpy as np


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
