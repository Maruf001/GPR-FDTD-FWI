# BEM Experiment 308: Bempp Fine-Mesh FDTD Archive Paired Proxy Comparator Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `307` validator for the run `306` paired proxy-comparator
smoke.

This run checks whether the validator accepts the exact saved run `306`
artifact set and rejects controlled damage to row counts, source-readiness
metadata, frequency receiver counts, scale diagnostics, shape markers,
receiver rows, downstream gates, figure validation, and script snapshots.

This is a guardrail run. It does not execute FDTD, run a new BEM solve, perform
a calibrated BEM/FDTD amplitude comparison, validate 3D physics, transfer to
field evidence, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/308_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         35
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        34
observed failure scenarios:        34
unexpected outcomes:               0
sensitivity ready:                 true
exact run 306 accepted:            true
damaged variants rejected:         true
raw amplitude comparison ready:    false
scale calibration ready:           false
real BEM/FDTD comparison ready:    false
3D validation claim ready:         false
field transfer ready:              false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The accepted case is the exact run `306` proxy-comparator artifact set. The 34
rejected damage cases include:

| Damage family | Examples |
| --- | --- |
| Count drift | receiver row removed, frequency row removed |
| Scale drift | scale factor changed, fit metric changed |
| Shape-marker drift | shape marker flipped |
| Receiver-value drift | zero BEM norm, non-finite scaled residual |
| Summary drift | source readiness, row counts, scale summaries, smoke readiness |
| Downstream promotion | real comparison, 3D, field, GPU/HPC, and field FWI flags forced true |
| Artifact drift | missing/weak figure validation and missing script snapshot hashes |

## Interpretation

The proxy-comparator validation branch is now guarded. Runs `306-308` support a
plumbing-level diagnostic only: the 2D scalar proxy export can be compared
against the 3D Bempp scattered-reference table after per-frequency scaling, but
that comparison still shows large frequency-dependent scale factors and is not
a calibrated physical amplitude match.

## Decision

Use runs `306-308` as the guarded proxy-comparator diagnostic path. Real
BEM/FDTD comparison, calibrated scale, 3D validation, field transfer, GPU/HPC
readiness, and field FWI remain blocked.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_paired_proxy_comparator_sensitivity.py
3 passed
```

Figure validation:

```text
4211x883, dynamic range=255
```
