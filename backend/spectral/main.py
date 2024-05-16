from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from .signal_analysis import (
    calculate_signal_duration,
    calculate_sound_pitch,
    calculate_sound_spectrogram,
    calculate_sound_f1_f2,
    signal_to_sound,
)
from .frame_analysis import (
    calculate_frame_duration,
    calculate_frame_pitch,
    calculate_frame_f1_f2,
)
from .data_objects import Frame, Signal
from .database import Database
import orjson
from scipy.io import wavfile as wv
from .mode_handler import simple_info_mode, spectogram_mode, vowel_space_mode
import io
import os

database = Database(
    os.getenv("POSTGRES_USER"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_HOST"),
    os.getenv("POSTGRES_PORT"),
    os.getenv("POSTGRES_DB"),
)


class ORJSONResponse(JSONResponse):
    """
    Custom JSONResponse class using ORJSON to handle nan's.
    """

    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content)


app: FastAPI = FastAPI(default_response_class=ORJSONResponse, root_path="/api")


@app.post("/frames/analyze")
async def frame_fundamental_features(frame: Frame):
    """
    Analyze fundamental features of an audio frame.

    This endpoint calculates the duration, pitch, and formants (f1, f2) of the provided audio frame.

    Parameters:
    - frame (Frame): Frame object containing the data and sample frequency of the audio frame.

    Returns:
    - dict: A dictionary containing the duration, pitch, f1, and f2 of the frame.

    Raises:
    - HTTPException: If the input data does not meet requirements.
    """
    try:
        duration = calculate_frame_duration(frame=frame.data, fs=frame.fs)
        pitch = calculate_frame_pitch(frame=frame.data, fs=frame.fs)
        formants = calculate_frame_f1_f2(frame=frame.data, fs=frame.fs)
        return {
            "duration": duration,
            "pitch": pitch,
            "f1": formants[0],
            "f2": formants[1],
        }
    except Exception as _:
        raise HTTPException(
            status_code=400, detail="Input data did not meet requirements"
        )


@app.post("/signals/analyze")
async def signal_fundamental_features(signal: Signal):
    """
    Analyze fundamental features of an audio signal.

    This endpoint calculates the duration, pitch, spectrogram, and formants of the provided audio signal.

    Parameters:
    - signal (Signal): Signal object containing the data, sample frequency, and optional analysis parameters.

    Returns:
    - dict: A dictionary containing the duration, pitch, spectrogram, and formants of the signal.

    Raises:
    - HTTPException: If the input data does not meet requirements.
    """
    try:
        sound = signal_to_sound(signal.data, signal.fs)
        duration = calculate_signal_duration(signal.data, signal.fs)
        pitch = calculate_sound_pitch(sound, time_step=signal.pitch_time_step)
        spectrogram = calculate_sound_spectrogram(
            sound,
            time_step=signal.spectogram_time_step,
            window_length=signal.spectogram_window_length,
            frequency_step=signal.spectogram_frequency_step,
        )
        formants = calculate_sound_f1_f2(
            sound,
            time_step=signal.formants_time_step,
            window_length=signal.formants_window_length,
        )
        return {
            "duration": duration,
            "pitch": pitch,
            "spectogram": spectrogram,
            "formants": formants,
        }
    except Exception as _:
        raise HTTPException(
            status_code=400, detail="Input data did not meet requirements"
        )


@app.get("/signals/modes/{mode}/{id}")
async def analyze_signal_mode(
    mode: Annotated[str, Path(title="The analysis mode")],
    id: Annotated[str, Path(title="The ID of the signal")],
    startIndex: Optional[int] = None,
    endIndex: Optional[int] = None,
):
    """
    Analyze an audio signal in different modes.

    This endpoint fetches an audio file from the database and performs the analysis based on the specified mode.

    Parameters:
    - mode (str): The analysis mode (e.g., "simple-info", "spectogram", "vowel-space").
    - id (str): The ID of the signal to analyze.
    - startIndex (Optional[int]): The start index of the frame to analyze.
    - endIndex (Optional[int]): The end index of the frame to analyze.

    Returns:
    - dict: The result of the analysis based on the selected mode.

    Raises:
    - HTTPException: If the mode is not found or input data is invalid.
    """
    file = database.fetch_file(id)
    fs, data = wv.read(io.BytesIO(file["data"]))
    frame_index = validate_frame_index(data, startIndex, endIndex)
    match mode:
        case "simple-info":
            return simple_info_mode(data, fs, file, frame_index)
        case "spectogram":
            return spectogram_mode(data, fs, frame_index)
        case "vowel-space":
            return vowel_space_mode(data, fs, frame_index)
        case _:
            raise HTTPException(status_code=400, detail="Mode not found")


def validate_frame_index(data, start_index, end_index):
    """
    Validates a frame index for a segment of the audio data and creates a dictionary for those values.

    Parameters:
    - data (list of int): The audio signal data.
    - start_index (int): The start index of the frame.
    - end_index (int): The end index of the frame.

    Returns:
    - dict: A dictionary containing the startIndex and endIndex.

    Raises:
    - HTTPException: If the startIndex or endIndex are invalid.

    Example:
    ```python
    frame_index = create_frame_index(data, 0, 100)
    ```
    """
    if start_index is None and end_index is None:
        return None
    if start_index is None:
        raise HTTPException(status_code=400, detail="no startIndex provided")
    if end_index is None:
        raise HTTPException(status_code=400, detail="no endIndex provided")
    if start_index >= end_index:
        raise HTTPException(
            status_code=400, detail="startIndex should be strictly lower than endIndex"
        )
    if start_index < 0:
        raise HTTPException(
            status_code=400, detail="startIndex should be larger or equal to 0"
        )
    if end_index > len(data):
        raise HTTPException(
            status_code=400, detail="endIndex should be lower than the file length"
        )
    return {"startIndex": start_index, "endIndex": end_index}
