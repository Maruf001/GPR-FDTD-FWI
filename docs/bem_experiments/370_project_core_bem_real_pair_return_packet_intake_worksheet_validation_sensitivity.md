# BEM Experiment 370: Real-Pair Return Packet Intake Worksheet Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `369` intake worksheet validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `368` worksheet and
rejects damaged variants covering count drift, action drift, template evidence
promotion, false packet presence, downstream promotion, figure drift, and
script-snapshot drift.

## Output

```text
outputs/bem_experiments/370_project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity_scenario_rows.csv
data/project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity.png
docs/PROJECT_CORE_BEM_REAL_PAIR_RETURN_PACKET_INTAKE_WORKSHEET_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                       15
expected pass:                   1
observed pass:                   1
expected failures:               14
observed failures:               14
unexpected outcomes:             0
sensitivity ready:               true
accepts exact run 368:           true
rejects damaged variants:        true
real packet files present:       false
real comparison ready:           false
threshold calibration ready:     false
GPU work ready:                  false
field transfer ready:            false
3D validation ready:             false
```

## Interpretation

The run `369` validator accepts the exact run `368` worksheet and rejects
damaged variants. This protects the worksheet from being treated as real
evidence or as a substitute for staged packet files.

## Decision

Use runs `368-370` as the guarded BEM return-packet intake worksheet block.
Real comparison remains blocked until real packet files pass the acceptance
gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity.py: pass
tests/test_project_core_bem_real_pair_return_packet_intake_worksheet_validation_sensitivity.py: pass
```

Figure validation:

```text
3473x922, dynamic range=255
```
