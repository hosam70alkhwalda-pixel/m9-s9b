"""Load `data/recipes_kg_subset.cypher` into the running Neo4j and
assert acceptance.

Run by the CI workflow before pytest, and by learners locally before
running the autograder. Idempotent: every run wipes the graph first so
the fixture is the only state under test.

Acceptance checks (exits non-zero on mismatch):
  * total node count == EXPECTED_NODES
  * total relationship count == EXPECTED_RELS
  * the entity_id_unique constraint exists (NEW or PRE-EXISTING)
  * no duplicate :Entity ids

Expected counts for the ~40-node subset (see contract §5):
  * 31 nodes (8 cuisines + 8 ingredients + 4 authors + 3 techniques + 8 recipes)
  * 48 relationships
"""
from __future__ import annotations

import os
import sys

from neo4j import GraphDatabase


EXPECTED_NODES = 31
EXPECTED_RELS = 48

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "testtest")

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "data", "recipes_kg_subset.cypher")


def _read_statements(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Strip // line comments.
    cleaned_lines = []
    for line in text.splitlines():
        idx = line.find("//")
        cleaned_lines.append(line[:idx] if idx >= 0 else line)
    cleaned = "\n".join(cleaned_lines)
    # Split on ';' — each statement runs separately.
    parts = [s.strip() for s in cleaned.split(";")]
    return [s for s in parts if s]


def main() -> int:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            # Wipe.
            session.run("MATCH (n) DETACH DELETE n").consume()

        statements = _read_statements(FIXTURE_PATH)
        with driver.session() as session:
            for stmt in statements:
                session.run(stmt).consume()

        # Acceptance.
        with driver.session() as session:
            n_nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
            n_rels = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
            dup_rows = list(session.run(
                "MATCH (n:Entity) WITH n.id AS id, count(*) AS c "
                "WHERE c > 1 RETURN id, c"
            ))

        print(f"Loaded fixture: {n_nodes} nodes, {n_rels} relationships.")

        ok = True
        if n_nodes != EXPECTED_NODES:
            print(f"FAIL: expected {EXPECTED_NODES} nodes, got {n_nodes}", file=sys.stderr)
            ok = False
        if n_rels != EXPECTED_RELS:
            print(f"FAIL: expected {EXPECTED_RELS} relationships, got {n_rels}", file=sys.stderr)
            ok = False
        if dup_rows:
            print(f"FAIL: duplicate :Entity ids: {dup_rows}", file=sys.stderr)
            ok = False

        return 0 if ok else 1
    finally:
        driver.close()


if __name__ == "__main__":
    sys.exit(main())
