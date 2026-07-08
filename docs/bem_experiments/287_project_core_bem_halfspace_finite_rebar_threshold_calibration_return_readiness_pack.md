# BEM Experiment 287: Threshold-Calibration Return Readiness Pack

Date: 2026-06-28

## Purpose

Combine the first-real-pair threshold-calibration template from run `271` with
the guarded post-execution boundary from runs `284-286`.

This run answers the practical BEM handoff question:

```text
What has to be filled when the first real matched BEM/FDTD pair arrives, and
what downstream work remains blocked until that happens?
```

This run does not execute future real-pair commands, inspect real FDTD traces,
compare real BEM/FDTD outputs, set thresholds, run 3D validation, run inversion
scale studies, transfer to field evidence, use GPU/HPC, or run field FWI.

## Output

```text
outputs/bem_experiments/287_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_summary.json
data/figure_validation.csv
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_RETURN_READINESS_PACK.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
readiness rows:                    19
threshold metrics:                 4
required metadata fields:          8
calibrated thresholds:             0
ready metadata fields:             0
guarded return supports:           2
post-return blockers:              5
real-data blockers:                5
template pack ready:               true
post-execution boundary ready:     true
boundary sensitivity ready:        true
command plan guarded:              true
current guard execution guarded:   true
return readiness pack ready:       true
real trace files present:          false
real BEM/FDTD comparison ready:    false
threshold calibration ready:       false
3D validation ready:               false
inversion-scale ready:             false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

## Interpretation

The BEM threshold-calibration handoff is now explicit. The first real matched
BEM/FDTD pair must fill four threshold metrics and eight required metadata
fields. Two return-side supports are already guarded: the command checklist and
the current guard-execution smoke. Five real-data/downstream blockers remain
until real traces, a real paired comparison, and accepted threshold values
exist.

## Decision

Use this run as the first-real-pair BEM threshold-calibration checklist. Do not
set thresholds, promote BEM/FDTD agreement, start 3D validation, start
inversion-scale studies, transfer to field evidence, use GPU/HPC, or run field
FWI until real traces and the first real paired comparison pass the guarded
path.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_return_readiness_pack.py
3 passed
```

Figure validation:

```text
3293x890, dynamic range=255
```
