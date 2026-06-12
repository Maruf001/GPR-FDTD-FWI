# Experiment 152: IMRAD Manuscript Current Archive Validation Refresh

## Purpose

Refresh the run 562 IMRAD manuscript reproducibility pointers from the older
run 591/run 580 archive state to the current run 610-618 smoke, audit, commit,
queue, and archive state.

## 619: IMRAD Manuscript Current Archive Validation Refresh

Output:

```text
outputs/experiments/619_imrad_manuscript_current_archive_validation_refresh
```

Command:

```text
Update the manuscript validation/archive and Data And Code Availability blocks,
then run structural manuscript lint and balance/guardrail audit.
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_current_archive_refresh.json
data/manuscript_balance_audit_current_archive_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint current archive refresh: pass
referenced runs: 50
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit current archive refresh: pass
word count: 1820
required guardrails present: 5/5
git diff --check: clean after run 619
```

## Interpretation

The manuscript now points to the current post-smoke-audit validation and archive
state without changing the scientific claims. The structural lint confirms that
all referenced runs and embedded figures resolve.

## Next Decision

Refresh commit-preparation and next-action queue pointers so manuscript
validation points to run 619.
