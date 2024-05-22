from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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

class FrameAnalysisResponse(BaseModel):
    """
    FrameAnalysisResponse model representing the results of frame analysis.

    Attributes:
        duration (float): Duration (in seconds) of the frame.
        pitch (float): Fundamental frequency (F0) of the frame (in Hz).
        f1 (float): First formant frequency of the frame (in Hz).
        f2 (float): Second formant frequency of the frame (in Hz).
    """
    
    duration: float
    pitch: float
    f1: float
    f2: float

class SignalPitch(BaseModel):
    """
    SignalPitch model representing extracted pitch information from a signal.

    Attributes:
        time_step (float): Time step (in seconds) between pitch data points.
        start_time (float): Starting time (in seconds) of the analysis.
        data (List[float]): List containing the pitch values (in Hz) for each time step.
    """
    
    time_step: float
    start_time: float
    data: List[float]

class SignalSpectrogram(BaseModel):
    """
    SignalSpectrogram model representing extracted spectrogram information from a signal.

    Attributes:
        time_step (float): Time step (in seconds) between spectrogram columns.
        window_length (float): Window length (in seconds) used for spectrogram analysis.
        frequency_step (float): Frequency step (in Hz) between spectrogram rows. 
        start_time (float): Starting time (in seconds) of the analysis.
        data (List[float]): List containing the spectrogram data in row-major order (time, frequency).
    """
    
    time_step: float
    window_length: float
    frequency_step: float
    start_time: float
    data: List[float]

class SignalFormants(BaseModel):
    """
    SignalFormants model representing extracted formant information from a signal.

    Attributes:
        time_step (float): Time step (in seconds) between formant data points.
        window_length (float): Window length (in seconds) used for formants analysis.
        start_time (float): Starting time (in seconds) of the analysis.
        data (List[List[float]]): List containing formant frequencies (in Hz) for each time step (inner list represents multiple formants).
    """
    
    time_step: float
    window_length: float
    start_time: float
    data: List[List[float]]

class SignalAnalysisResponse(BaseModel):
    """
    SignalAnalysisResponse model representing the results of signal analysis.

    Attributes:
        duration (float): Total duration (in seconds) of the signal.
        pitch (SignalPitch): Extracted pitch information for the signal.
        spectrogram (SignalSpectrogram): Extracted spectrogram information for the signal.
        formants (SignalFormants): Extracted formant information for the signal.
    """
    
    duration: float
    pitch: SignalPitch
    spectrogram: SignalSpectrogram
    formants: SignalFormants

class SimpleInfoResponse(BaseModel):
    """
    SimpleInfoResponse model containing basic information about a signal.

    Attributes:
        duration (float): Duration (in seconds) of the signal.
        averagePitch (float): Average pitch (F0) of the signal (in Hz).
        fileSize (int): File size of the signal data (in bytes).
        fileCreationDate (datetime): Date and time the signal file was created.
        frame (FrameAnalysisResponse): Frame analysis results for a representative frame of the signal.
    """
    
    duration: float
    averagePitch: float
    fileSize: int
    fileCreationDate: datetime
    frame: FrameAnalysisResponse

class VowelSpaceResponse(BaseModel):
    """
    VowelSpaceResponse model representing formant location in the vowel space.

    Attributes:
        f1 (float): First formant frequency (in Hz).
        f2 (float): Second formant frequency (in Hz).
    """
    
    f1: float
    f2: float

class TranscriptionSegment(BaseModel):
    """
    TranscriptionSegment model representing a segment of a signal transcription.

    Attributes:
        value (str): Textual content of the segment.
        start (float): Starting time (in seconds) of the segment.
        end (float): Ending time (in seconds) of the segment.
    """
    
    value: str
    start: float
    end: float