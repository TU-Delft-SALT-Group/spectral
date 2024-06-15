"""Everything related to textgrid format."""

import tempfile
from pathlib import Path

import mytextgrid


def convert_to_textgrid(transcriptions):
    """
    Convert transcriptions of file to textgrid format.

    Args:
    ----
        transcriptions (_type_): list of tracks with transcriptions

    Returns:
    -------
        _type_: string representing a textgrid file

    """
    if len(transcriptions.transcriptions) == 0:
        return None
    tg = mytextgrid.create_textgrid(
        xmax=transcriptions.transcriptions[0].captions[-1].end,
    )
    for transcription in transcriptions.transcriptions:
        tier = tg.insert_tier(transcription.name)
        times = [
            transcription.captions[index].end for index in range(len(transcription.captions) - 1)
        ]
        tier.insert_boundaries(*times)  # pyright: ignore[reportAttributeAccessIssue]
        for index in range(len(transcription.captions)):
            tier.set_text_at_index(index, transcription.captions[index].value)  # pyright: ignore[reportAttributeAccessIssue]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".TextGrid",
        mode="w",
    ) as tmp_file:
        tg.write(tmp_file.name)
        file_name = tmp_file.name

    with Path(file_name).open("r") as file:
        return file.read()
