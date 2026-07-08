# BEM Experiment 595: Matched FDTD Input-Bound Exporter Real Staging Closure Plan

Date: 2026-06-30

## Purpose

Reduce the real BEM/FDTD external staging gap from runs `592-594` into a short
closure plan.

Runs `592-594` prove that the synthetic exporter roundtrip did not pollute the
locked external staging paths. This run asks what remains physically required
before real BEM/FDTD comparison can proceed.

This run does not copy real FDTD files, execute the exporter, accept return
files, run real BEM/FDTD comparison, start GPU/HPC work, transfer to field
work, or run field FWI.

## Output

```text
outputs/bem_experiments/595_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_missing_file_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_closure_group_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan.png
scripts/
```

## Result

```text
source guard ready:                    true
source validation ready:               true
source sensitivity ready:              true
staged files required:                 4
real input files required:             2
accepted return files required:        2
present files:                         0
accepted files:                        0
closure groups:                        4
ready groups:                          0
real input phase ready:                false
exporter execution ready:              false
real BEM/FDTD comparison ready:        false
3D validation claim ready:             false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
gpu priority:                          none
```

The four closure groups are:

| Priority | Closure group | Required files | Present | Accepted |
| ---: | --- | ---: | ---: | ---: |
| 1 | supply real matched-FDTD input CSVs | 2 | 0 | 0 |
| 2 | rerun receipt gate on real input CSVs | 2 | 0 | 0 |
| 3 | run input-bound exporter to create accepted return CSVs | 2 | 0 | 0 |
| 4 | rerun receipt, exporter, and BEM/FDTD comparison gates | 4 | 0 | 0 |

## Interpretation

The blocker is now concrete. The BEM side does not need another synthetic
roundtrip before real comparison; it needs two real matched-FDTD input CSVs,
then the input-bound exporter must create two accepted return CSVs. Only after
those four files pass the gates should real BEM/FDTD comparison be rerun.

## Decision

Use run `595` as the current BEM/FDTD handoff closure plan. Keep real
BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, and
field FWI blocked until both real input CSVs and both accepted return CSVs are
present and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_closure_plan.py

3 passed
```

Figure validation:

```text
2285x847, dynamic range=255
```
