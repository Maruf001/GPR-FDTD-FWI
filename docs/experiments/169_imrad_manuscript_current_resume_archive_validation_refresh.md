# Experiment 169: IMRAD Manuscript Current Resume-Archive Validation Refresh

## Purpose

Refresh the run 562 IMRAD manuscript reproducibility pointers from the run
619/run 616 archive state to the current run 626/629/633/634/635 resume, audit,
archive, commit, and queue state.

## 636: IMRAD Manuscript Current Resume-Archive Validation Refresh

Output:

```text
outputs/experiments/636_imrad_manuscript_current_resume_archive_validation_refresh
```

Command:

```text
Update the manuscript validation/archive and Data And Code Availability
pointers, then run structural lint and balance/guardrail checks.
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_current_resume_archive_refresh.json
data/manuscript_balance_audit_current_resume_archive_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint current resume/archive refresh: pass
referenced runs: 57
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit current resume/archive refresh: pass
word count: 1454
required guardrails present: 5/5
git diff --check: clean after run 636
```

## Interpretation

The manuscript now points to the current run 626 restart checkpoint, run 629
state audit, run 633 archive, run 634 commit summary, and run 635 queue. No
scientific claim changed.

## Next Decision

Refresh commit-preparation and next-action queue pointers so manuscript
validation points to run 636.
