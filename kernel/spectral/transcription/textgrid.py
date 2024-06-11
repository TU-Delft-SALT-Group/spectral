import mytextgrid
import tempfile


def convert_to_textgrid(transcriptions):
    if len(transcriptions.transcriptions) == 0:
        return None
    tg = mytextgrid.create_textgrid(
        xmax=transcriptions.transcriptions[0].captions[-1].end
    )
    for transcription in transcriptions.transcriptions:
        tier = tg.insert_tier(transcription.name)
        times = []
        for index in range(len(transcription.captions) - 1):
            times.append(transcription.captions[index].end)
        tier.insert_boundaries(*times)  # pyright: ignore[reportAttributeAccessIssue]
        for index in range(len(transcription.captions)):
            print(transcription.captions[index])
            tier.set_text_at_index(index, transcription.captions[index].value)  # pyright: ignore[reportAttributeAccessIssue]

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".TextGrid", mode="w"
    ) as tmp_file:
        tg.write(tmp_file.name)
        file_name = tmp_file.name

    with open(file_name, "r") as file:
        data = file.read()
    return data
