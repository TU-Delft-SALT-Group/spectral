"""Main source file; contains the basic FastAPI setup."""

from __future__ import annotations

import os
from typing import Annotated, Any, Literal, Self, Union

import orjson
from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse

from .data_objects import (
    ErrorRateResponse,
    FileStateBody,
    GeneratedTranscriptionsModel,
    SimpleInfoResponse,
    SpectrogramResponse,
    TranscriptionSegment,
    TranscriptionsTextgridModel,
    VowelSpaceResponse,
    WaveformResponse,
)
from .database import Database
from .mode_handler import (
    convert_to_wav,
    error_rate_mode,
    simple_info_mode,
    spectrogram_mode,
    transcription_mode,
    vowel_space_mode,
    waveform_mode,
)
from .response_examples import (
    signal_modes_response_examples,
    transcription_response_examples,
)
from .transcription.textgrid import convert_to_textgrid
from .transcription.transcription import get_transcription
from .types import FileStateType


def get_db():  # pragma: no cover # noqa
    db = None
    try:
        user = os.getenv("POSTGRES_USER", "user")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        dbname = os.getenv("POSTGRES_DB", "postgres")

        db = Database(user, password, host, port, dbname)
        db.connection()
        yield db
    finally:
        if db is not None:
            db.close()


class ORJSONResponse(JSONResponse):
    """Custom JSONResponse class using ORJSON to handle nan's."""

    media_type = "application/json"

    def render(self: Self, content: Any) -> bytes:
        """Process the content, converting it into bytes."""
        return orjson.dumps(content)


app: FastAPI = FastAPI(default_response_class=ORJSONResponse, root_path="/api")


@app.post(
    "/signals/modes/{mode}",
    response_model=Union[
        None,
        SimpleInfoResponse,
        VowelSpaceResponse,
        list[list[TranscriptionSegment]],
        ErrorRateResponse,
        WaveformResponse,
        SpectrogramResponse,
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
    file_state_body: FileStateBody,
    database=Depends(get_db),
) -> Any:
    """
    Analyze an audio signal in different modes.

    This endpoint fetches an audio file from the database and performs the analysis
    based on the specified mode.

    Parameters
    ----------
    - mode (str): The analysis mode (e.g., "simple-info", "spectrogram", "wave-form",
                  "vowel-space", "transcription", "error-rate").
    - fileState (dict): The important state data of the file

    Returns
    -------
    - dict: The result of the analysis based on the selected mode.

    Raises
    ------
    - HTTPException: If the mode is not found or input data is invalid.

    """
    db_session = database
    file_state: FileStateType = file_state_body.fileState
    if mode == "simple-info":
        return simple_info_mode(db_session, file_state)
    if mode == "spectrogram":
        return spectrogram_mode(db_session, file_state)
    if mode == "waveform":
        return waveform_mode(db_session, file_state)
    if mode == "vowel-space":
        return vowel_space_mode(db_session, file_state)
    if mode == "transcription":
        return transcription_mode(db_session, file_state)
    if mode == "error-rate":
        return error_rate_mode(db_session, file_state)


@app.get(
    "/transcription/{model}/{file_id}/{api_key}",
    response_model=GeneratedTranscriptionsModel,
    responses=transcription_response_examples,
)
async def transcribe_file(
    model: Annotated[
        Literal["whisper", "deepgram", "allosaurus", "whisper-torgo-1-epoch"],
        Path(title="The transcription model"),
    ],
    file_id: Annotated[str, Path(title="The ID of the file")],
    api_key: Annotated[str, Path(title="The key for the model")],
    database=Depends(get_db),
) -> Any:
    """
    Transcribe an audio file.

    This endpoint transcribes an audio file using the specified model.

    Parameters
    ----------
    - model (str): The transcription model to use.
    - file_id (str): The ID of the file to transcribe.

    Returns
    -------
    - list: A list of dictionaries with keys 'start', 'end' and 'value' containing the
            transcription of the audio file.

    Raises
    ------
    - HTTPException: If the file is not found or an error occurs during
                     transcription or storing the transcription.

    """
    db_session = database
    try:
        file = db_session.fetch_file(file_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found") from e

    file["data"] = convert_to_wav(file["data"])

    return get_transcription(model, file, api_key)


@app.post(
    "/transcription/textgrid",
    response_model=Any,
)
async def to_textgrid(transcriptions: TranscriptionsTextgridModel):
    """Convert some transcriptions to textgrid."""
    return convert_to_textgrid(transcriptions)
