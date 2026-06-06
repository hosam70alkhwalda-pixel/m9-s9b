"""Shared test fixtures for the KG critic autograder."""
from __future__ import annotations

import os
import sys

import pytest

# Resolve imports against the repo root (where starter/ becomes the root
# on push). NEVER use "../starter/" — that path does not exist in the
# student's accepted repo.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from neo4j import GraphDatabase  # noqa: E402


NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "testtest")


@pytest.fixture(scope="session")
def driver():
    """Session-scoped Neo4j driver. The fixture has already been loaded
    by `load_fixture.py` in the CI pipeline (or by the learner locally)
    before pytest runs."""
    d = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        # Smoke probe.
        with d.session() as s:
            s.run("RETURN 1").consume()
        yield d
    finally:
        d.close()
