# Experiment 112: Current Handoff Archive Size Audit

## Purpose

Audit whether the old run 555 report dependency archive still covers the
current manuscript validation, commit summary, and action queue state.

## 579: Current Handoff Archive Size Audit

Output:

```text
outputs/experiments/579_current_handoff_archive_size_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Build current handoff dependency list from run 575 manuscript lint, docs,
runtime scripts/tests, and run 578 action queue; compare with run 555 archive.
PY
```

Artifacts:

```text
README.md
data/current_handoff_archive_size_audit.json
data/current_handoff_archive_file_list.txt
run_manifest.json
```

Validation:

```text
status: pass
dependency paths: 115
files: 351
total size: 13.7 MiB
missing paths: 0
paths not covered by run 555 archive: 36
archive recommended: true
```

## Interpretation

The old run 555 archive remains valid for its original dependency set but is
stale for the current handoff. A new compact current handoff archive is
justified and should be low-risk.

## Next Decision

Create the current handoff archive from the audited file list plus the run 579
audit folder.
