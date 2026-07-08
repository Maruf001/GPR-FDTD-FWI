# BEM Experiment 355: Real-Pair Packet Staging Command Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `354` staging-plan validator with controlled damaged
variants.

The exact run `353` plan should pass. Damaged variants should fail when they
change plan counts, phase order, dependencies, expected output counts,
non-execution semantics, source links, real-packet readiness, downstream
readiness, figure validation, or script snapshots.

This run does not stage packet files, execute a real BEM/FDTD comparison,
calibrate thresholds, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/355_project_core_bem_real_pair_trace_export_packet_staging_command_plan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_staging_command_plan_validation_sensitivity_scenarios.csv
data/project_core_bem_real_pair_trace_export_packet_staging_command_plan_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_trace_export_packet_staging_command_plan_validation_sensitivity.png
docs/PROJECT_CORE_BEM_REAL_PAIR_TRACE_EXPORT_PACKET_STAGING_COMMAND_PLAN_VALIDATION_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    14
expected pass:                1
observed pass:                1
expected failures:            13
observed failures:            13
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 353:        true
rejects damaged variants:     true
real packet files present:    false
real pair execution ready:    false
broad BEM replacement ready:  false
field transfer ready:         false
3D validation ready:          false
GPU work ready:               false
field FWI ready:              false
figure size:                  3365x904
figure dynamic range:         255
```

The validator rejects all damaged variants:

| Scenario | Expected | Observed |
| --- | --- | --- |
| exact run 353 inputs | pass | pass |
| policy label drift | fail | fail |
| phase count drift | fail | fail |
| phase order drift | fail | fail |
| dependency drift | fail | fail |
| output count drift | fail | fail |
| command execution promotion | fail | fail |
| command uncommented | fail | fail |
| source contract link drift | fail | fail |
| real packet promotion | fail | fail |
| real pair promotion | fail | fail |
| downstream promotion | fail | fail |
| figure validation drift | fail | fail |
| script snapshot drift | fail | fail |

## Interpretation

The run `354` validator accepts the exact run `353` staging command plan and
rejects controlled damaged variants for plan-count drift, phase-order drift,
dependency drift, output-count drift, command execution promotion, uncommented
command text, source-link drift, false real-packet promotion, downstream
promotion, figure drift, and script-snapshot drift.

## Decision

Use runs `353-355` as the guarded real-pair packet staging command-plan block.
Keep real BEM/FDTD execution, threshold calibration, broad replacement, 3D
validation, GPU/HPC work, field transfer, and field FWI blocked until an actual
packet is staged and validated.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_trace_export_packet_staging_command_plan_validation_sensitivity.py
3 passed
```
