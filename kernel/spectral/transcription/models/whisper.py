from openai import OpenAI
import os
import tempfile


def whisper_transcription(data: bytes) -> list[dict]:
    try:
        client = OpenAI(api_key=os.getenv("WHISPER_KEY"))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav.write(data)
            temp_wav_filename = temp_wav.name

        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=open(temp_wav_filename, "rb"),
            response_format="verbose_json",
            timestamp_granularities=["word"],
        )

        res = []

        if hasattr(transcription, "words"):
            words = transcription.words  # pyright: ignore[reportAttributeAccessIssue]

            for word in words:
                res.append(
                    {"value": word["word"], "start": word["start"], "end": word["end"]}
                )

        return res

    except Exception as e:
        print(f"Exception: {e}")
        return []
