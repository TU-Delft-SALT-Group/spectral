from pydantic import BaseModel
from typing import Optional


class Frame(BaseModel):
    """
    Frame model representing a frame of data with its sampling frequency.

    Attributes:
        data (list): The data contained in the frame.
        fs (float): The sampling frequency of the data.
    """

    data: list
    fs: float


class Signal(BaseModel):
    """
    Signal model representing a signal which contains both various attributes related to its
    sampling frequency and values, and parameters for calculating the pitches, spectogram and formants

    Attributes:
        data (list): The data contained in the signal.
        fs (float): The sampling frequency of the signal.
        pitch_time_step (Optional[float]): The time step for pitch analysis. Defaults to None.
        spectogram_time_step (float): The time step for spectrogram analysis. Defaults to 0.002 seconds.
        spectogram_window_length (float): The window length for spectrogram analysis. Defaults to 0.005 seconds.
        spectogram_frequency_step (float): The frequency step for spectrogram analysis. Defaults to 20.0 Hz.
        formants_time_step (Optional[float]): The time step for formants analysis. Defaults to None.
        formants_window_length (float): The window length for formants analysis. Defaults to 0.025 seconds.
    """

    data: list
    fs: float
    pitch_time_step: Optional[float] = None
    spectogram_time_step: float = 0.002
    spectogram_window_length: float = 0.005
    spectogram_frequency_step: float = 20.0
    formants_time_step: Optional[float] = None
    formants_window_length: float = 0.025
