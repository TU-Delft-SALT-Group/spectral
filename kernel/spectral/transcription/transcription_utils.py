from ..signal_analysis import get_audio, calculate_signal_duration
from ..types import FileStateType


def fill_gaps(transcriptions: list[dict], file: FileStateType) -> list[dict]:
    """Fill the gaps between consegutive transcription dictionaries such that all time is accounted for

    Args:
        transcriptions (list[dict]): list of transcriptions with possible gaps in time
        file (FileStateType): The state of the file that is being transcribed

    Returns:
        list[dict]: list of transcriptions with gaps filled with empty strings.
    """
    res = []

    audio = get_audio(file)
    duration = calculate_signal_duration(audio)

    if len(transcriptions) == 0:
        return [{"value": "", "start": 0, "end": duration}]

    time = 0

    for transcription in transcriptions:
        if time != transcription["start"]:
            res.append({"value": "", "start": time, "end": transcription["start"]})
        time = transcription["end"]
        res.append(transcription)

    if time != duration:
        res.append({"value": "", "start": time, "end": duration})

    return res
