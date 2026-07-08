# BEM Experiment 592: Matched FDTD Input-Bound Exporter Post-Synthetic-Roundtrip External Staging Guard

Date: 2026-06-30

## Purpose

Audit the real external staging paths after the output-local synthetic exporter
roundtrip in runs `589-591`.

This run checks that the synthetic return files did not pollute the locked
external staging area.

## Output

```text
outputs/bem_experiments/592_project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_external_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard.png
scripts/
```

## Result

```text
source roundtrip ready:                  true
source validation ready:                 true
source sensitivity ready:                true
synthetic return files:                  2
synthetic accepted rows:                 558
external paths checked:                  4
external parent directories present:     4
external files present:                  0
external nonempty files:                 0
external accepted files:                 0
synthetic pollution count:               0
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

## Interpretation

The synthetic roundtrip stayed inside its own output folder. The locked
external real staging area remains empty and unaccepted.

## Decision

Use run `592` as the post-synthetic-roundtrip guard. Keep real BEM/FDTD
comparison blocked until actual external staged files are supplied and
accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
