# BEM Experiment 755: Stage-1 Positive Control Comparison Handoff Guard

Date: 2026-07-01

## Purpose

Check whether the accepted stage-1 positive-control intake rows from run `754`
can safely feed the real BEM/FDTD comparison layer.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/755_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard_handoff_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source positive control ready:       true
handoff checks:                      4
passed handoff checks:               4
failed handoff checks:               0
accepted positive-control files:     2
accepted positive-control rows:      2
full strict file rows required:      558
receiver-frequency pairs required:   279
positive-control row fraction:       0.003584
handoff to comparator ready:         false
live return intake accepted as real: false
real BEM/FDTD comparison ready:      false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Handoff checks:

| Check | Observed | Required | Result |
| --- | ---: | ---: | --- |
| stage-1 positive-control intake passes | 2 | 2 | pass |
| full strict row coverage incomplete | 2 | 558 | pass |
| live evidence not promoted | false | false | pass |
| real comparison remains blocked | false | false | pass |

## Interpretation

The stage-1 positive-control rows prove the intake mechanics only. They cover
two rows out of the 558 strict rows required for full BEM/FDTD comparison, so
they cannot feed a real comparison or support a modeling claim.

## Decision

Keep real BEM/FDTD comparison blocked until live producer files cover the full
strict row set and pass the guarded intake path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard.py: pass
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_stage1_positive_control_comparison_handoff_guard.py: pass
```

Figure check:

```text
1492x844, dynamic range=255
```
