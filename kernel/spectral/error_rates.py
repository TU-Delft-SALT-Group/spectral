"""All the functionality related to computing errors between transcriptions."""

from __future__ import annotations

from typing import Any

import jiwer
from jiwer import process_characters, process_words


def calculate_error_rates(
    reference_annotations: list[dict],
    hypothesis_annotations: list[dict],
) -> dict | None:
    """
    Calculate error rates between the reference transcription and annotations.

    This function calculates both word-level and character-level error rates
    based on the provided reference transcription and annotations.

    Parameters
    ----------
    - reference_annotations: The reference transcription.
    - hypothesis_annotations: The list of annotations where each annotation is a
    dictionary with a "value" key.

    Returns
    -------
    - dict: A dictionary containing word-level and character-level error rates.

    """
    reference = annotation_to_sentence(reference_annotations)
    if reference == "":
        return None
    hypothesis = annotation_to_sentence(hypothesis_annotations)
    word_level = word_level_processing(reference, hypothesis)
    character_level = character_level_processing(reference, hypothesis)

    return {"wordLevel": word_level, "characterLevel": character_level}


def word_level_processing(reference: str, hypothesis: str) -> dict[str, Any]:
    """
    Process word-level error metrics between the reference and hypothesis.

    This function processes word-level metrics.

    Parameters
    ----------
    - reference (str): The reference transcription.
    - hypothesis (str): The hypothesis transcription.

    Returns
    -------
    - dict: A dictionary containing word-level error metrics and alignments.

    """
    processed_data = process_words(reference=reference, hypothesis=hypothesis)
    return {
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
        "alignments": get_alignments(processed_data.alignments[0]),
    }


def character_level_processing(reference: str, hypothesis: str) -> dict[str, Any]:
    """
    Process character-level error metrics between the reference and hypothesis.

    This function processes character-level metrics.

    Parameters
    ----------
    - reference (str): The reference transcription.
    - hypothesis (str): The hypothesis transcription.

    Returns
    -------
    - dict: A dictionary containing character-level error metrics and alignments.

    """
    processed_data = process_characters(reference=reference, hypothesis=hypothesis)

    return {
        "cer": processed_data.cer,
        "hits": processed_data.hits,
        "substitutions": processed_data.substitutions,
        "insertions": processed_data.insertions,
        "deletions": processed_data.deletions,
        "reference": processed_data.references[0],
        "hypothesis": processed_data.hypotheses[0],
        "alignments": get_alignments(processed_data.alignments[0]),
    }


def annotation_to_sentence(annotations: list) -> str:
    """
    Convert annotations to a single hypothesis string.

    This function concatenates the values from the annotations list to form a hypothesis string.

    Parameters
    ----------
    - annotations (list of dict): The list of annotations where each annotation is a dictionary
    with a "value" key.

    Returns
    -------
    - str: A single concatenated hypothesis string.

    """
    res = ""
    if len(annotations) == 0:
        return res

    for annotation in annotations:
        if annotation["value"] == "":
            continue
        res += annotation["value"] + " "

    return res[: len(res) - 1]


def get_alignments(
    unparsed_alignments: list[jiwer.process.AlignmentChunk],
) -> list[dict]:
    """
    Convert unparsed alignments into a structured format.

    This function processes unparsed alignment data and converts it into a list of dictionaries
    with detailed alignment information.

    Parameters
    ----------
    - unparsed_alignments (list): A list of unparsed alignment objects.

    Returns
    -------
    - list of dict: A list of dictionaries where each dictionary contains alignment information.

    """
    alignments = []

    for alignment in unparsed_alignments:
        alignment_dict = {
            "type": alignment.type,
            "referenceStartIndex": alignment.ref_start_idx,
            "referenceEndIndex": alignment.ref_end_idx,
            "hypothesisStartIndex": alignment.hyp_start_idx,
            "hypothesisEndIndex": alignment.hyp_end_idx,
        }
        alignments.append(alignment_dict)

    return alignments
