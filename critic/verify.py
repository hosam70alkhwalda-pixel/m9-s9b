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

_KNOWN_RELATIONSHIP_PREDICATES = frozenset(SCHEMA_CONSTRAINTS.keys())


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


def _validate_relationship_predicate(predicate: str) -> str:
    """Return `predicate` unchanged iff it is a known relationship type.

    This is the ONLY claim component ever allowed to be template-
    substituted into a Cypher string, and only after this check passes
    — relationship type cannot be bound as a $param in vanilla Cypher.
    subject_id / object_id must always flow through $param slots instead.
    """
    if predicate not in _KNOWN_RELATIONSHIP_PREDICATES:
        raise ValueError(f"Unknown relationship predicate: {predicate!r}")
    return predicate


def _stage1_supported(driver, subject_id: str, predicate: str, object_id: str) -> bool:
    """Stage 1 — is this claim already directly asserted in the graph?

    "type" claims use the reflexive depth-0 SUBCLASS_OF pattern (subject
    and object are the same node). Relationship predicates use a direct
    MATCH on the named edge between the two :Entity nodes.
    """
    if predicate == "type":
        query = (
            "MATCH (h:Entity {id: $subject_id})-[:SUBCLASS_OF*0..0]->(t:Entity {id: $object_id}) "
            "RETURN h.id AS h, t.id AS t LIMIT 1"
        )
    else:
        rel_type = _validate_relationship_predicate(predicate)
        query = (
            f"MATCH (h:Entity {{id: $subject_id}})-[:{rel_type}]->(t:Entity {{id: $object_id}}) "
            "RETURN h.id AS h, t.id AS t LIMIT 1"
        )

    with driver.session() as session:
        result = session.run(query, subject_id=subject_id, object_id=object_id)
        return result.single() is not None


def _stage2_entailed_chain(driver, subject_id: str, object_id: str) -> tuple[str, ...] | None:
    """Stage 2 — does subject_id reach object_id via 1+ SUBCLASS_OF hops?

    Only meaningful for "type" claims. Depth >= 1 is enforced via *1..
    so this stage never re-fires on the depth-0 case Stage 1 already
    covers — that's what keeps "entailed" distinguishable from
    "supported".
    """
    query = (
        "MATCH path = (h:Entity {id: $subject_id})-[:SUBCLASS_OF*1..]->(t:Entity {id: $object_id}) "
        "RETURN [n IN nodes(path) | n.id] AS chain LIMIT 1"
    )
    with driver.session() as session:
        result = session.run(query, subject_id=subject_id, object_id=object_id)
        row = result.single()
        if row is None:
            return None
        return tuple(row["chain"])


def _stage3_contradicts(driver, subject_id: str, predicate: str, object_id: str) -> bool:
    """Stage 3 — does this claim violate the predicate's domain/range?

    Only fires when BOTH endpoints exist and carry a non-:Entity label —
    a missing node is absence of evidence, not a contradiction, and
    should fall through to Stage 4's abstention rather than being
    over-flagged here. (Over-flagging contradicted on a node we simply
    have no evidence about is a worse error than abstaining: it commits
    to a high-confidence claim we can't actually back.)
    """
    expected_source, expected_target = SCHEMA_CONSTRAINTS[predicate]
    subject_labels = _labels_of(driver, subject_id)
    object_labels = _labels_of(driver, object_id)
    if not subject_labels or not object_labels:
        return False
    return expected_source not in subject_labels or expected_target not in object_labels


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
    """
    subject_id, predicate, object_id = claim

    if predicate != "type" and predicate not in SCHEMA_CONSTRAINTS:
        raise ValueError(f"Unknown predicate: {predicate!r}")

    # Stage 1 — direct EXISTS
    if _stage1_supported(driver, subject_id, predicate, object_id):
        return Verdict("supported", [(subject_id, object_id)], 1.0)

    # Stage 2 — hierarchical entailment (type claims only)
    if predicate == "type":
        chain = _stage2_entailed_chain(driver, subject_id, object_id)
        if chain is not None:
            return Verdict("entailed", [chain], 0.7)

    # Stage 3 — domain/range contradiction (relationship predicates only)
    if predicate != "type" and _stage3_contradicts(driver, subject_id, predicate, object_id):
        return Verdict("contradicted", [(subject_id, object_id)], 0.8)

    # Stage 4 — abstain (the honest "no")
    return Verdict("unsupported", [], 0.5)