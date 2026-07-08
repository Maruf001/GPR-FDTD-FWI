# BEM Experiment 374: Real-Pair Return Packet Staging Dependency Plan

Date: 2026-06-29

## Purpose

Convert the guarded BEM/FDTD return-packet worksheet into a dependency-ordered
staging plan.

This run clarifies what must be produced first and what can only be derived
after those files exist. It does not stage real packet files, run a real
BEM/FDTD comparison, calibrate thresholds, launch GPU work, transfer to field
evidence, or start 3D validation.

## Output

```text
outputs/bem_experiments/374_project_core_bem_real_pair_return_packet_staging_dependency_plan
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_staging_dependency_plan_stage_rows.csv
data/project_core_bem_real_pair_return_packet_staging_dependency_plan_dependency_edges.csv
data/project_core_bem_real_pair_return_packet_staging_dependency_plan_summary.json
figures/project_core_bem_real_pair_return_packet_staging_dependency_plan.png
scripts/
```

## Result

```text
staging plan ready:                 true
stage count:                        4
dependency edges:                   3
external export stages:             2
derived stages:                     2
packet items:                       34
missing packet items:               34
missing projected trace files:       26
missing metadata/control files:      8
first required stage:               stage_projected_fdtd_trace_files
last required stage:                derive_pairwise_residuals_and_thresholds
acceptance gate can pass now:        false
real comparison ready:              false
threshold calibration ready:         false
GPU work ready:                     false
field transfer ready:               false
3D validation ready:                false
```

The four-stage critical path is:

| Order | Stage | Missing files |
| ---: | --- | ---: |
| 1 | projected FDTD trace export | 26 |
| 2 | primary metadata and references | 4 |
| 3 | frequency export after traces exist | 2 |
| 4 | paired residual and threshold outputs | 2 |

## Interpretation

The 34 missing return-packet files are not one flat task. They form a four-stage
sequence: export 26 projected traces, stage four metadata/reference files,
derive two frequency-export files, and then derive two residual/threshold
files.

The current archive still has zero real packet files. The BEM/FDTD acceptance
gate and real comparison remain blocked.

## Decision

Use run `374` as the BEM return-packet staging sequence. Do not run real
comparison, threshold calibration, GPU work, field transfer, or 3D validation
until these stages are populated and the acceptance gate passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_return_packet_staging_dependency_plan.py
3 passed
```

Figure validation:

```text
3670x969, dynamic range=255
```
