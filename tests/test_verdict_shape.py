"""Structural tests for the Verdict dataclass."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from critic.verdict import Verdict


def test_verdict_label_set():
    """The four allowed verdict labels must round-trip through Verdict."""
    for label in ("supported", "entailed", "contradicted", "unsupported"):
        v = Verdict(verdict=label, evidence_paths=[], confidence=0.5)
        assert v.verdict == label


def test_verdict_rejects_unknown_label():
    with pytest.raises(ValueError):
        Verdict(verdict="maybe", evidence_paths=[], confidence=0.5)


def test_confidence_in_unit_interval():
    Verdict(verdict="supported", evidence_paths=[], confidence=0.0)
    Verdict(verdict="supported", evidence_paths=[], confidence=1.0)
    with pytest.raises(ValueError):
        Verdict(verdict="supported", evidence_paths=[], confidence=1.1)
    with pytest.raises(ValueError):
        Verdict(verdict="supported", evidence_paths=[], confidence=-0.1)


def test_evidence_paths_is_list():
    v = Verdict(verdict="entailed", evidence_paths=[("a", "b")], confidence=0.7)
    assert isinstance(v.evidence_paths, list)


def test_verdict_is_frozen():
    """The frozen=True guarantee — TAs can compare returned verdicts by
    structural equality without worrying about mutation."""
    v = Verdict(verdict="supported", evidence_paths=[], confidence=1.0)
    with pytest.raises(Exception):
        v.verdict = "entailed"  # type: ignore[misc]
