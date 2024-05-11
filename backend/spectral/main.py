from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .frame_analysis import (
    calculate_frame_duration,
    calculate_frame_pitch,
    calculate_frame_f1_f2,
)
from pydantic import BaseModel
import orjson


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content) -> bytes:
        return orjson.dumps(content)


app = FastAPI(default_response_class=ORJSONResponse)


class Frame(BaseModel):
    data: list
    fs: float


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
