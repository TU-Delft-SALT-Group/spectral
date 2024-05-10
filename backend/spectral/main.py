from fastapi import FastAPI, HTTPException
from .frame_analysis import *
from pydantic import BaseModel

app = FastAPI()

class Frame(BaseModel):
    data: list = []
    fs: float

@app.post("/frames/analyze")
async def frame_fundamental_features(frame: Frame):
    try:
        duration = calculate_frame_duration(frame=frame.data,fs=frame.fs)
        pitch = calculate_frame_pitch(frame=frame.data,fs=frame.fs)
        formants = calculate_frame_f1_f2(frame=frame.data,fs=frame.fs)
        return {"duration":duration,"pitch":pitch,"f1":formants[0],"f2":formants[1]}
    except:
        raise HTTPException(status_code=400, detail="Input data did not meet requirements")