# BEM Experiment 752: Live Return Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `751` BEM/FDTD live-return intake gate from its output
artifacts.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/752_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source intake gate ready:        true
validation checks:               7
passed validation checks:        7
failed validation checks:        0
expected live files:             10
missing live files:              10
required real-data cells:        2790
blank required real-data cells:  2790
live return intake accepted:     false
strict acceptance ready:         false
real BEM/FDTD comparison ready:  false
GPU/HPC ready:                   false
field transfer ready:            false
field FWI ready:                 false
```

Validation checks:

| Check | Result |
| --- | --- |
| Source intake gate ready | pass |
| Ten live files represented | pass |
| Current live state remains absent | pass |
| Stage shape preserved | pass |
| Acceptance remains blocked | pass |
| Downstream states remain blocked | pass |
| Figure and script snapshots present | pass |

## Interpretation

The saved intake gate is internally consistent. It sees all ten expected live
producer files, preserves the five-stage row shape, confirms that all ten
files are still absent, and keeps strict acceptance plus real BEM/FDTD
comparison blocked.

## Decision

Use run `751` as the live-return intake gate and run `752` as its saved-artifact
validator. Sensitivity hardening remains the next useful step before relying on
the gate for damaged future returns.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
