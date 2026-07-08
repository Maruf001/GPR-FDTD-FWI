# Experiment 1440: Local 2D Objective-Revision Adoption Checklist

Date: 2026-06-28

## Purpose

Convert the guarded run `1437-1439` local 2D objective-revision claim boundary
into a practical adoption checklist.

This run defines how the supported objective revision can be used locally
without promoting broad-radius, physical-transfer, GPU, field-FWI, or 3D/HPC
claims.

This run uses saved artifacts only. It does not execute new FDTD simulations,
launch GPU work, transfer to field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1440_local_2d_state_consistent_objective_revision_adoption_checklist
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_adoption_checklist_rows.csv
data/local_2d_state_consistent_objective_revision_adoption_checklist_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_adoption_checklist.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_ADOPTION_CHECKLIST.md
scripts/run_local_2d_state_consistent_objective_revision_adoption_checklist.py
scripts/test_local_2d_state_consistent_objective_revision_adoption_checklist.py
scripts/script_snapshot_manifest.json
```

## Result

```text
adoption routes:                    6
local-use ready routes:             2
bounded observations:               1
new-design-required routes:         1
blocked routes:                     2
blocked downstream routes:          3
claim-boundary sensitivity ready:   true
drop-veryhigh local-use ready:      true
majority-vote cross-check ready:    true
veryhigh diagnostic-only ready:     true
promote revised objective now:      false
broad radius tolerance promoted:    false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The guarded objective-revision result is usable as a local checklist. Dropping
`veryhigh` is the preferred local route, majority vote is a local cross-check,
and `veryhigh` is diagnostic only for the tested radius-neighbor branch.
Broad-radius generalization needs a new design, and physical/GPU/field/FWI/3D
routes remain blocked.

## Decision

Use run `1440` as the local 2D objective-revision adoption checklist. Do not
promote broad-radius, physical-transfer, GPU, field-FWI, or 3D/HPC claims from
this branch.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_adoption_checklist.py
3 passed
```

Figure validation:

```text
2789x865, dynamic range=255
```
