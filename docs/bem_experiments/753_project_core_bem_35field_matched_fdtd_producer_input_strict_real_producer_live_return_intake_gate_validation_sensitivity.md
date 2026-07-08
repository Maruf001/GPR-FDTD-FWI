# BEM Experiment 753: Live Return Intake Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `752` validator for the BEM/FDTD live-return intake gate.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/753_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:             true
sensitivity scenarios:              9
expected pass scenarios:            1
expected fail scenarios:            8
observed pass scenarios:            1
observed fail scenarios:            8
unexpected outcomes:                0
damaged scenarios:                  8
damaged scenarios rejected:         8
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source not ready | fail | fail | source intake gate ready |
| missing count drift | fail | fail | current live state remains absent |
| file status damage | fail | fail | current live state remains absent |
| stage shape damage | fail | fail | stage shape is preserved |
| false acceptance | fail | fail | acceptance remains blocked |
| downstream promotion | fail | fail | downstream states remain blocked |
| figure damage | fail | fail | figure and script snapshots are present |
| snapshot damage | fail | fail | figure and script snapshots are present |

## Interpretation

The validator accepts only the exact saved intake-gate state. It rejects damaged
source readiness, live-file counts, per-file status, stage row shape, false
acceptance, downstream promotion, damaged figure validation, and missing script
snapshots.

## Decision

Use runs `751-753` as the guarded BEM live-return intake block. The current
BEM/FDTD path remains blocked on real producer files, but the receipt side is
now ready to classify future files and reject damaged states.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validation_sensitivity.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```
