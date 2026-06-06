# Stretch Tue — Learner Notes

This file is your writeup. Use it to record your design decisions, the
behavior you observed against the eval set, and (optionally) how you
wired the critic into the M8 stretch query router. The TA reads this
alongside `critic/verify.py` when grading the "README + optional
warm-up" rubric dimension.

A short, structured writeup is better than a long unstructured one.

## Design decisions

Briefly describe the choices you made in `verify_claim`:

* How did you structure the Stage 2 entailment query? Did you use a
  single variable-length `[:SUBCLASS_OF*0..]` traversal, or two
  separate Cypher calls (one for depth-0, one for depth >=1)? Why?
* For Stage 3 (domain/range), did you fetch labels once per call or
  cache them across calls?
* Anything you considered but rejected? (Stage ordering, confidence
  values, extra signals you tried.)

## Eval-set behavior

Run the autograder locally and record what you observed:

| Class          | Precision | Recall |
|---|---|---|
| supported      |           |        |
| entailed       |    -      |        |
| contradicted   |           |   -    |

Notes:
* Which class was hardest to hit the gate on? Why?
* Did any individual claim surprise you (predicted differently than
  you expected on inspection of the cascade)?

## Abstention boundary

In your own words: *what is the right way to think about when the
critic should return `"unsupported"` vs. one of the other three
verdicts?* Why is over-flagging "contradicted" worse than abstaining?

## Optional — M8 router warm-up

If you completed the M8 stretch query router, describe how you wired
`verify_claim` into it. If you skipped this, write one sentence saying
so. Either is acceptable.
