from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import os


def deepgram_transcription(data: bytes) -> list[dict]:
    """
    Transcribe audio data using Deepgram API.

    This function transcribes audio data using the Deepgram API.

    Parameters:
    - data (bytes): The audio data to transcribe.

    Returns:
    - list: A list of transcriptions containing words with their start and end times.

    Raises:
    - Exception: If an error occurs during the transcription process.
    """
    try:
        # STEP 1: Create a Deepgram client using the API key
        key = os.getenv("DG_KEY")
        deepgram = None
        if key is None:
            raise Exception("No API key for Deepgram is found")
        else:
            deepgram = DeepgramClient(key)

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
            res.append(
                {"value": word["word"], "start": word["start"], "end": word["end"]}
            )
        return res

    except Exception as e:
        print(f"Exception: {e}")
        return []