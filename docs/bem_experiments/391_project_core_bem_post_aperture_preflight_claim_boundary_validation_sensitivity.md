# BEM Experiment 391: Post-Aperture Preflight Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `390` validator for the run `389` BEM
post-aperture-preflight claim boundary.

## Output

```text
outputs/bem_experiments/391_project_core_bem_post_aperture_preflight_claim_boundary_validation_sensitivity
```

## Result

```text
scenario count:                     13
expected pass count:                1
observed pass count:                1
expected failure count:             12
observed failure count:             12
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 389:    true
validator rejects damaged variants: true
claim count:                        17
guarded claim count:                14
blocked claim count:                3
metadata fields:                    35
blocking metadata fields:           34
preflight blocking failures:        10
real comparison ready:              false
3D validation ready:                false
field FWI ready:                    false
GPU/HPC ready:                      false
```

The exact run `389` artifacts pass. Twelve damaged variants fail as expected:
source identity drift, claim-count drift, aperture-row drift, metadata-row
evidence drift, false preflight-row demotion, metadata-count drift,
preflight-failure count drift, false target-file promotion, blocked-row support
drift, downstream promotion, figure drift, and script-snapshot drift.

## Interpretation

Runs `389-391` close the current BEM claim-boundary update. The boundary can be
used as the current BEM decision state: the aperture-aware return contract is
guarded, while measured comparison and downstream escalation remain blocked.

## Decision

Use runs `389-391` as the guarded BEM post-aperture-preflight claim-boundary
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_aperture_preflight_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3545x895, dynamic range=255
```
