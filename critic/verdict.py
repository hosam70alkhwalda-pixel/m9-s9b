"""Verdict dataclass — fully implemented, do not modify.

The critic's `verify_claim` returns a Verdict instance. The four verdict
strings encode the cascade result; evidence_paths is the chain of node
ids that justified the verdict (one tuple per path); confidence is in
[0.0, 1.0].
"""
from dataclasses import dataclass, field
from typing import Literal


VerdictLabel = Literal["supported", "entailed", "contradicted", "unsupported"]


@dataclass(frozen=True)
class Verdict:
    """A KG critic verdict on a (subject, predicate, object) claim.

    Attributes
    ----------
    verdict : str
        One of "supported", "entailed", "contradicted", "unsupported".
    evidence_paths : list[tuple[str, ...]]
        Zero or more node-id chains documenting why the critic ruled the
        way it did. For "supported" this is typically [(s_id, o_id)]
        (the direct edge endpoints). For "entailed" this is the full
        SUBCLASS_OF traversal chain. For "contradicted" this names the
        offending source/target ids. For "unsupported" this is [].
    confidence : float
        In [0.0, 1.0]. Per the cascade:
          supported    -> 1.0
          entailed     -> 0.7
          contradicted -> 0.8
          unsupported  -> 0.5
    """
    verdict: VerdictLabel
    evidence_paths: list = field(default_factory=list)
    confidence: float = 0.0

    def __post_init__(self) -> None:
        if self.verdict not in ("supported", "entailed", "contradicted", "unsupported"):
            raise ValueError(f"Invalid verdict label: {self.verdict!r}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"confidence must be in [0.0, 1.0], got {self.confidence!r}"
            )
