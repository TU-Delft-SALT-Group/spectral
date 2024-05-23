from typing import Annotated, Optional, Union, Any
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
    spectrogram_mode,
    vowel_space_mode,
    transcription_mode,
    error_rate_mode,
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
)
from .database import Database
import orjson
import io


import os
from pydub import AudioSegment


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


@app.post("/frames/analyze", response_model=FrameAnalysisResponse, responses={
    200: {"content": {
                "application/json": {
                    "example": {
                        "duration": 0.04,
                        "pitch": 160.32,
                        "f1": 523.32,
                        "f2": 762.89     
                    }
                }
            }
          },
    400: {"content": { 
            "application/json": {
                "example": {
                    "detail": "error message"
                    }
                }
            }
        }
    })
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


@app.post("/signals/analyze", response_model= SignalAnalysisResponse, responses={
    200: {"content": {
                "application/json": {
                    "example": {
                        "duration": 4.0, 
                        "pitch": {
                            "time_step": 0.002,
                            "start_time": 0.99,
                            "data": [123,32]
                            }, 
                        "spectrogram":{
                            "time_step": 0.002,
                            "window_length": 0.005,
                            "frequency_step": 20.0,
                            "start_time": .99,
                            "data": [123,32] 
                            },
                        "formants":{
                            "time_step": 0.002,
                            "window_length": 0.005,
                            "start_time": .99,
                            "data": [[20,30],[40,50]]
                        }    
                    }
                }
            }
          },
    400: {"content": { 
            "application/json": {
                "example": {
                    "detail": "error message"
                    }
                }
            }
        }
    })
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


@app.get("/signals/modes/{mode}/{id}", response_model=Union[Any,None,SimpleInfoResponse,VowelSpaceResponse,list[list[TranscriptionSegment]]], responses={
    200: {"content": {
                "application/json": {
                    "examples": {
                        "simple-info": {
                            "summary": "Example for simple-info mode",
                            "value": {
                                "duration": 2.12,
                                "averagePitch": 30.2,
                                "fileSize": 123456,
                                "fileCreationDate": "2024-05-21T09:58:42.263896",
                                "frame": {
                                    "duration": 0.04,
                                    "pitch": 200.2,
                                    "f1": 400.56,
                                    "f2": 800.98
                                }
                            }
                        },
                        "spectrogram": {
                            "summary": "Example for spectrogram mode",
                            "value": "null (actual null value, fastapi currently doesn't support examples with just null)"
                        },
                        "waveform": {
                            "summary": "Example for waveform mode",
                            "value": "null (actual null value, fastapi currently doesn't support examples with just null)"
                        },
                        "vowel-space": {
                            "summary": "Example for vowel-space mode",
                            "value": {
                                "f1": 400.56,
                                "f2": 800.98
                            }
                        },
                        "transcription": {
                            "summary": "Example for transcription mode",
                            "value": [[
                                {"value": "foo", "start": 0, "end": 0.12},
                                {"value": "bar", "start": 0.12, "end": 0.24}
                                ]]
                        }
                    }
                }
            }
        }, 
    400: {"content": { 
            "application/json": {
                "example": {
                    "detail": "error message"
                    }
                }
            }
        }, 
    404: {"content": { 
            "application/json": {
                "example": {
                    "detail": "error message"
                    }
                }
            }
        }
    })
async def analyze_signal_mode(
    mode: Annotated[str, Path(title="The analysis mode")],
    id: Annotated[str, Path(title="The ID of the signal")],
    startIndex: Optional[int] = None,
    endIndex: Optional[int] = None,
    database=Depends(get_db),
):
    """
    Analyze an audio signal in different modes.

    This endpoint fetches an audio file from the database and performs the analysis based on the specified mode.

    Parameters:
    - mode (str): The analysis mode (e.g., "simple-info", "spectrogram", "wave-form", "vowel-space", "transcription").
    - id (str): The ID of the signal to analyze.
    - startIndex (Optional[int]): The start index of the frame to analyze.
    - endIndex (Optional[int]): The end index of the frame to analyze.

    Returns:
    - dict: The result of the analysis based on the selected mode.

    Raises:
    - HTTPException: If the mode is not found or input data is invalid.
    """
    try:
        file = database.fetch_file(id)
    except Exception as _:
        raise HTTPException(status_code=404, detail="File not found")

    audio = AudioSegment.from_file(io.BytesIO(file["data"]))
    fs = audio.frame_rate
    data = audio.get_array_of_samples()
    frame_index = validate_frame_index(data, startIndex, endIndex)

    if mode == "simple-info":
        return simple_info_mode(data, fs, file, frame_index)
    if mode == "spectrogram":
        return spectrogram_mode(data, fs, frame_index)
    if mode == "waveform":
        return None
    if mode == "vowel-space":
        return vowel_space_mode(data, fs, frame_index)
    if mode == "transcription":
        return transcription_mode(id, database)
    if mode == "error-rate":
        return error_rate_mode(id, database, file)
    raise HTTPException(status_code=400, detail="Mode not found")


@app.get("/transcription/{model}/{id}", response_model=list[TranscriptionSegment], responses={
    200: {"content": {
                "application/json": {
                    "example": [{"value": "foo", "start": 0, "end": 0.12},{"value": "bar", "start": 0.12, "end": 0.24}]
                }
            }
          }, 
    404: {"content": { 
            "application/json": {
                "example": {
                    "detail": "error message"
                    }
                }
            }
        }, 
    500: {"content": { 
            "application/json": {
                "example": {
                    "detail": "error message"
                    }
                }
            }
        }
    })
async def transcribe_file(
    model: Annotated[str, Path(title="The transcription model")],
    id: Annotated[str, Path(title="The ID of the file")],
    # startIndex: Optional[int] = None,
    # endIndex: Optional[int] = None,
    database=Depends(get_db),
):
    """
    Transcribe an audio file.

    This endpoint transcribes an audio file using the specified model.

    Parameters:
    - model (str): The transcription model to use.
    - id (str): The ID of the file to transcribe.

    Returns:
    - list: A list of dictionaries with keys 'start', 'end' and 'value' containing the transcription of the audio file.

    Raises:
    - HTTPException: If the file is not found or an error occurs during transcription or storing the transcription.
    """
    try:
        file = database.fetch_file(id)
    except Exception as _:
        raise HTTPException(status_code=404, detail="File not found")
    transcription = get_transcription(model, file)
    try:
        database.store_transcription(id, transcription)
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while storing the transcription",
        )
    return transcription


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
