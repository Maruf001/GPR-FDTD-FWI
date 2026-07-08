# BEM Experiment 368: Real-Pair Return Packet Intake Worksheet

Date: 2026-06-29

## Purpose

Create a non-evidence intake worksheet for the future BEM/FDTD return packet.

The worksheet converts the guarded 34-item packet contract and return-packet
acceptance gate into explicit templates. The generated files live inside this
run folder only and do not count as real packet files.

This run does not stage real FDTD traces, run BEM/FDTD comparison, calibrate
thresholds, launch GPU work, transfer to field evidence, run field FWI, or
start 3D validation.

## Output

```text
outputs/bem_experiments/368_project_core_bem_real_pair_return_packet_intake_worksheet
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_intake_worksheet_intake_rows.csv
data/project_core_bem_real_pair_return_packet_intake_worksheet_directory_rows.csv
data/project_core_bem_real_pair_return_packet_intake_worksheet_template_file_rows.csv
data/project_core_bem_real_pair_return_packet_intake_worksheet_summary.json
figures/project_core_bem_real_pair_return_packet_intake_worksheet.png
template_packet_root/
docs/PROJECT_CORE_BEM_REAL_PAIR_RETURN_PACKET_INTAKE_WORKSHEET.md
scripts/
```

## Result

```text
packet items:                         34
projected trace templates:            26
metadata/control templates:           8
template files written:               35
expected packet root:                 outputs/bem_experiments/real_pair_fdtd_export_packet
real packet files present:            false
present packet items:                 0
missing packet items:                 34
expected FDTD frequency rows:         234
expected paired residual rows:        117
real BEM/FDTD comparison ready:       false
threshold calibration ready:          false
GPU work ready:                       false
field transfer ready:                 false
3D validation ready:                  false
```

## Interpretation

The worksheet improves packet handoff clarity without changing the evidence
state. It makes the exact 26 projected trace files and eight metadata/control
files explicit, but the real packet root is still empty/absent and the
acceptance gate still cannot pass.

## Decision

Use run `368` as the intake worksheet for future returned BEM/FDTD packet
files. Real comparison, threshold calibration, GPU work, field transfer, field
FWI, and 3D validation remain blocked until real files are staged under the
expected packet root and the return-packet acceptance gate passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_return_packet_intake_worksheet.py
4 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_return_packet_intake_worksheet.py: pass
tests/test_project_core_bem_real_pair_return_packet_intake_worksheet.py: pass
```

Figure validation:

```text
3616x929, dynamic range=255
```
