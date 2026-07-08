# BEM Experiment 754: Stage-1 Intake Positive Control Smoke

Date: 2026-07-01

## Purpose

Exercise the positive path of the guarded BEM/FDTD live-return intake gate using
two output-local stage-1 control files.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/754_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke
```

Key artifacts:

```text
data/stage1_positive_control/fdtd_source_hash_manifest_stage1_positive_control.csv
data/stage1_positive_control/fdtd_scattered_norm_values_stage1_positive_control.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                    true
positive-control files:                 2
positive-control files present:         2
positive-control accepted files:        2
required rows:                          2
observed rows:                          2
required real-data cells:               10
blank required real-data cells:         0
real FDTD exported true count:          2
returned value nonblank count:          2
positive-control statuses:              accepted;accepted
live return intake accepted as real:    false
strict acceptance ready:                false
real BEM/FDTD comparison ready:         false
GPU/HPC ready:                          false
field transfer ready:                   false
field FWI ready:                        false
```

Accepted output-local files:

| File key | Rows | Required cells | Intake status |
| --- | ---: | ---: | --- |
| fdtd_source_hash_manifest | 1 | 5 | accepted |
| fdtd_scattered_norm_values | 1 | 5 | accepted |

## Interpretation

The intake gate's positive path works for the smallest BEM/FDTD return unit.
Two output-local stage-1 files, one source-hash manifest row and one scattered
norm row, pass the same field-level checks used by the live intake gate.

This is mechanics coverage only. It does not replace live producer files and
does not make real BEM/FDTD comparison ready.

## Decision

Use this as a stage-1 positive-control smoke for the intake gate. Keep real
BEM/FDTD comparison, strict acceptance, 3D validation, GPU/HPC work, field
transfer, and field FWI blocked until real live producer files arrive and pass
the guarded intake path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke.py
2 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke.py: pass
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage1_positive_control_smoke.py: pass
```

Figure check:

```text
1492x851, dynamic range=255
```
