# Module 9 Week B — Stretch Tue: KG Critic on Neo4j

**Honors Track.** Complete the core Applied Lab 9B (`m9-l9b`) first — the
critic's verification cascade builds directly on the lab's Identity
Discipline and SUBCLASS_OF entailment patterns. Honors Track work is
required for Honors distinction but not for program completion. See the
Stretch Tue page for the full eligibility note.

## What you build

A **KG Critic** — a verifier that takes a `(subject, predicate, object)`
claim and decides whether the recipes graph **supports**, **entails**,
**contradicts**, or has nothing to say about it (`unsupported` —
abstain).

A KG critic is a first-class verification primitive in any production
retrieval-augmented system: when an LLM emits a structured claim, the
critic adjudicates it against the graph instead of trusting the LLM's
generated text. This stretch operationalizes one of the load-bearing
answers to "what is a KG *for?*" — verification under the open-world
assumption, with explicit abstention.

The cascade is intentionally short — four stages, returning the first
verdict that fires:

1. **Direct EXISTS** → `supported` (confidence 1.0)
2. **Hierarchical entailment via `[:SUBCLASS_OF*0..]`** → `entailed` (confidence 0.7)
3. **Domain/range violation** → `contradicted` (confidence 0.8)
4. **Otherwise** → `unsupported` (confidence 0.5)

You implement Stages 1–4 inside `critic/verify.py`. The schema
constraints, the Verdict dataclass, the claim extractor, and the
fixture loader are all course-provided.

## Setup

```bash
# 1. Start Neo4j locally.
docker compose up -d
docker compose logs -f neo4j | head
# Wait for "Started." then Ctrl-C.

# 2. Python deps (the M9 venv from the lab is fine).
pip install -r requirements.txt

# 3. Load the fixture and assert acceptance.
python load_fixture.py

# 4. Run the autograder.
pytest tests/ -v
```

The unmodified starter is expected to fail — the cascade isn't wired
up yet. See `critic/verify.py` for the four TODO blocks.

## File map

```
starter/
├── critic/
│   ├── verify.py           # YOU IMPLEMENT — 4-stage cascade (Option B TODOs)
│   ├── verdict.py          # course-provided — Verdict dataclass (frozen)
│   ├── extractor.py        # course-provided — parses (s,p,o) from text
│   ├── router_warmup.py    # OPTIONAL — M8 router integration writeup
│   └── __init__.py
├── data/
│   ├── recipes_kg_subset.cypher  # frozen ~40-node fixture
│   ├── eval_set.py               # 40 labeled claims (20 sup / 10 ent / 10 con)
│   └── README.md                 # schema reference for the cascade
├── load_fixture.py         # CI: wipe + load + assert acceptance
├── learner_notes.md        # YOU WRITE — design decisions and observations
├── docker-compose.yml      # local Neo4j (mirrors CI service container)
├── requirements.txt
├── FORK-SUBMIT.md          # how to submit (fork-and-submit flow)
└── LICENSE
tests/
├── test_critic.py          # cascade gates (precision/recall thresholds)
├── test_verdict_shape.py
└── test_extractor_unchanged.py
.github/workflows/m9-s9b-autograder.yml
```

## Deliverables

1. A working `critic/verify.py` that passes the autograder gates on the
   eval-set classes.
2. A short writeup in `learner_notes.md` covering your design choices,
   per-class precision/recall observations, and your view of the
   abstention boundary.
3. (Optional) A wired `critic/router_warmup.py` + a note in
   `learner_notes.md` if you completed the M8 stretch query router.

Submission: see `FORK-SUBMIT.md`. Branch name: `stretch-9b-tue-kg-critic`.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.
