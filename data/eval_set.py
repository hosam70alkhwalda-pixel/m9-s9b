"""Frozen 40-claim eval set for the KG critic.

Each entry is {"claim": (s_id, predicate, o_id), "label": "supported" |
"entailed" | "contradicted"}.

Conventions:

- "type" predicate: claim is that `s_id` is-a `o_id`, where `o_id` is
  another entity (typically a Cuisine or Ingredient higher in the
  hierarchy). The verifier should resolve "type" via [:SUBCLASS_OF*0..]
  traversal — depth-0 covers the trivial reflexive case (s == o).

- Domain predicates (USES_INGREDIENT, OF_CUISINE, BY_AUTHOR,
  REQUIRES_TECHNIQUE): claim is the corresponding directed relationship
  (s)-[:PREDICATE]->(o). Domain/range labels are pinned in
  critic/verify.py's SCHEMA_CONSTRAINTS.

Distribution (per Phase 3 contract §5):
  20 supported, 10 entailed-only, 10 contradicted.

Labels are NOT visible to the critic at runtime — the autograder reads
them here and compares predicted verdicts to gold.
"""

EVAL_SET = [
    # ─── 20 SUPPORTED ────────────────────────────────────────────────
    # Reflexive type claims (depth-0 of SUBCLASS_OF*) — trivially true.
    {"claim": ("cuisine:sichuan",              "type", "cuisine:sichuan"),       "label": "supported"},
    {"claim": ("cuisine:italian",              "type", "cuisine:italian"),       "label": "supported"},
    {"claim": ("ingredient:basil",             "type", "ingredient:basil"),      "label": "supported"},
    {"claim": ("ingredient:peppercorn",        "type", "ingredient:peppercorn"), "label": "supported"},
    # Direct USES_INGREDIENT edges.
    {"claim": ("recipe:001", "USES_INGREDIENT", "ingredient:szechuanpeppercorn"), "label": "supported"},
    {"claim": ("recipe:002", "USES_INGREDIENT", "ingredient:ginger"),             "label": "supported"},
    {"claim": ("recipe:004", "USES_INGREDIENT", "ingredient:basil"),              "label": "supported"},
    {"claim": ("recipe:004", "USES_INGREDIENT", "ingredient:tomato"),             "label": "supported"},
    {"claim": ("recipe:006", "USES_INGREDIENT", "ingredient:tomato"),             "label": "supported"},
    {"claim": ("recipe:007", "USES_INGREDIENT", "ingredient:ginger"),             "label": "supported"},
    {"claim": ("recipe:008", "USES_INGREDIENT", "ingredient:basil"),              "label": "supported"},
    # Direct OF_CUISINE edges.
    {"claim": ("recipe:001", "OF_CUISINE",     "cuisine:sichuan"),               "label": "supported"},
    {"claim": ("recipe:004", "OF_CUISINE",     "cuisine:italian"),               "label": "supported"},
    {"claim": ("recipe:005", "OF_CUISINE",     "cuisine:tuscan"),                "label": "supported"},
    # Direct BY_AUTHOR edges.
    {"claim": ("recipe:001", "BY_AUTHOR",      "author:li-wei"),                 "label": "supported"},
    {"claim": ("recipe:004", "BY_AUTHOR",      "author:maria-rossi"),            "label": "supported"},
    {"claim": ("recipe:007", "BY_AUTHOR",      "author:julia-chen"),             "label": "supported"},
    # Direct REQUIRES_TECHNIQUE edges.
    {"claim": ("recipe:002", "REQUIRES_TECHNIQUE", "technique:stir-fry"),        "label": "supported"},
    {"claim": ("recipe:006", "REQUIRES_TECHNIQUE", "technique:saute"),           "label": "supported"},
    {"claim": ("recipe:001", "REQUIRES_TECHNIQUE", "technique:braise"),          "label": "supported"},

    # ─── 10 ENTAILED-ONLY ────────────────────────────────────────────
    # type claims that hold only via [:SUBCLASS_OF*0..] traversal.
    # Cuisine hierarchy.
    {"claim": ("cuisine:sichuan",   "type", "cuisine:chinese"),  "label": "entailed"},   # Sichuan -> Chinese
    {"claim": ("cuisine:sichuan",   "type", "cuisine:asian"),    "label": "entailed"},   # Sichuan -> Chinese -> Asian
    {"claim": ("cuisine:sichuan",   "type", "cuisine:world"),    "label": "entailed"},   # 3-hop
    {"claim": ("cuisine:cantonese", "type", "cuisine:asian"),    "label": "entailed"},
    {"claim": ("cuisine:tuscan",    "type", "cuisine:european"), "label": "entailed"},
    {"claim": ("cuisine:tuscan",    "type", "cuisine:world"),    "label": "entailed"},
    {"claim": ("cuisine:italian",   "type", "cuisine:world"),    "label": "entailed"},
    # Ingredient hierarchy.
    {"claim": ("ingredient:szechuanpeppercorn", "type", "ingredient:peppercorn"), "label": "entailed"},
    {"claim": ("ingredient:szechuanpeppercorn", "type", "ingredient:spice"),      "label": "entailed"},
    {"claim": ("ingredient:basil",              "type", "ingredient:herb"),       "label": "entailed"},

    # ─── 10 CONTRADICTED ─────────────────────────────────────────────
    # Domain/range violations — the predicate's expected source or target
    # label does not match the actual entity's label per SCHEMA_CONSTRAINTS.
    {"claim": ("recipe:001",                    "BY_AUTHOR",          "ingredient:basil"),             "label": "contradicted"},  # BY_AUTHOR target must be Author
    {"claim": ("recipe:002",                    "BY_AUTHOR",          "cuisine:sichuan"),              "label": "contradicted"},
    {"claim": ("recipe:004",                    "USES_INGREDIENT",    "author:maria-rossi"),           "label": "contradicted"},  # USES_INGREDIENT target must be Ingredient
    {"claim": ("recipe:007",                    "USES_INGREDIENT",    "cuisine:sichuan"),              "label": "contradicted"},
    {"claim": ("recipe:001",                    "OF_CUISINE",         "ingredient:ginger"),            "label": "contradicted"},  # OF_CUISINE target must be Cuisine
    {"claim": ("recipe:008",                    "OF_CUISINE",         "author:antonio-b"),             "label": "contradicted"},
    {"claim": ("recipe:002",                    "REQUIRES_TECHNIQUE", "ingredient:garlic"),            "label": "contradicted"},  # REQUIRES_TECHNIQUE target must be Technique
    {"claim": ("ingredient:basil",              "USES_INGREDIENT",    "ingredient:tomato"),            "label": "contradicted"},  # USES_INGREDIENT source must be Recipe
    {"claim": ("author:maria-rossi",            "OF_CUISINE",         "cuisine:italian"),              "label": "contradicted"},  # OF_CUISINE source must be Recipe
    {"claim": ("cuisine:sichuan",               "BY_AUTHOR",          "author:li-wei"),                "label": "contradicted"},  # BY_AUTHOR source must be Recipe
]

assert len(EVAL_SET) == 40, f"Expected 40 claims, got {len(EVAL_SET)}"

# Convenience subset accessors used by the autograder.
SUPPORTED_CLAIMS    = [e for e in EVAL_SET if e["label"] == "supported"]
ENTAILED_CLAIMS     = [e for e in EVAL_SET if e["label"] == "entailed"]
CONTRADICTED_CLAIMS = [e for e in EVAL_SET if e["label"] == "contradicted"]

assert len(SUPPORTED_CLAIMS)    == 20
assert len(ENTAILED_CLAIMS)     == 10
assert len(CONTRADICTED_CLAIMS) == 10
