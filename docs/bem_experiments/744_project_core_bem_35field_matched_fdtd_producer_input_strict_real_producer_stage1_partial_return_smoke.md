# BEM Experiment 744: Strict Real-Producer Stage-1 Partial Return Smoke

Date: 2026-07-01

## Purpose

Exercise the stage-1 handoff packet from run `743` with an output-local
synthetic partial return.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/744_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_partial_return_smoke
```

Key artifacts:

```text
data/stage_one_synthetic_partial_return/
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_partial_return_smoke_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_partial_return_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_partial_return_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage-1 files:                     2
stage-1 file rows:                 2
stage-1 receiver-frequency pairs:  1
stage-1 schema-pass files:         2
stage-1 schema-pass rows:          2
blank required fields:             0
full strict file rows required:    558
full strict pairs required:        279
stage-1 fraction of full rows:     0.003584
strict acceptance ready:           false
synthetic partial return only:     true
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

## Interpretation

The stage-1 packet can be filled and checked locally for the two-row center
pair. This verifies the incremental return mechanics for the smallest BEM/FDTD
producer handoff.

The result is intentionally not a strict acceptance pass. Stage 1 contains only
two of the 558 required strict file rows, so it cannot support real BEM/FDTD
comparison or downstream promotion.

## Decision

Use this run as a stage-1 mechanics smoke only. Keep real BEM/FDTD comparison,
3D validation, GPU/HPC work, field transfer, and field FWI blocked until the
full live producer files are returned and strict-accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_stage1_partial_return_smoke.py
3 passed
```

Figure check:

```text
1744x851, dynamic range=255
```
