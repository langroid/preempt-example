"""
Run like this:
    uv run tests/test-round-trip.py
"""

from typing import List
from preempt.sanitizer import *
from rich.console import Console
console = Console()

import torch

device = (
    "mps" if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available()
    else "cpu"
)
# Load NER object
# ner_model = NER("/path/to/UniNER-7B-all", device="cuda:1")
ner_model = NER("meta-llama/Meta-Llama-3.1-8B-Instruct", device=device)
# Load Sanitizer objects for name and money
sanitizer_name = Sanitizer(
    ner_model,
    key = "EF4359D8D580AA4F7F036D6F04FC6A94",
    tweak = "D8E7920AFA330A73"
)
sanitizer_money = Sanitizer(
    ner_model,
    key = "FF4359D8D580AA4F7F036D6F04FC6A94",
    tweak = "E8E7920AFA330A73"
)

def sanitize_names(sentences: List[str]) -> List[str]:
    """
    Sanitize names in a list of sentences using a Sanitizer object.

    Args:
        sentences (List[str]): List of sentences to sanitize.

    Returns:
        List[str]: List of sanitized sentences.
    """

    # Sanitizing names
    return sanitizer_name.encrypt(
        sentences,
        entity='Name',
        epsilon=1,
    )


def sanitize_money(sentences: List[str]) -> List[str]:
    """
    Sanitize money values in a list of sentences using a Sanitizer object.

    Args:
        sentences (List[str]): List of sentences to sanitize.

    Returns:
        List[str]: List of sanitized sentences.
    """

    return sanitizer_money.encrypt(
        sentences,
        entity='Money',
        epsilon=1,
    )


def desanitize_names(sentences: List[str]) -> List[str]:
    """
    Desanitize names in a list of sentences using a Sanitizer object.

    Args:
        sentences (List[str]): List of sentences to desanitize.

    Returns:
        List[str]: List of desanitized sentences.
    """

    # Load Sanitizer object for names
    return sanitizer_name.decrypt(sentences, entity='Name', use_cache=True)

def desanitize_money(sentences: List[str]) -> List[str]:
    """
    Desanitize money values in a list of sentences using a Sanitizer object.

    Args:
        sentences (List[str]): List of sentences to desanitize.

    Returns:
        List[str]: List of desanitized sentences.
    """

    # Load Sanitizer object for money
    return sanitizer_money.decrypt(sentences, entity='Money', use_cache=True)


def sanitize_names_money(sentences: List[str]) -> List[str]:
    """
    Sanitize names and money values in a list of sentences using a Sanitizer object.

    Args:
        sentences (List[str]): List of sentences to sanitize.

    Returns:
        List[str]: List of sanitized sentences.
    """

    # Sanitizing names
    sanitized_sentences, _ = sanitizer_name.encrypt(
        sentences,
        entity='Name',
        epsilon=1,
    )

    # Sanitizing money values
    sanitized_sentences, _ = sanitizer_money.encrypt(
        sanitized_sentences,
        entity='Money',
        epsilon=1,
    )

    return sanitized_sentences


def desanitize_money_names(sentences: List[str]) -> List[str]:
    """
    Desanitize names and money values in a list of sentences using a Sanitizer object.

    Args:
        sentences (List[str]): List of sentences to desanitize.

    Returns:
        List[str]: List of desanitized sentences.
    """

    # Load Sanitizer object for names
    desanitized_sentences = sanitizer_money.decrypt(
        sentences,
        entity='Money',
        use_cache=True,
    )

    # Load Sanitizer object for money
    desanitized_sentences = sanitizer_name.decrypt(
        desanitized_sentences,
        entity='Name',
        use_cache=True,
    )

    return desanitized_sentences

