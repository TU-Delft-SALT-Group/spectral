import parselmouth
import numpy as np
from pydub import AudioSegment
from .types import AudioType, SoundType
import io
from typing import Any
from array import array


def get_audio(file: dict[str, Any]) -> AudioType:
    """
    Extract audio data and sampling rate from the given file.

    Parameters:
    - file: A dictionary containing the file data, including audio bytes.

    Returns:
    - A list, that contains audio data

    Example:
    ```python
    audio = get_audio(file)
    ```
    """
    audio = AudioSegment.from_file(io.BytesIO(file["data"]))

    return audio


def simple_signal_info(audio: AudioType) -> dict[str, Any]:
    """
    Extracts and returns basic information from a given audio signal.

    This function calculates the duration and average pitch of the provided audio signal.

    Parameters:
    - signal (list of int): The audio signal data.

    Returns:
    - dict: A dictionary containing the duration and average pitch of the signal.

    Example:
    ```python
    result = simple_signal_info(signal, fs)
    ```
    """
    duration: float = calculate_signal_duration(audio)
    avg_pitch: float = np.mean(
        calculate_sound_pitch(
            signal_to_sound(signal=audio.get_array_of_samples(), fs=audio.frame_rate)
        )["data"]  # type: ignore
    ).item()
    return {"duration": duration, "averagePitch": avg_pitch}


def signal_to_sound(signal: array, fs: float | int) -> SoundType:
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
    return parselmouth.Sound(values=np.array(signal).astype("float64"), sampling_frequency=fs)


def calculate_signal_duration(audio: AudioType) -> float:
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
    return audio.duration_seconds


def calculate_sound_pitch(
    sound: SoundType, time_step: float | None = None
) -> dict[str, Any] | None:  # pragma: no cover
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
    sound: SoundType,
    time_step: float = 0.002,
    window_length: float = 0.005,
    frequency_step: float = 20.0,
) -> dict[str, Any] | None:  # pragma: no cover
    """
    This method calculates the spectrogram of a sound fragment.

    Parameters:
    - sound (parselmouth.Sound): Sound object representing a speech fragment.
    - time_step (float): Time between the center of the frames.
    - window_length (float): Duration of the analysis window.
    - frequency_step (float): Frequency resolution.

    Returns:
    - time_step (float): Time between spectrogram samples.
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


def calculate_sound_f1_f2(
    sound: SoundType, time_step: float | None = None, window_length: float = 0.025
):  # pragma: no cover
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
        formants = sound.to_formant_burg(time_step=time_step, window_length=window_length)
        data: list = []
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
