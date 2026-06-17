# Stretch Tue — Learner Notes (KG Critic)

## Design decisions

In `verify_claim`, I implemented the cascade strictly in the required order (Stage 1 → Stage 2 → Stage 3 → Stage 4), ensuring that the first matching stage returns immediately and prevents later stages from executing.

- **Stage 1 (Direct EXISTS):**  
  I used a parameterized Cypher query for direct edge existence checks between `subject_id` and `object_id`. The relationship type is validated against `SCHEMA_CONSTRAINTS` and only then injected as a safe literal into the query. This ensures both correctness and protection against Cypher injection.

- **Stage 2 (Hierarchical entailment):**  
  I used a single variable-length traversal query:
  `[:SUBCLASS_OF*1..]`  
  This keeps entailment logic compact and avoids duplicating logic for depth-0 vs depth-≥1 cases. Stage 1 exclusively handles reflexive (depth-0) cases.

- **Stage 3 (Domain/Range contradiction):**  
  I fetch node labels using a parameterized helper (`_labels_of`) and compare them against `SCHEMA_CONSTRAINTS`. To improve efficiency, I avoided repeated label lookups by calling the helper only once per node per claim.

- **Stage 4 (Abstain):**  
  If no prior stage fires, the function returns `unsupported` with a neutral confidence score, following the open-world assumption.

- **Rejected considerations:**
  - Using separate Cypher queries for Stage 1 and Stage 2 (rejected in favor of cleaner separation via explicit stage logic in Python).
  - Using `*0..` traversal for entailment (rejected because it would overlap with Stage 1 and break cascade clarity).
  - Adding heuristic scoring beyond fixed stage confidence values (rejected to preserve deterministic grading behavior).

---

## Eval-set behavior

After running the autograder, the results were:

| Class        | Precision | Recall |
|--------------|-----------|--------|
| supported    | 1.000     | 1.000  |
| entailed     | 1.000     | 1.000  |
| contradicted | 1.000     | 1.000  |

**Observations:**
- All classes achieved perfect precision and recall, indicating correct stage ordering and correct separation between direct support, hierarchical entailment, and schema-based contradiction.
- The most sensitive part of the system was Stage 2 vs Stage 4 boundary handling; ensuring correct `*1..` traversal was key to achieving full recall on entailed-only cases.

---

## Abstention boundary

The correct use of `"unsupported"` is when the graph provides no direct evidence, no hierarchical entailment, and no schema violation.

In other words, abstention is the default fallback when the system cannot justify a stronger claim.

Over-flagging a claim as `"contradicted"` is worse than abstaining because contradiction implies the graph explicitly violates a rule or structure. If this is predicted incorrectly, it introduces false negatives that are more harmful than missing information, since it incorrectly asserts that something is impossible or invalid rather than simply unknown.

Abstention preserves the open-world assumption and ensures the critic remains conservative when evidence is insufficient.

---

## Optional — M8 router warm-up

Not applicable in this implementation. The `verify_claim` function was used independently as a standalone verification component and was not integrated into the M8 query router.