# BEM Experiment 376: Real-Pair Return Packet Staging Dependency Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `375` BEM/FDTD return-packet staging-plan validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `374` staging plan and
rejects changes that would alter the stage order, dependency chain, missing-file
counts, readiness states, downstream decision states, figure validation, or
script snapshots.

## Output

```text
outputs/bem_experiments/376_project_core_bem_real_pair_return_packet_staging_dependency_plan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_staging_dependency_plan_validation_sensitivity_scenario_rows.csv
data/project_core_bem_real_pair_return_packet_staging_dependency_plan_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_return_packet_staging_dependency_plan_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                     15
expected pass:                 1
observed pass:                 1
expected failures:             14
observed failures:             14
unexpected outcomes:           0
sensitivity ready:             true
accepts exact run 374:         true
rejects damaged variants:      true
real comparison ready:         false
threshold calibration ready:    false
GPU work ready:                false
field transfer ready:          false
3D validation ready:           false
```

## Interpretation

The run `375` validator accepts the exact run `374` staging plan and rejects
controlled damaged variants for stage-count drift, stage-order drift,
missing-count drift, dependency-chain drift, readiness promotion, downstream
promotion, figure drift, and script-snapshot drift.

## Decision

Use runs `374-376` as the guarded BEM return-packet staging dependency block.
Keep real comparison, threshold calibration, GPU work, field transfer, and 3D
validation blocked until real packet files pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_return_packet_staging_dependency_plan_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3689x913, dynamic range=255
```
