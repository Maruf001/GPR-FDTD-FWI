# Experiment 263: IMRAD Manuscript Current Validation Refresh

## Purpose

Refresh the IMRAD manuscript validation pointers from the run 685
archive-coverage state to the current validation, review, archive-coverage,
commit, queue, and audit state.

## 730: IMRAD Manuscript Current Validation Refresh

Output:

```text
outputs/experiments/730_imrad_manuscript_current_validation_refresh
```

Command:

```text
Update the manuscript validation/archive section and Data And Code Availability
block to the current run 718/722/726/727/728/729 state, then lint references,
images, markers, and guardrail prose.
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_current_validation_refresh.json
data/manuscript_balance_audit_current_validation_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint: pass
referenced runs: 68
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit: pass
word count: 1673
required guardrails present: 5/5
duplicate interval-supported sentence: false
git diff --check: clean after run 730
```

## Interpretation

The manuscript now points to the current local validation, code self-review,
aggregate/objective CLI smokes, state audit, archive coverage, commit summary,
resume checkpoint, and action queue. No scientific claim changed.

## Next Decision

Refresh commit-preparation and next-action queue pointers so manuscript
validation points to run 730.
