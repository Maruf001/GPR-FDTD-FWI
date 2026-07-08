# Experiment 1833: BEM Stage-1 Complex FDTD External Artifact Acceptance Watchlist

Date: 2026-07-01

## Purpose

List the two live external artifacts required before the BEM stage-1 complex
FDTD producer can be authorized.

This run reads the existing action rollup and hygiene audit. It does not write
live approval files, write returned FDTD files, run FDTD, compare BEM/FDTD,
transfer to field, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1833_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist
```

Key artifacts:

```text
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_artifact_rows.csv
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_summary.json
figures/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist.png
```

## Result

```text
source rollup ready:                    true
source hygiene ready:                   true
source hygiene validation ready:        true
source hygiene sensitivity ready:       true
watchlist artifacts:                    2
required live files:                    2
present live files:                     0
missing live files:                     2
accepted artifacts:                     0
parent directories present:             2
source templates present:               1
live approval file present:             false
BEM partial-return file present:        false
FDTD producer authorized now:           false
FDTD executed now:                      false
real BEM/FDTD comparison ready:         false
field transfer ready:                   false
3D/HPC ready:                           false
gpu priority:                           none
```

The two required artifacts are:

```text
APPROVED_BEM_STAGE1_COMPLEX_FDTD_RETURN.json
project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_partial.csv
```

## Interpretation

The 2D stage-1 path is cleanly blocked, not ambiguous. The approval parent and
partial-return parent directories exist, but the live approval JSON and the
partial-return CSV are both absent.

## Decision

Keep FDTD execution and BEM/FDTD comparison blocked until both live artifacts
exist and pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist.py
2 passed
```

Figure check:

```text
2466x837, dynamic range=255
```
