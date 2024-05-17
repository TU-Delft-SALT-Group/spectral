from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from fastapi import HTTPException
import os

def get_transcription(model, file):
    match model:
        case "deepgram":
            return deepgram_transcription(file["data"])
        case _:
            raise HTTPException(
                status_code=404, detail="Model was not found"
            )
            

def deepgram_transcription(data):
    try:
        # STEP 1: Create a Deepgram client using the API key
        print(os.getenv("DG_KEY"))
        deepgram = DeepgramClient(os.getenv("DG_KEY"))

        payload: FileSource = {
            "buffer": data,
        }

        # STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            profanity_filter=False,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        
        res = []
        for word in response["results"]["channels"][0]["alternatives"][0]["words"]:
            res.append({"value":word["word"],"start":word["start"],"end":word["end"]})
        return res

    except Exception as e:
        print(f"Exception: {e}")