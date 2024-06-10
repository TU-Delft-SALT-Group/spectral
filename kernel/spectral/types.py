import parselmouth
from collections.abc import Iterator
from .database import Database
from pydub import AudioSegment

# type definitions
AudioType = AudioSegment
SoundType = parselmouth.Sound
FileStateType = dict
DatabaseType = Database | Iterator[Database]
