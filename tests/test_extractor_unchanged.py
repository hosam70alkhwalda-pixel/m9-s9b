"""Guard the course-provided extractor's public API.

Learners may improve `critic/extractor.py` internally, but the
`extract_claims(text) -> list[tuple[str,str,str]]` signature and shape
must continue to work — downstream code (and TAs running through the
critic) rely on it.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from critic.extractor import extract_claims


def test_extracts_three_claims():
    text = (
        "recipe:001 USES_INGREDIENT ingredient:ginger\n"
        "recipe:001 OF_CUISINE cuisine:sichuan\n"
        "cuisine:sichuan type cuisine:asian\n"
    )
    claims = extract_claims(text)
    assert claims == [
        ("recipe:001", "USES_INGREDIENT", "ingredient:ginger"),
        ("recipe:001", "OF_CUISINE", "cuisine:sichuan"),
        ("cuisine:sichuan", "type", "cuisine:asian"),
    ]


def test_skips_blank_and_comment_lines():
    text = (
        "\n"
        "# a comment\n"
        "recipe:001 USES_INGREDIENT ingredient:ginger\n"
        "\n"
    )
    assert extract_claims(text) == [
        ("recipe:001", "USES_INGREDIENT", "ingredient:ginger"),
    ]


def test_returns_list_of_3_tuples():
    claims = extract_claims("recipe:001 OF_CUISINE cuisine:sichuan")
    assert isinstance(claims, list)
    assert all(isinstance(c, tuple) and len(c) == 3 for c in claims)


def test_empty_input_returns_empty_list():
    assert extract_claims("") == []
    assert extract_claims(None) == []  # type: ignore[arg-type]
