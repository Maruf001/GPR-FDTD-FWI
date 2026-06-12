# Experiment 124: IMRAD Manuscript Current Validation Refresh

## Purpose

Refresh the run 562 IMRAD manuscript reproducibility pointers after the current
local validation, resume checkpoint, commit summary, action queue, and artifact
audit advanced beyond run 575.

## 591: IMRAD Manuscript Current Validation Refresh

Output:

```text
outputs/experiments/591_imrad_manuscript_current_validation_refresh
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Lint run references, range references, embedded image links, editing markers,
section balance, guardrail phrases, and duplicate limitations text for the run
562 manuscript after updating validation/archive pointers.
PY
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint_current_refresh.json
data/manuscript_balance_audit_current_refresh.json
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint current refresh: pass
referenced runs: 54
missing referenced runs: 0
embedded images resolved: 7
unresolved editing markers: 0
manuscript balance/guardrail audit current refresh: pass
required guardrails present: 5/5
duplicate interval-supported sentence: false
```

## Interpretation

The manuscript now cites the current post-sparse-hardening validation state
without changing scientific claims, figure set, or no-GPU queue decision.

## Next Decision

Refresh commit preparation and the next-action queue so manuscript validation
points to run 591.
