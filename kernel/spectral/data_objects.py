"""Contains all the Pydantic specifications for the requests received by FastAPI server."""

# ruff: noqa: N815
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class FrameAnalysisResponse(BaseModel):
    """
    FrameAnalysisResponse model representing the results of frame analysis.

    Attributes
    ----------
        duration (float): Duration (in seconds) of the frame.
        pitch (float): Fundamental frequency (F0) of the frame (in Hz).
        f1 (float): First formant frequency of the frame (in Hz).
        f2 (float): Second formant frequency of the frame (in Hz).

    """

    duration: float
    pitch: float
    f1: float
    f2: float


class SimpleInfoResponse(BaseModel):
    """
    SimpleInfoResponse model containing basic information about a signal.

    Attributes
    ----------
        duration (float): Duration (in seconds) of the signal.
        averagePitch (float): Average pitch (F0) of the signal (in Hz).
        fileSize (int): File size of the signal data (in bytes).
        fileCreationDate (datetime): Date and time the signal file was created.
        frame (FrameAnalysisResponse): Frame analysis results for a representative frame of
                                       the signal.

    """

    duration: float
    averagePitch: float
    fileSize: int
    fileCreationDate: datetime
    frame: FrameAnalysisResponse | None


class Formants(BaseModel):
    """
    Formants model representing formant location in the vowel space.

    Attributes
    ----------
        f1 (float): First formant frequency (in Hz).
        f2 (float): Second formant frequency (in Hz).

    """

    f1: float
    f2: float


class VowelSpaceResponse(BaseModel):
    """
    VowelSpaceResponse model representing a list of formant location in the vowel space.

    Attributes
    ----------
        formants (list[Formants]): list of formants used for vowel space

    """

    formants: list[Formants]


class TranscriptionSegment(BaseModel):
    """
    TranscriptionSegment model representing a segment of a signal transcription.

    Attributes
    ----------
        value (str): Textual content of the segment.
        start (float): Starting time (in seconds) of the segment.
        end (float): Ending time (in seconds) of the segment.

    """

    value: str
    start: float
    end: float


class Alignment(BaseModel):
    """
    Alignment model representing the type and indices of the alignment.

    Attributes
    ----------
        type (Literal['insert', 'substitute', 'delete, 'equal']): Type of the alignment.
        referenceStartIndex (int): Starting index in the reference.
        referenceEndIndex (int): Ending index in the reference.
        hypothesisStartIndex (int): Starting index in the hypothesis.
        hypothesisEndIndex (int): Ending index in the hypothesis.

    """

    type: Literal["insert", "substitute", "delete", "equal"]
    referenceStartIndex: int
    referenceEndIndex: int
    hypothesisStartIndex: int
    hypothesisEndIndex: int


class WordLevelErrorRate(BaseModel):
    """
    WordLevelErrorRate model representing word-level error metrics.

    Attributes
    ----------
        wer (float): Word Error Rate.
        mer (float): Match Error Rate.
        wil (float): Word Information Lost.
        wip (float): Word Information Preserved.
        hits (int): Number of correct words.
        substitutions (int): Number of substituted words.
        insertions (int): Number of inserted words.
        deletions (int): Number of deleted words.
        reference (List[str]): List of reference words.
        hypothesis (List[str]): List of hypothesis words.
        alignments (List[Alignment]): List of alignment objects.
        bert (float): BERT score.
        jaroWinkler (float): Jaro Winkler score.

    """

    wer: float
    mer: float
    wil: float
    wip: float
    hits: int
    substitutions: int
    insertions: int
    deletions: int
    reference: list[str]
    hypothesis: list[str]
    alignments: list[Alignment]
    bert: float
    jaroWinkler: float


class CharacterLevelErrorRate(BaseModel):
    """
    CharacterLevelErrorRate model representing character-level error metrics.

    Attributes
    ----------
        cer (float): Character Error Rate.
        hits (int): Number of correct characters.
        substitutions (int): Number of substituted characters.
        insertions (int): Number of inserted characters.
        deletions (int): Number of deleted characters.
        reference (List[str]): List of reference characters.
        hypothesis (List[str]): List of hypothesis characters.
        alignments (List[Alignment]): List of alignment objects.

    """

    cer: float
    hits: int
    substitutions: int
    insertions: int
    deletions: int
    reference: list[str]
    hypothesis: list[str]
    alignments: list[Alignment]


class ErrorRateResponse(BaseModel):
    """
    ErrorRateValue model representing both word-level and character-level error metrics.

    Attributes
    ----------
        wordLevel (WordLevelErrorRate): Word-level error metrics.
        characterLevel (CharacterLevelErrorRate): Character-level error metrics.

    """

    wordLevel: WordLevelErrorRate
    characterLevel: CharacterLevelErrorRate


class SpectrogramResponse(BaseModel):
    """
    SpectrogramResponse model representing the response of the spectrogram mode endpoint.

    Attributes
    ----------
        formants (List[List[float|None]]): List of 5 formants.

    """

    formants: list[list[float | None]]


class FileStateBody(BaseModel):
    """The model of the fileState received from the frontend."""

    fileState: dict


class TranscriptionTextgridModel(BaseModel):
    """Textmodel transcription representation."""

    id: str
    name: str
    captions: list[TranscriptionSegment]


class TranscriptionsTextgridModel(BaseModel):
    """Textgrid model transcription representation."""

    transcriptions: list[TranscriptionTextgridModel]


class GeneratedTranscriptionsModel(BaseModel):
    """Transcriptions that have been generated automatically with one of the possible models."""

    language: str | None
    transcription: list[TranscriptionSegment]
