import parselmouth
import numpy as np


def simple_signal_info(signal, fs):
    """
    Extracts and returns basic information from a given audio signal.

    This function calculates the duration and average pitch of the provided audio signal.

    Parameters:
    - signal (list of int): The audio signal data.
    - fs (float): The sample frequency of the audio signal.

    Returns:
    - dict: A dictionary containing the duration and average pitch of the signal.

    Example:
    ```python
    result = simple_signal_info(signal, fs)
    ```
    """
    duration = calculate_signal_duration(signal=signal, fs=fs)
    avg_pitch = np.mean(
        calculate_sound_pitch(signal_to_sound(signal=signal, fs=fs))["data"]  # type: ignore
    ).item()
    return {"duration": duration, "averagePitch": avg_pitch}


def signal_features(signal, fs):
    """
    Extracts and returns various features from a given audio signal.

    This function calculates the duration, pitch, spectrogram, and formants of the provided audio signal.

    Parameters:
    - signal (list of int): The audio signal data.
    - fs (float): The sample frequency of the audio signal.

    Returns:
    - dict: A dictionary containing the duration, pitch, spectrogram, and formants of the signal.

    Example:
    ```python
    result = signal_features(signal, fs)
    ```
    """
    sound = signal_to_sound(signal, fs)
    duration = calculate_signal_duration(signal, fs)
    pitch = calculate_sound_pitch(sound)
    spectrogram = calculate_sound_spectrogram(sound)
    formants = calculate_sound_f1_f2(sound)
    return {
        "duration": duration,
        "pitch": pitch,
        "spectogram": spectrogram,
        "formants": formants,
    }


def signal_to_sound(signal, fs):
    """
    This method converts a signal to a parselmouth sound object.

    Parameters:
    - signal (arr['float']): array of floats representing an audio signal.
    - fs (float): sample frequency of speech signal.

    Returns:
    - (return parselmout.Sound): Sound object of the signal.

    Example:
    ```python
    result = signal_to_sound(signal, fs)
    ```
    """
    return parselmouth.Sound(
        values=np.array(signal).astype("float64"), sampling_frequency=fs
    )


def calculate_signal_duration(signal, fs):
    """
    This method calculates the duration of a signal based on the signal and the sample frequency.

    Parameters:
    - signal (arr['float']): array of floats representing an audio signal.
    - fs (float): sample frequency of speech signal.

    Returns:
    - (return float): Duration of the signal.

    Example:
    ```python
    result = calculate_signal_duration(signal, fs)
    ```
    """
    return len(signal) / fs


def calculate_sound_pitch(sound, time_step=None):
    """
    This method calculates the pitches present in a sound object.

    Parameters:
    - sound (parselmouth.Sound): Sound object representing a speech fragment.
    - time_step (float): Time between pitch samples.

    Returns:
    - time_step (float): Time between pitch samples.
    - start_time (float): Time of center of first pitch sample.
    - data (arr['float']): 1D array of the frequencies of the pitch samples.

    Example:
    ```python
    result = calculate_sound_pitch(sound, time_step)
    ```
    """
    try:
        pitch = sound.to_pitch(time_step=time_step)
        return {
            "time_step": pitch.time_step,
            "start_time": pitch.get_time_from_frame_number(1),
            "data": pitch.selected_array["frequency"].tolist(),
        }
    except Exception as _:
        return None


def calculate_sound_spectrogram(
    sound, time_step=0.002, window_length=0.005, frequency_step=20.0
):
    """
    This method calculates the spectrogram of a sound fragment.

    Parameters:
    - sound (parselmouth.Sound): Sound object representing a speech fragment.
    - time_step (float): Time between the center of the frames.
    - window_length (float): Duration of the analysis window.
    - frequency_step (float): Frequency resolution.

    Returns:
    - time_step (float): Time between spectogram samples.
    - window_length (float): Duration of the analysis window.
    - frequency_step (float): Frequency resolution.
    - start_time (float): Time of center of the frame.
    - data (numpy.ndarray): 2D array representing the spectrogram.

    Example:
    ```python
    result = calculate_sound_spectrogram(sound, time_step, window_length, frequency_step)
    ```
    """
    try:
        spectrogram = sound.to_spectrogram(
            time_step=time_step,
            window_length=window_length,
            frequency_step=frequency_step,
        )
        return {
            "time_step": spectrogram.time_step,
            "window_length": window_length,
            "frequency_step": frequency_step,
            "start_time": spectrogram.get_time_from_frame_number(1),
            "data": spectrogram.values.tolist(),
        }
    except Exception:
        return None


def calculate_sound_f1_f2(sound, time_step=None, window_length=0.025):
    """
    This method calculates the first and second formant of a sound fragment.

    Parameters:
    - sound (parselmouth.Sound): Sound object representing a speech fragment.
    - time_step (float): Time between the center of the frames.
    - window_length (float): Effective duration of the analysis window.

    Returns:
    - time_step (float): Time between the center of the frames.
    - window_length (float): Effective duration of the analysis window.
    - start_time (float): Time of center of the first frame.
    - data (numpy.ndarray): 2D array with the f1 and f2 found in each frame.

    Example:
    ```python
    result = calculate_sound_f1_f2(sound, time_step, window_length)
    ```
    """
    try:
        formants = sound.to_formant_burg(
            time_step=time_step, window_length=window_length
        )
        data = []
        for frame in np.arange(1, len(formants) + 1):
            data.append(
                [
                    formants.get_value_at_time(
                        formant_number=1, time=formants.frame_number_to_time(frame)
                    ),
                    formants.get_value_at_time(
                        formant_number=2, time=formants.frame_number_to_time(frame)
                    ),
                ]
            )
        return {
            "time_step": formants.time_step,
            "window_length": window_length,
            "start_time": formants.get_time_from_frame_number(1),
            "data": data,
        }
    except Exception as _:
        return None
