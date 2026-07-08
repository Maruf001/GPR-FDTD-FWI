# BEM Experiment 080: 3D FDTD Frequency-Bin Extractor Contract

Date: 2026-06-25

## Purpose

Define the extractor contract needed to convert future paired 3D FDTD receiver
time traces into the run `077` frequency-bin import templates.

This is CPU-only implementation planning. It does not launch 3D FDTD, field
FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/bem_experiments/080_project_core_bem_3d_fdtd_frequency_bin_extractor_contract
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_time_trace_schema.csv
data/project_core_bem_3d_fdtd_frequency_bin_extractor_requirements.csv
data/project_core_bem_3d_fdtd_frequency_bin_extractor_contract_summary.json
figures/project_core_bem_3d_fdtd_frequency_bin_extractor_contract.png
docs/PROJECT_CORE_BEM_3D_FDTD_FREQUENCY_BIN_EXTRACTOR_CONTRACT.md
```

## Result

```text
requirements:                         7
ready / implementation / blocked:     4 / 2 / 1
time-trace schema columns:            9
frequency-bin schema columns:         12
extractor contract ready:             true
extractor implemented:                false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
```

## Interpretation

The real FDTD import path now has an explicit input and output contract.
Future 3D FDTD/exporter output must provide target/background receiver time
traces with nine required columns:

```text
run_role, receiver_index, x_m, y_m, z_m, time_s, field_ex, field_ey, field_ez
```

The extractor must convert those traces into the 12-column run `077`
frequency-bin templates and preserve all 124 target plus 124 background
receiver/frequency keys.

Implementation remains blocked by missing real 3D traces, missing complex
frequency extraction, and missing local/external 3D FDTD execution.

## Decision

Use this contract as the implementation target for the next 3D FDTD import
branch. Do not claim real comparison, 3D validation, field FWI, heavy GPU work,
field 3D/HPC, or neural-network training until real traces are converted into
run `077` frequency bins and pass run `075`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_frequency_bin_extractor_contract.py
2 passed
```

Figure check:

```text
1996x808, dynamic range=255
```
