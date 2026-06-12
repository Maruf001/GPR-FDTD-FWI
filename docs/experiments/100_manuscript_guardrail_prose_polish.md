# Experiment 100: Manuscript Guardrail Prose Polish

## Purpose

Record the prose cleanup after the manuscript balance audit: restore readable
guardrail sentence wrapping, remove a duplicated phrase, and rerun the
manuscript checks.

## 567: Manuscript Guardrail Prose Polish

Output:

```text
outputs/experiments/567_manuscript_guardrail_prose_polish
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Rerun manuscript structural lint and whitespace-normalized balance/guardrail
audit after prose cleanup.
PY
```

Artifacts:

```text
README.md
run_manifest.json
```

Validation:

```text
IMRAD manuscript lint: pass
manuscript balance/guardrail audit: pass
referenced runs: 42
embedded images resolved: 7
required guardrails present: 5/5
duplicate interval-supported sentence: false
```

## Interpretation

No scientific claim changed. The manuscript is more readable and the guardrail
audit is less brittle.

## Next Decision

Continue manuscript polish, code/docs review, commit preparation, or handoff.
