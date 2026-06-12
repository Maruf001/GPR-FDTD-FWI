# Experiment 218: IMRAD Manuscript Current Archive-Coverage Validation Refresh

## Purpose

Refresh the IMRAD manuscript validation pointers from the run 636
resume/archive state to the current reporting, audit, archive-coverage,
commit, and queue state.

## 685: IMRAD Manuscript Current Archive-Coverage Validation Refresh

Output:

```text
outputs/experiments/685_imrad_manuscript_current_archive_coverage_validation_refresh
```

Command:

```text
Update the manuscript validation/archive section and Data And Code Availability
block to the current run 675/676/679/682/683/684 state, then lint references,
images, markers, and guardrail prose.
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_current_archive_coverage_refresh.json
data/manuscript_balance_audit_current_archive_coverage_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint: pass
referenced runs: 63
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit: pass
word count: 1482
required guardrails present: 5/5
duplicate interval-supported sentence: false
git diff --check: clean after run 685
```

## Interpretation

The manuscript now points to the current local validation, aggregate/objective
CLI smokes, state audit, archive coverage, commit summary, resume checkpoint,
and action queue. No scientific claim changed.

## Next Decision

Refresh commit-preparation and next-action queue pointers so manuscript
validation points to run 685.

