from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from fastapi import HTTPException
from jiwer import wer, cer, process_words, process_characters, visualize_alignment
import os

def calculate_error_rates(reference, annotations):
    
    hypothesis = annotation_to_hypothesis(annotations)
    
    word_level = word_level_processing(reference, hypothesis)
    character_level = character_level_processing(reference, hypothesis) 
        
    return {"wordLevel": word_level, "characterLevel": character_level}

def annotation_to_hypothesis(annotations):
    
    res = ""
    
    if len(annotations) == 0:
        return res
    
    for annotation in annotations:
        res += annotation["value"] + " "
        
    return res[:len(res)-1]
    
def word_level_processing(reference, hypothesis):
    
    processed_data = process_words(reference=reference, hypothesis=hypothesis)
    
    result = {}
    
    result["wer"] = processed_data.wer
    result["mer"] = processed_data.mer
    result["wil"] = processed_data.wil
    result["wip"] = processed_data.wip
    result["hits"] = processed_data.hits
    result["substitutions"] = processed_data.substitutions
    result["insertions"] = processed_data.insertions
    result["deletions"] = processed_data.deletions
    result["reference"] = processed_data.references[0]
    result["hypothesis"] = processed_data.hypotheses[0]
    result["alignments"] = get_alignments(processed_data.alignments[0])
    
    return result
    
def character_level_processing(reference, hypothesis):
    
    processed_data = process_characters(reference=reference, hypothesis=hypothesis)
    
    result = {}
    result["cer"] = processed_data.cer
    result["hits"] = processed_data.hits
    result["substitutions"] = processed_data.substitutions
    result["insertions"] = processed_data.insertions
    result["deletions"] = processed_data.deletions
    result["alignments"] = get_alignments(processed_data.alignments[0])
    
    return result

def get_alignments(unparsed_alignments):
    
    alignments = []
    
    for alignment in unparsed_alignments:
        alignment_dict = {}
        alignment_dict["type"] = alignment.type
        alignment_dict["referenceStartIndex"] = alignment.ref_start_idx
        alignment_dict["referenceEndIndex"] = alignment.ref_end_idx
        alignment_dict["hypothesisStartIndex"] = alignment.hyp_start_idx
        alignment_dict["hypothesisEndIndex"] = alignment.hyp_end_idx
        alignments.append(alignment_dict)
        
    return alignments 
        
def get_transcription(model, file):
    """
    Get transcription of an audio file using the specified model.

    This function gets the transcription of an audio file using the specified model.

    Parameters:
    - model (str): The transcription model to use.
    - file (dict): The file object containing the audio data.

    Returns:
    - list: A list of transcriptions containing words with their start and end times.

    Raises:
    - HTTPException: If the specified model is not found.
    """
    if model == "deepgram":
        return deepgram_transcription(file["data"])
    raise HTTPException(status_code=404, detail="Model was not found")


def deepgram_transcription(data):
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
