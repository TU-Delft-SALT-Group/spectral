"""All the mode orchestration functionality and some conversion related stuff."""

from __future__ import annotations

import subprocess
import tempfile
from typing import Any

from fastapi import HTTPException

from .error_rates import calculate_error_rates
from .frame_analysis import (
    calculate_frame_f1_f2,
    get_matching_captions,
    simple_frame_info,
    validate_frame_index,
)
from .signal_analysis import (
    calculate_sound_f1_f2,
    calculate_sound_formants_for_spectrogram,
    calculate_sound_pitch,
    get_audio,
    signal_to_sound,
    simple_signal_info,
)
from .types import DatabaseType, FileStateType


def simple_info_mode(
    database: DatabaseType,
    file_state: FileStateType,
) -> dict[str, Any]:
    """
    Extract and return basic information about a signal and its corresponding frame.

    This function combines the signal information, file metadata, and frame-specific details.

    Parameters
    ----------
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including frame indices.

    Returns
    -------
    - dict: A dictionary containing the combined signal information, file size, file creation date,
            and frame information. If the frame index is invalid, it still includes the basic file
            information.

    Example:
    ```python
    result = simple_info_mode(database, file_state)
    ```

    """
    file = get_file(database, file_state)

    audio = get_audio(file)

    result = simple_signal_info(audio)
    result["fileSize"] = len(file["data"])
    result["fileCreationDate"] = file["creationTime"]

    frame_index = validate_frame_index(audio.get_array_of_samples(), file_state)

    result["frame"] = simple_frame_info(
        audio.get_array_of_samples(),
        audio.frame_rate,
        frame_index,
    )

    return result


def spectrogram_mode(database: DatabaseType, file_state: FileStateType) -> Any:
    """
    Extract first 5 formants from signal to show in spectrogram.

    Parameters
    ----------
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including frame indices.

    Returns
    -------
    - list: A list of a list with 5 formants for each frame.

    """
    file = get_file(database, file_state)
    audio = get_audio(file)
    data = audio.get_array_of_samples()
    sound = signal_to_sound(data, audio.frame_rate)

    return calculate_sound_formants_for_spectrogram(sound)


def waveform_mode(database: DatabaseType, file_state: FileStateType) -> dict[str, Any]:
    """
    Extract the pitch, f1 and f2 of multiple frames to show in waveform mode.

    Parameters
    ----------
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including frame indices.

    Returns
    -------
    - dict: A dictionary containing the found pitches and formants.

    """
    file = get_file(database, file_state)
    audio = get_audio(file)
    data = audio.get_array_of_samples()
    sound = signal_to_sound(data, audio.frame_rate)

    pitch_dict = calculate_sound_pitch(sound)
    pitch = []
    if pitch_dict is not None:
        pitch = pitch_dict["data"]
    formants_dict = calculate_sound_f1_f2(sound)
    formants = []
    if formants_dict is not None:
        formants = formants_dict["data"]
    return {"pitch": pitch, "formants": formants}


def vowel_space_mode(
    database: DatabaseType,
    file_state: FileStateType,
) -> dict[str, list[dict[str, float]]] | None:
    """
    Extract and return the first and second formants of a specified frame.

    This function calculates the first (f1) and second (f2) formants of a segment within the
    audio signal.

    Parameters
    ----------
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including frame indices.

    Returns
    -------
    - dict: A dictionary containing the first formant (f1) and the second formant (f2).
    - Returns None if the frame index is invalid.

    Example:
    ```python
    result = vowel_space_mode(database, file_state)
    ```

    """
    file = get_file(database, file_state)
    audio = get_audio(file)
    data = audio.get_array_of_samples()
    frame_index = validate_frame_index(data, file_state)

    response = []

    if frame_index is not None:
        frame_data = data[frame_index["startIndex"] : frame_index["endIndex"]]
        formants = calculate_frame_f1_f2(frame_data, audio.frame_rate)

        response.append(
            {
                "f1": formants[0],
                "f2": formants[1],
                "matchString": None,
                "start": audio.duration_seconds * frame_index["startIndex"] / len(data),
                "end": audio.duration_seconds * frame_index["endIndex"] / len(data),
            }
        )

    for caption in get_matching_captions(file_state):
        frame_data = data[
            int(len(data) / audio.duration_seconds * caption["start"]) : int(
                len(data) / audio.duration_seconds * caption["end"]
            )
        ]
        formants = calculate_frame_f1_f2(frame_data, audio.frame_rate)
        response.append(
            {
                "f1": formants[0],
                "f2": formants[1],
                "matchString": caption["matchString"],
                "start": caption["start"],
                "end": caption["end"],
            }
        )

    return {"formants": response}


def transcription_mode(database: DatabaseType, file_state: FileStateType) -> Any:  # noqa: ARG001
    """TBD."""
    return None


def error_rate_mode(
    database: DatabaseType,  # noqa: ARG001
    file_state: FileStateType,
) -> dict[str, Any] | None:
    """
    Calculate the error rates of transcriptions against the ground truth.

    Parameters
    ----------
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including transcriptions.

    Returns
    -------
    - A dictionary with the ground truth and a list of error rates for each transcription.
    - Returns None if there are no transcriptions or if the ground truth is missing.

    Example:
    ```python
    result = error_rate_mode(database, file_state)
    ```

    """
    if (
        "reference" not in file_state
        or file_state["reference"] is None
        or "captions" not in file_state["reference"]
        or file_state["reference"]["captions"] is None
        or "hypothesis" not in file_state
        or file_state["hypothesis"] is None
        or "captions" not in file_state["hypothesis"]
        or file_state["hypothesis"]["captions"] is None
    ):
        return None

    return calculate_error_rates(
        file_state["reference"]["captions"],
        file_state["hypothesis"]["captions"],
    )


def get_file(database: DatabaseType, file_state: FileStateType) -> FileStateType:
    """
    Fetch a file from the database using the file_state information.

    Parameters
    ----------
    - database: The database object used to fetch the file.
    - file_state: A dictionary containing the state of the file, including its ID.

    Returns
    -------
    - The file object fetched from the database.

    Raises
    ------
    - HTTPException: If the 'id' is not in file_state or if the file is not found.

    Example:
    ```python
    file = get_file(database, file_state)
    ```

    """
    if "id" not in file_state:
        raise HTTPException(status_code=404, detail="file_state did not include id")
    try:
        file = database.fetch_file(file_state["id"])  # pyright: ignore[reportAttributeAccessIssue]
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found") from e

    file["data"] = convert_to_wav(file["data"])

    return file


def convert_to_wav(data: bytes) -> bytes:
    """Convert an arbitrary format recording into wav format."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_input:
        temp_input.write(data)
        temp_input.flush()  # Ensure data is written to disk
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_output:
            command = [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                temp_input.name,
                temp_output.name,
            ]
            subprocess.run(
                command,  # noqa: S603
                stdout=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                check=False,
            )
            temp_output.seek(0)  # Rewind to the beginning of the file
            return temp_output.read()
