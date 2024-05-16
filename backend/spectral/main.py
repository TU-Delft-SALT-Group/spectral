from fastapi import FastAPI, HTTPException
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
from pydantic import BaseModel
import orjson
from typing import Optional


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content)


app: FastAPI = FastAPI(default_response_class=ORJSONResponse)


class Frame(BaseModel):
    data: list
    fs: float


class Signal(BaseModel):
    data: list
    fs: float
    pitch_time_step: Optional[float] = None
    spectogram_time_step: float = 0.002
    spectogram_window_length: float = 0.005
    spectogram_frequency_step: float = 20.0
    formants_time_step: Optional[float] = None
    formants_window_length: float = 0.025


@app.post("/frames/analyze")
async def frame_fundamental_features(frame: Frame):
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
