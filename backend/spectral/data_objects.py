from pydantic import BaseModel
from typing import Optional

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