import parselmouth
from pydub import AudioSegment

try:
    from beartype.claw import beartype_this_package

    beartype_this_package()
except ImportError:
    # in case beartype is not installed: running in production
    pass


# type definitions
AudioType = AudioSegment
SoundType = parselmouth.Sound
FileStateType = dict
