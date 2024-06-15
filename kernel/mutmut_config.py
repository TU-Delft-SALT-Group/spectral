"""The configuration setup for mutmut."""

from typing import Any


def pre_mutation(context: Any) -> None:
    """Skips a file with response examples for faster mutation testing."""
    if context.filename == "response_examples.py":
        context.skip = True
