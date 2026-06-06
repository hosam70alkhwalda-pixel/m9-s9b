"""KG critic verifier — four-stage cascade.

Given a (subject_id, predicate, object_id) claim, decide whether the
recipes graph supports it, entails it, contradicts it, or has nothing
to say (unsupported / abstain).

Cascade order — MUST be applied in this sequence per the stretch
contract (§5 of the W9B Phase 3 build contract). The first stage that
fires returns; later stages do not run.

  1. **Direct EXISTS** — check whether the claim's edge / class-membership
     holds directly in the graph (no traversal of SUBCLASS_OF*).
     -> verdict="supported", confidence=1.0

  2. **Hierarchical entailment via [:SUBCLASS_OF*0..]** — for "type"
     claims, check whether `subject_id` reaches `object_id` along the
     SUBCLASS_OF chain (depth >=1; depth-0 is handled by Stage 1).
     -> verdict="entailed", confidence=0.7

  3. **Domain/range violation detection** — read SCHEMA_CONSTRAINTS
     below. If the predicate is in the dict and either the subject's or
     object's label disagrees with the expected (source_label, target_label)
     pair, the claim is structurally impossible.
     -> verdict="contradicted", confidence=0.8

  4. **Otherwise** — none of the above fired.
     -> verdict="unsupported", confidence=0.5

The whole point of the cascade (over a plain "does this edge exist"
ASK-style check) is the entailment stage — without it, recall on the
entailed-only subset collapses to 0.
"""
from __future__ import annotations

from .verdict import Verdict


# ─── Course-provided constant — do NOT modify. ───────────────────────
# Maps predicate names to (expected_source_label, expected_target_label).
# Stage 3 reads this to detect structural impossibilities. The "type"
# predicate is intentionally absent — type membership is governed by the
# subgraph's SUBCLASS_OF hierarchy, not by a fixed label pair.
SCHEMA_CONSTRAINTS: dict[str, tuple[str, str]] = {
    "USES_INGREDIENT":    ("Recipe", "Ingredient"),
    "OF_CUISINE":         ("Recipe", "Cuisine"),
    "BY_AUTHOR":          ("Recipe", "Author"),
    "REQUIRES_TECHNIQUE": ("Recipe", "Technique"),
}


def _labels_of(driver, node_id: str) -> list[str]:
    """Course-provided helper. Return the non-:Entity labels of the node
    with the given id, or [] if the node does not exist. Uses
    parameterized Cypher (never f-string interpolation)."""
    with driver.session() as session:
        result = session.run(
            "MATCH (n:Entity {id: $id}) RETURN [l IN labels(n) WHERE l <> 'Entity'] AS labels",
            id=node_id,
        )
        row = result.single()
        return list(row["labels"]) if row else []


def verify_claim(driver, claim: tuple[str, str, str]) -> Verdict:
    """Adjudicate a (subject_id, predicate, object_id) claim against the
    recipes graph via the four-stage cascade documented at the top of
    this module.

    Parameters
    ----------
    driver
        A connected `neo4j.GraphDatabase.driver(...)` instance.
    claim
        A 3-tuple ``(subject_id, predicate, object_id)``. ``predicate``
        is either ``"type"`` (class-membership claim) or one of the
        relationship-type keys in ``SCHEMA_CONSTRAINTS``.

    Returns
    -------
    Verdict
        With the verdict label, an evidence_paths list (node-id chains),
        and the confidence pinned by the cascade stage.

    Implementation requirements
    ---------------------------
    * All Cypher MUST be parameterized — pass `subject_id`, `predicate`,
      `object_id` through `session.run(..., key=value)` keyword args.
      f-string interpolation of any claim component into a Cypher string
      is a test failure (see `test_verify_uses_parameterized_cypher`).
    * The relationship-type filter cannot be a parameter in vanilla
      Cypher; you may template-substitute the predicate string ONLY
      after validating it is a known relationship type (e.g., it appears
      in SCHEMA_CONSTRAINTS or equals one of the known type names). The
      claim's subject/object ids must still flow through `$param` slots.
    """
    subject_id, predicate, object_id = claim

    # TODO — Stage 1: direct existence check.
    #
    # For the "type" predicate, this is the reflexive case (subject_id ==
    # object_id), or equivalently a depth-0 SUBCLASS_OF traversal.
    # For relationship predicates (USES_INGREDIENT, OF_CUISINE,
    # BY_AUTHOR, REQUIRES_TECHNIQUE), this is a MATCH on the directed
    # edge between the two :Entity nodes with the matching ids.
    # If the edge exists, return:
    #   Verdict("supported", [(subject_id, object_id)], 1.0)

    # TODO — Stage 2: hierarchical entailment via [:SUBCLASS_OF*0..].
    #
    # Only relevant for the "type" predicate (the SUBCLASS_OF hierarchy
    # encodes is-a relations; recipe-level edges do not have a hierarchy
    # in this fixture). If the subject reaches the object along a path
    # of one or more SUBCLASS_OF hops, the claim is entailed (not
    # directly asserted but logically implied). Build the evidence path
    # from the actual node ids visited in the chain. Return:
    #   Verdict("entailed", [tuple_of_ids_along_chain], 0.7)
    #
    # Note: Stage 1 already covered the depth-0 case. Stage 2 must look
    # for depth >= 1, so the entailed-only label is distinguishable from
    # supported.

    # TODO — Stage 3: domain/range violation detection.
    #
    # Look up `predicate` in SCHEMA_CONSTRAINTS. If present, fetch the
    # actual labels of the subject and object nodes (you may use the
    # course-provided `_labels_of` helper). If either side's label does
    # NOT match the expected label, the claim is structurally impossible
    # — return:
    #   Verdict("contradicted", [(subject_id, object_id)], 0.8)
    #
    # If the predicate is not in SCHEMA_CONSTRAINTS (e.g., "type"), skip
    # this stage and proceed to Stage 4.

    # TODO — Stage 4: abstain. None of the prior stages fired.
    #
    #   return Verdict("unsupported", [], 0.5)

    raise NotImplementedError(
        "verify_claim is not yet implemented — see the cascade docstring "
        "and Stretch Tue page."
    )
