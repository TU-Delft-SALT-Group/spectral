from collections.abc import Iterator

import parselmouth
from pydantic import BaseModel
from pydub import AudioSegment

from .database import Database

# type definitions
AudioType = AudioSegment
SoundType = parselmouth.Sound
FileStateType = dict
DatabaseType = Database | Iterator[Database]


class FileStateBody(BaseModel):
    fileState: dict
