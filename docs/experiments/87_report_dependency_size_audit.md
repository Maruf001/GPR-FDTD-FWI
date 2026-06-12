# Experiment 87: Report Dependency Size Audit

## Purpose

Measure the ignored output folders needed by the final report before choosing
an archive strategy.

## 554: Report Dependency Size Audit

Output:

```text
outputs/experiments/554_report_dependency_size_audit
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python - <<'PY'
Read run 549 referenced run IDs, add runs 548-553, and measure each matching
outputs/experiments folder with du -sb.
PY
```

Artifacts:

```text
README.md
data/report_dependency_size_audit.csv
data/report_dependency_size_audit.json
run_manifest.json
```

Result:

```text
referenced run IDs: 48
existing folders: 48
missing folders: 0
total size: 9.244 MiB
```

Largest folders:

```text
run 481: 0.983 MiB
run 532: 0.825 MiB
run 505: 0.552 MiB
run 528: 0.464 MiB
run 526: 0.464 MiB
```

## Interpretation

The report dependency output set is small enough for safe archiving if the user
chooses to package ignored outputs. This run only audits sizes; it does not
create an archive or change git tracking.

## Next Decision

Choose whether to create an explicit report-dependency archive or continue with
manuscript editing.
