from typing import Annotated, Union, Literal
from fastapi import FastAPI, HTTPException, Path, Depends
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
from .mode_handler import (
    simple_info_mode,
    waveform_mode,
    spectrogram_mode,
    vowel_space_mode,
    transcription_mode,
    error_rate_mode,
)
from .response_examples import (
    frame_analysis_response_examples,
    signal_analysis_response_examples,
    signal_modes_response_examples,
    transcription_response_examples,
)
from .transcription import get_transcription
from .data_objects import (
    Frame,
    Signal,
    FrameAnalysisResponse,
    SignalAnalysisResponse,
    SimpleInfoResponse,
    VowelSpaceResponse,
    TranscriptionSegment,
    ErrorRateResponse,
)
from .database import Database
import orjson
import json
import os


def get_db():  # pragma: no cover
    db = None
    try:
        db = Database(
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_HOST"),
            os.getenv("POSTGRES_PORT"),
            os.getenv("POSTGRES_DB"),
        )
        db.connection()
        yield db
    finally:
        if db is not None:
            db.close()


class ORJSONResponse(JSONResponse):
    """
    Custom JSONResponse class using ORJSON to handle nan's.
    """

    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content)


app: FastAPI = FastAPI(default_response_class=ORJSONResponse, root_path="/api")


@app.post(
    "/frames/analyze",
    response_model=FrameAnalysisResponse,
    responses=frame_analysis_response_examples,
)
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


@app.post(
    "/signals/analyze",
    response_model=SignalAnalysisResponse,
    responses=signal_analysis_response_examples,
)
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
            time_step=signal.spectrogram_time_step,
            window_length=signal.spectrogram_window_length,
            frequency_step=signal.spectrogram_frequency_step,
        )
        formants = calculate_sound_f1_f2(
            sound,
            time_step=signal.formants_time_step,
            window_length=signal.formants_window_length,
        )
        return {
            "duration": duration,
            "pitch": pitch,
            "spectrogram": spectrogram,
            "formants": formants,
        }
    except Exception as _:
        raise HTTPException(
            status_code=400, detail="Input data did not meet requirements"
        )


@app.get(
    "/signals/modes/{mode}",
    response_model=Union[
        None,
        SimpleInfoResponse,
        VowelSpaceResponse,
        list[list[TranscriptionSegment]],
        ErrorRateResponse,
    ],
    responses=signal_modes_response_examples,
)
async def analyze_signal_mode(
    mode: Annotated[
        Literal[
            "simple-info",
            "spectrogram",
            "waveform",
            "vowel-space",
            "transcription",
            "error-rate",
        ],
        Path(title="The analysis mode"),
    ],
    fileState,
    database=Depends(get_db),
):
    """
    Analyze an audio signal in different modes.

    This endpoint fetches an audio file from the database and performs the analysis based on the specified mode.

    Parameters:
    - mode (str): The analysis mode (e.g., "simple-info", "spectrogram", "wave-form", "vowel-space", "transcription", "error-rate").
    - fileState (dict): The important state data of the file

    Returns:
    - dict: The result of the analysis based on the selected mode.

    Raises:
    - HTTPException: If the mode is not found or input data is invalid.
    """
    fileState = json.loads(fileState)

    if mode == "simple-info":
        return simple_info_mode(database, fileState)
    if mode == "spectrogram":
        return spectrogram_mode(database, fileState)
    if mode == "waveform":
        return waveform_mode(database, fileState)
    if mode == "vowel-space":
        return vowel_space_mode(database, fileState)
    if mode == "transcription":
        return transcription_mode(database, fileState)
    if mode == "error-rate":
        return error_rate_mode(database, fileState)


@app.get(
    "/transcription/{model}/{session_id}/{file_id}",
    response_model=list[TranscriptionSegment],
    responses=transcription_response_examples,
)
async def transcribe_file(
    model: Annotated[str, Path(title="The transcription model")],
    session_id: Annotated[str, Path(title="The ID of the file")],
    file_id: Annotated[str, Path(title="The ID of the file")],
    database=Depends(get_db),
):
    """
    Transcribe an audio file.

    This endpoint transcribes an audio file using the specified model.

    Parameters:
    - model (str): The transcription model to use.
    - file_id (str): The ID of the file to transcribe.
    - session_id (str): The ID of the session to which the file belongs

    Returns:
    - list: A list of dictionaries with keys 'start', 'end' and 'value' containing the transcription of the audio file.

    Raises:
    - HTTPException: If the file is not found or an error occurs during transcription or storing the transcription.
    """
    try:
        file = database.fetch_file(file_id)
    except Exception as _:
        raise HTTPException(status_code=404, detail="File not found")
    transcription = get_transcription(model, file)
    return transcription
