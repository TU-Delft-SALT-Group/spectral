# ruff: noqa
"""Several response examples, purely for the documentation purposes."""

from __future__ import annotations

from typing import Any

signal_modes_response_examples: dict[int | str, dict[str, Any]] = {
    200: {
        "content": {
            "application/json": {
                "examples": {
                    "simple-info": {
                        "summary": "Example for simple-info mode",
                        "value": {
                            "duration": 2.12,
                            "averagePitch": 30.2,
                            "fileSize": 123456,
                            "fileCreationDate": "2024-05-21T09:58:42.263896",
                            "frame": {
                                "duration": 0.04,
                                "pitch": 200.2,
                                "f1": 400.56,
                                "f2": 800.98,
                            },
                        },
                    },
                    "spectrogram": {
                        "summary": "Example for spectrogram mode",
                        "value": "null (actual null value, fastapi currently doesn't support examples with just null)",
                    },
                    "waveform": {
                        "summary": "Example for waveform mode",
                        "value": "null (actual null value, fastapi currently doesn't support examples with just null)",
                    },
                    "vowel-space": {
                        "summary": "Example for vowel-space mode",
                        "value": {"f1": 400.56, "f2": 800.98},
                    },
                    "vowel-space no frame": {
                        "summary": "Example for vowel-space mode if no frame is provided",
                        "value": None,
                    },
                    "transcription": {
                        "summary": "Example for transcription mode",
                        "value": [
                            [
                                {"value": "foo", "start": 0, "end": 0.12},
                                {"value": "bar", "start": 0.12, "end": 0.24},
                            ],
                        ],
                    },
                    "error_rate": {
                        "summary": "Example for error rate mode",
                        "value": {
                            "groundTruth": "was a test",
                            "errorRate": {
                                "wordLevel": {
                                    "wer": 1.0,
                                    "mer": 0.6,
                                    "wil": 0.7333333333333334,
                                    "wip": 0.26666666666666666,
                                    "hits": 2,
                                    "substitutions": 1,
                                    "insertions": 2,
                                    "deletions": 0,
                                    "reference": ["was", "a", "test"],
                                    "hypothesis": [
                                        "this",
                                        "is",
                                        "a",
                                        "short",
                                        "test",
                                    ],
                                    "bert": 0.91,
                                    "jaroWinkler": 0.59,
                                    "alignments": [
                                        {
                                            "type": "insert",
                                            "referenceStartIndex": 0,
                                            "referenceEndIndex": 0,
                                            "hypothesisStartIndex": 0,
                                            "hypothesisEndIndex": 1,
                                        },
                                        {
                                            "type": "substitute",
                                            "referenceStartIndex": 0,
                                            "referenceEndIndex": 1,
                                            "hypothesisStartIndex": 1,
                                            "hypothesisEndIndex": 2,
                                        },
                                        {
                                            "type": "equal",
                                            "referenceStartIndex": 1,
                                            "referenceEndIndex": 2,
                                            "hypothesisStartIndex": 2,
                                            "hypothesisEndIndex": 3,
                                        },
                                        {
                                            "type": "insert",
                                            "referenceStartIndex": 2,
                                            "referenceEndIndex": 2,
                                            "hypothesisStartIndex": 3,
                                            "hypothesisEndIndex": 4,
                                        },
                                        {
                                            "type": "equal",
                                            "referenceStartIndex": 2,
                                            "referenceEndIndex": 3,
                                            "hypothesisStartIndex": 4,
                                            "hypothesisEndIndex": 5,
                                        },
                                    ],
                                },
                                "characterLevel": {
                                    "cer": 1.2,
                                    "hits": 8,
                                    "substitutions": 2,
                                    "insertions": 10,
                                    "deletions": 0,
                                    "reference": [
                                        "w",
                                        "a",
                                        "s",
                                        " ",
                                        "a",
                                        " ",
                                        "t",
                                        "e",
                                        "s",
                                        "t",
                                    ],
                                    "hypothesis": [
                                        "t",
                                        "h",
                                        "i",
                                        "s",
                                        " ",
                                        "i",
                                        "s",
                                        " ",
                                        "a",
                                        " ",
                                        "s",
                                        "h",
                                        "o",
                                        "r",
                                        "t",
                                        " ",
                                        "t",
                                        "e",
                                        "s",
                                        "t",
                                    ],
                                    "alignments": [
                                        {
                                            "type": "insert",
                                            "referenceStartIndex": 0,
                                            "referenceEndIndex": 0,
                                            "hypothesisStartIndex": 0,
                                            "hypothesisEndIndex": 1,
                                        },
                                        {
                                            "type": "substitute",
                                            "referenceStartIndex": 0,
                                            "referenceEndIndex": 2,
                                            "hypothesisStartIndex": 1,
                                            "hypothesisEndIndex": 3,
                                        },
                                        {
                                            "type": "equal",
                                            "referenceStartIndex": 2,
                                            "referenceEndIndex": 4,
                                            "hypothesisStartIndex": 3,
                                            "hypothesisEndIndex": 5,
                                        },
                                        {
                                            "type": "insert",
                                            "referenceStartIndex": 4,
                                            "referenceEndIndex": 4,
                                            "hypothesisStartIndex": 5,
                                            "hypothesisEndIndex": 8,
                                        },
                                        {
                                            "type": "equal",
                                            "referenceStartIndex": 4,
                                            "referenceEndIndex": 5,
                                            "hypothesisStartIndex": 8,
                                            "hypothesisEndIndex": 9,
                                        },
                                        {
                                            "type": "insert",
                                            "referenceStartIndex": 5,
                                            "referenceEndIndex": 5,
                                            "hypothesisStartIndex": 9,
                                            "hypothesisEndIndex": 15,
                                        },
                                        {
                                            "type": "equal",
                                            "referenceStartIndex": 5,
                                            "referenceEndIndex": 10,
                                            "hypothesisStartIndex": 15,
                                            "hypothesisEndIndex": 20,
                                        },
                                    ],
                                },
                            },
                        },
                    },
                },
            },
        },
    },
    400: {"content": {"application/json": {"example": {"detail": "error message"}}}},
    404: {"content": {"application/json": {"example": {"detail": "error message"}}}},
}

transcription_response_examples: dict[int | str, dict[str, Any]] = {
    200: {
        "content": {
            "application/json": {
                "example": [
                    {"value": "foo", "start": 0, "end": 0.12},
                    {"value": "bar", "start": 0.12, "end": 0.24},
                ],
            },
        },
    },
    404: {"content": {"application/json": {"example": {"detail": "error message"}}}},
    500: {"content": {"application/json": {"example": {"detail": "error message"}}}},
}
