# Stretch Tue — Data

This directory holds the fixture graph and the labeled eval set the
KG critic is scored against. Both are frozen — your implementation
work is in `critic/verify.py`, not here.

## `recipes_kg_subset.cypher`

A ~40-node subset of the Lab 9B recipes fixture, kept small so CI
runs fast. The schema is identical to the lab:

* **Labels** — every domain node also carries `:Entity` for the
  Identity Discipline uniqueness constraint:
  * `:Recipe`, `:Cuisine`, `:Ingredient`, `:Author`, `:Technique`
* **Relationships:**
  * `(:Recipe)-[:USES_INGREDIENT]->(:Ingredient)`
  * `(:Recipe)-[:OF_CUISINE]->(:Cuisine)`
  * `(:Recipe)-[:BY_AUTHOR]->(:Author)`
  * `(:Recipe)-[:REQUIRES_TECHNIQUE]->(:Technique)`
  * `(:Cuisine)-[:SUBCLASS_OF]->(:Cuisine)` — load-bearing hierarchy
  * `(:Ingredient)-[:SUBCLASS_OF]->(:Ingredient)` — secondary hierarchy
* **id convention:** `'<label-lower>:<slug>'`, e.g., `'recipe:001'`,
  `'cuisine:sichuan'`, `'ingredient:szechuanpeppercorn'`.

Cuisine hierarchy (3+ levels — the critic's entailment stage walks
this chain):

```
World
├─ Asian
│  └─ Chinese
│     ├─ Sichuan
│     └─ Cantonese
└─ European
   └─ Italian
      └─ Tuscan
```

Ingredient subclass chains:

```
spice
└─ peppercorn
   └─ szechuanPeppercorn
herb
└─ basil
```

Expected counts (asserted by `load_fixture.py`): **31 nodes**,
**48 relationships**.

## `eval_set.py`

40 frozen claims in three subsets:

| Subset         | Count | Pattern |
|---|---|---|
| `supported`    | 20    | Direct edge or reflexive type claim — Stage 1 of the cascade fires. |
| `entailed`     | 10    | Type claim that requires walking `[:SUBCLASS_OF*0..]` — Stage 2 fires. |
| `contradicted` | 10    | Domain/range violation: predicate's expected source or target label does not match the actual node's label. Stage 3 fires. |

Claim format: `{"claim": (subject_id, predicate, object_id), "label": "<verdict>"}`.

The `"type"` predicate is special — it asks "is `subject_id` an instance
of `object_id`'s category?" — and is resolved by SUBCLASS_OF traversal
(depth-0 for reflexive supported, depth >=1 for entailed). The
relationship predicates (`USES_INGREDIENT`, `OF_CUISINE`, `BY_AUTHOR`,
`REQUIRES_TECHNIQUE`) check for a directed edge between the two
specific `:Entity` nodes.

Labels are NOT visible to the critic at runtime — the autograder reads
them here and compares against `verify_claim`'s predicted verdict.
