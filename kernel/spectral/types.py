import parselmouth
from collections.abc import Iterator
from .database import Database
from pydub import AudioSegment
from pydantic import BaseModel

# type definitions
AudioType = AudioSegment
SoundType = parselmouth.Sound
FileStateType = dict
DatabaseType = Database | Iterator[Database]


class FileStateBody(BaseModel):
    fileState: dict
