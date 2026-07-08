# Field Experiment 256: Controlled Archive Real Return Post-Execution Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `255` post-execution boundary validator.

This run does not execute future real-archive commands, inspect real measured
files, accept a real archive, promote field evidence, run field FWI, or launch
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/256_gssi51600s_controlled_archive_real_return_post_execution_boundary_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_post_execution_boundary_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_post_execution_boundary_sensitivity_summary.json
figures/field_controlled_archive_real_return_post_execution_boundary_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_POST_EXECUTION_BOUNDARY_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_return_post_execution_boundary_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_return_post_execution_boundary_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         24
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        23
observed failure scenarios:        23
unexpected outcomes:               0
sensitivity ready:                 true
boundary validation ready:         true
source boundary ready:             true
future real-archive commands run:  false
real files present:                false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The post-execution real-return boundary validator accepts the exact run `254`
boundary and rejects controlled damage to rows, counts, guards, and false
real/downstream readiness.

## Decision

Use runs `254-256` as the guarded field post-execution boundary. Real measured
files remain required before archive acceptance.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_post_execution_boundary_sensitivity.py
5 passed
```

Figure validation:

```text
4121x888, dynamic range=255
```
