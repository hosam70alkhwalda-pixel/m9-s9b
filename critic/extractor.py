"""Claim extraction from free-text answer strings.

FULLY IMPLEMENTED course-provided helper. Learners may *improve* this
module (e.g., tighten the regex, add spaCy parsing) — but the autograder
verifies that the public API (`extract_claims`) still accepts the same
input shape and returns the same structural type. See
`tests/test_extractor_unchanged.py`.

The default implementation parses a deliberately simple format:

    "<s_id> <PREDICATE> <o_id>"

per line, splitting on whitespace and skipping blanks/comments. This is
sufficient for the KG critic's downstream verifier — claim extraction
itself is not the load-bearing skill of this stretch.
"""
from __future__ import annotations


def extract_claims(answer_text: str) -> list[tuple[str, str, str]]:
    """Parse claim triples from a free-text answer.

    Each non-blank, non-comment line is expected to be three whitespace-
    separated tokens: ``s_id PREDICATE o_id``. Lines starting with ``#``
    are treated as comments.

    Parameters
    ----------
    answer_text : str
        Multi-line string containing zero or more claim lines.

    Returns
    -------
    list[tuple[str, str, str]]
        A list of (subject_id, predicate, object_id) triples in source
        order. Malformed lines are silently skipped — the verifier is
        responsible for adjudicating well-formed claims, not validating
        the answer's surface form.
    """
    claims: list[tuple[str, str, str]] = []
    for raw in (answer_text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 3:
            continue
        s, p, o = parts
        claims.append((s, p, o))
    return claims
