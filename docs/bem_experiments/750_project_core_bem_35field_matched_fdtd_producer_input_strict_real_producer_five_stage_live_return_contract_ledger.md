# BEM Experiment 750: Five-Stage Live Return Contract Ledger

Date: 2026-07-01

## Purpose

Combine the stage-1 through stage-5 live return contracts into one strict
producer checklist.

This run does not create real FDTD evidence, accept live producer files, run
FDTD, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/750_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_five_stage_live_return_contract_ledger
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_five_stage_live_return_contract_ledger_stage_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_five_stage_live_return_contract_ledger_expected_file_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_five_stage_live_return_contract_ledger_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_five_stage_live_return_contract_ledger.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stages:                          5
expected live files:             10
live files present:              0
live parent directories present: 10
missing live files:              10
strict file rows covered:        558
receiver-frequency pairs covered:279
stage row counts:                2, 16, 60, 240, 240
stage pair counts:               1, 8, 30, 120, 120
cumulative row counts:           2, 18, 78, 318, 558
cumulative pair counts:          1, 9, 39, 159, 279
contract sequence closed:        true
strict acceptance ready:         false
real BEM/FDTD comparison ready:  false
GPU/HPC ready:                   false
field transfer ready:            false
field FWI ready:                 false
```

## Interpretation

The staged BEM/FDTD return contract is now complete as a checklist. The five
stages cover all 279 receiver-frequency pairs and all 558 strict file rows:

| Stage | Contract block | File rows | Pairs | Cumulative rows | Cumulative pairs |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | center pair smoke | 2 | 1 | 2 | 1 |
| 2 | center receiver frequency sweep | 16 | 8 | 18 | 9 |
| 3 | center frequency receiver sweep | 60 | 30 | 78 | 39 |
| 4 | midband receiver matrix | 240 | 120 | 318 | 159 |
| 5 | edgeband receiver matrix | 240 | 120 | 558 | 279 |

All ten expected live files have parent directories, but none of the live
files is present yet. The sequence is therefore complete as a return contract
and incomplete as measured comparison evidence.

## Decision

Use this ledger as the complete live-return checklist for the matched
BEM/FDTD producer. Keep strict acceptance, real BEM/FDTD comparison, 3D
validation, GPU/HPC work, field transfer, and field FWI blocked until all ten
live files are returned and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_five_stage_live_return_contract_ledger.py
4 passed
```

Figure check:

```text
2140x846, dynamic range=255
```
