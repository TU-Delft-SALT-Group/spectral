from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from fastapi import HTTPException
from jiwer import process_words, process_characters
import os

def calculate_error_rates(reference, annotations):
    """
    Calculate error rates between the reference transcription and annotations.

    This function calculates both word-level and character-level error rates 
    based on the provided reference transcription and annotations.

    Parameters:
    - reference (str): The reference transcription.
    - annotations (list of dict): The list of annotations where each annotation is a dictionary with a "value" key.

    Returns:
    - dict: A dictionary containing word-level and character-level error rates.

    """
    hypothesis = annotation_to_hypothesis(annotations)
    word_level = word_level_processing(reference, hypothesis)
    character_level = character_level_processing(reference, hypothesis)
    
    return {"wordLevel": word_level, "characterLevel": character_level}

def annotation_to_hypothesis(annotations):
    """
    Convert annotations to a single hypothesis string.

    This function concatenates the values from the annotations list to form a hypothesis string.

    Parameters:
    - annotations (list of dict): The list of annotations where each annotation is a dictionary with a "value" key.

    Returns:
    - str: A single concatenated hypothesis string.

    """
    res = ""
    if len(annotations) == 0:
        return res
    
    for annotation in annotations:
        res += annotation["value"] + " "
        
    return res[:len(res)-1]

def word_level_processing(reference, hypothesis):
    """
    Process word-level error metrics between the reference and hypothesis.

    This function processes word-level metrics.

    Parameters:
    - reference (str): The reference transcription.
    - hypothesis (str): The hypothesis transcription.

    Returns:
    - dict: A dictionary containing word-level error metrics and alignments.

    """
    processed_data = process_words(reference=reference, hypothesis=hypothesis)
    
    result = {
        "wer": processed_data.wer,
        "mer": processed_data.mer,
        "wil": processed_data.wil,
        "wip": processed_data.wip,
        "hits": processed_data.hits,
        "substitutions": processed_data.substitutions,
        "insertions": processed_data.insertions,
        "deletions": processed_data.deletions,
        "reference": processed_data.references[0],
        "hypothesis": processed_data.hypotheses[0],
        "alignments": get_alignments(processed_data.alignments[0])
    }
    
    return result

def character_level_processing(reference, hypothesis):
    """
    Process character-level error metrics between the reference and hypothesis.

    This function processes character-level metrics.

    Parameters:
    - reference (str): The reference transcription.
    - hypothesis (str): The hypothesis transcription.

    Returns:
    - dict: A dictionary containing character-level error metrics and alignments.

    """
    processed_data = process_characters(reference=reference, hypothesis=hypothesis)
    
    result = {
        "cer": processed_data.cer,
        "hits": processed_data.hits,
        "substitutions": processed_data.substitutions,
        "insertions": processed_data.insertions,
        "deletions": processed_data.deletions,
        "reference": processed_data.references[0],
        "hypothesis": processed_data.hypotheses[0],
        "alignments": get_alignments(processed_data.alignments[0])
    }
    
    return result

def get_alignments(unparsed_alignments):
    """
    Convert unparsed alignments into a structured format.

    This function processes unparsed alignment data and converts it into a list of dictionaries 
    with detailed alignment information.

    Parameters:
    - unparsed_alignments (list): A list of unparsed alignment objects.

    Returns:
    - list of dict: A list of dictionaries where each dictionary contains alignment information.

    """
    alignments = []
    
    for alignment in unparsed_alignments:
        alignment_dict = {
            "type": alignment.type,
            "referenceStartIndex": alignment.ref_start_idx,
            "referenceEndIndex": alignment.ref_end_idx,
            "hypothesisStartIndex": alignment.hyp_start_idx,
            "hypothesisEndIndex": alignment.hyp_end_idx
        }
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
