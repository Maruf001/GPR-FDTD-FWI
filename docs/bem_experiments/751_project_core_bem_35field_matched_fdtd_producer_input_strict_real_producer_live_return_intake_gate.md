# BEM Experiment 751: Live Return Intake Gate

Date: 2026-07-01

## Purpose

Create a reusable intake gate for the ten staged live producer files defined by
run `750`.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/751_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_stage_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                 true
stages:                              5
expected live files:                 10
live files present:                  0
missing live files:                  10
live parent directories present:     10
required strict rows:                558
observed live rows:                  0
required real-data cells:            2790
blank or missing real-data cells:    2790
schema-passing files:                0
accepted files:                      0
accepted stages:                     0
stage required rows:                 2;16;60;240;240
stage required real-data cells:      10;80;300;1200;1200
stage missing file counts:           2;2;2;2;2
live return intake accepted:         false
strict acceptance ready:             false
real BEM/FDTD comparison ready:      false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Stage intake state:

| Stage | Contract block | Expected files | Present files | Required rows | Required real-data cells |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | center pair smoke | 2 | 0 | 2 | 10 |
| 2 | center receiver frequency sweep | 2 | 0 | 16 | 80 |
| 3 | center frequency receiver sweep | 2 | 0 | 60 | 300 |
| 4 | midband receiver matrix | 2 | 0 | 240 | 1200 |
| 5 | edgeband receiver matrix | 2 | 0 | 240 | 1200 |

## Interpretation

The BEM/FDTD live-return path now has a direct intake gate. When producer files
arrive, this gate classifies each file as missing, unreadable, row-count
mismatched, missing required fields, blank in required real-data values, or
accepted.

The present state is still a clean pre-return state. All ten parent
directories exist, but none of the ten live files exists. Therefore all 2790
required real-data cells are still unfilled.

## Decision

Use this intake gate when staged live producer files arrive. Keep strict
acceptance, real BEM/FDTD comparison, 3D validation, GPU/HPC work, field
transfer, and field FWI blocked until all ten files pass intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate.py: pass
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_live_return_intake_gate.py: pass
```

Figure check:

```text
2212x854, dynamic range=255
```
