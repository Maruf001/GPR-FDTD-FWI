# Experiment 96: IMRAD Manuscript Lint

## Purpose

Verify the run 562 IMRAD manuscript draft.

## 563: IMRAD Manuscript Lint

Output:

```text
outputs/experiments/563_imrad_manuscript_lint
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Parse manuscript_draft.md, verify run references against outputs/experiments,
verify embedded image paths, and search for TODO/FIXME/TBD/XXX markers.
PY
```

Artifacts:

```text
README.md
data/imrad_manuscript_lint.json
run_manifest.json
```

Result:

```text
status=pass
referenced runs=42
missing runs=0
embedded images=7
broken embedded images=0
unresolved markers=0
```

## Interpretation

The IMRAD manuscript draft is structurally ready for manuscript editing. It
does not introduce missing evidence references or broken figure links.

## Next Decision

Continue with manuscript polish, commit preparation, or user-directed handoff.
