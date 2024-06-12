"""All the types, that are reused throughout the Spectral."""

from collections.abc import Iterator

import parselmouth
from pydub import AudioSegment

from .database import Database

# type definitions
AudioType = AudioSegment
SoundType = parselmouth.Sound
FileStateType = dict
DatabaseType = Database | Iterator[Database]
