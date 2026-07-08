# BEM Experiment 390: Post-Aperture Preflight Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `389` BEM post-aperture-preflight claim boundary from
artifacts.

## Output

```text
outputs/bem_experiments/390_project_core_bem_post_aperture_preflight_claim_boundary_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
claim count:                        17
guarded claim count:                14
blocked claim count:                3
receiver-aperture sensitivity ready: true
metadata addendum ready:            true
35-field preflight ready:           true
metadata fields:                    35
blocking metadata fields:           34
preflight checks:                   10
preflight blocking failures:        10
target file present:                false
background file present:            false
metadata file present:              false
real comparison ready:              false
3D validation ready:                false
field FWI ready:                    false
GPU/HPC ready:                      false
```

The validator checks claim counts, the three new aperture/preflight claim rows,
metadata and preflight metrics, blocked claim rows, downstream blocked states,
figure validation, and script snapshots.

## Interpretation

The run `389` boundary is internally consistent. It guards the aperture-related
BEM handoff contract while preserving the no-go decision for measured
comparison and downstream escalation.

## Decision

Use run `390` as the validator for run `389`. Sensitivity hardening remains
required before closing the block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_aperture_preflight_claim_boundary_validator.py
3 passed
```

Figure check:

```text
3653x929, dynamic range=255
```
