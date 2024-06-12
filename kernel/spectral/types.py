from collections.abc import Iterator

import parselmouth
from pydub import AudioSegment
from pydantic import BaseModel

from .database import Database

# type definitions
AudioType = AudioSegment
SoundType = parselmouth.Sound
FileStateType = dict
DatabaseType = Database | Iterator[Database]


class FileStateBody(BaseModel):
    fileState: dict
