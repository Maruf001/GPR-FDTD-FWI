# Experiment 108: IMRAD Manuscript Validation Refresh

## Purpose

Refresh the IMRAD manuscript state after the current validation and resume
artifacts changed from run 556/257 tests to run 573/258 tests.

## 575: IMRAD Manuscript Validation Refresh

Output:

```text
outputs/experiments/575_imrad_manuscript_validation_refresh
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Lint run references, embedded image links, editing markers, section balance,
guardrail phrases, and duplicate limitations text for the run 562 manuscript.
PY
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_refresh.json
data/manuscript_balance_audit_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint refresh: pass
referenced runs: 51
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit refresh: pass
required guardrails present: 5/5
duplicate interval-supported sentence: false
```

## Interpretation

The manuscript now cites the current post-hardening validation state without
changing the scientific claims, figure set, or no-GPU queue decision.

## Next Decision

Refresh the next-action queue or continue manuscript editing/commit
preparation.
