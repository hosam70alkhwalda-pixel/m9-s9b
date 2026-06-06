"""OPTIONAL — M8 stretch query router warm-up.

Bridges the M8 → M9 → M10 cumulative multi-agent artifact. If you
completed the M8 stretch (query router with vector / BM25 / metadata
branches), you can register the M9 KG critic as the **KG branch** so a
single router can either retrieve OR verify, depending on the routed
intent.

Not autograder-gated — rubric points only (see Stretch Tue page).
Degrades gracefully: a learner who did not complete M8 stretch can
leave this file untouched and forfeit only the warm-up portion of the
rubric.

────────────────────────────────────────────────────────────────────
Reference shape (not a working implementation — your M8 router may
have a different surface):

    from m8_stretch.router import QueryRouter
    from critic.verify import verify_claim
    from neo4j import GraphDatabase

    def register_kg_branch(router: QueryRouter, neo4j_driver) -> None:
        '''Register verify_claim as the KG branch of the router.

        The router classifies the incoming query intent. When the intent
        is "verify_claim" (the query carries a structured (s, p, o)
        claim), the router dispatches to verify_claim instead of any of
        the retrieval branches.
        '''
        def kg_branch(query):
            claim = query.payload["claim"]  # adjust to your router's payload shape
            return verify_claim(neo4j_driver, claim)

        router.register("verify_claim", kg_branch)

────────────────────────────────────────────────────────────────────
Write a brief paragraph in ``learner_notes.md`` describing how you
wired this in (or why you skipped it). Either is acceptable; the
rubric rewards a thoughtful writeup.
"""
