# BEM Experiment 389: Post-Aperture Preflight Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the BEM claim boundary after the guarded receiver-aperture and
35-field preflight blocks.

## Output

```text
outputs/bem_experiments/389_project_core_bem_post_aperture_preflight_claim_boundary
```

## Result

```text
claim count:                         17
guarded claim count:                 14
blocked claim count:                 3
base claim count:                    14
base guarded claim count:            11
base blocked claim count:            3
receiver-aperture sensitivity ready: true
metadata addendum ready:             true
metadata fields:                     35
blocking metadata fields:            34
receiver-aperture addendum fields:   5
35-field preflight ready:            true
preflight checks:                    10
preflight blocking failures:         10
target file present:                 false
background file present:             false
metadata file present:               false
real comparison ready:               false
broad BEM replacement ready:         false
field transfer ready:                false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
claim boundary ready:                true
```

This run adds three guarded claims to the previous BEM boundary:

| Claim | Supporting runs | Meaning |
| --- | --- | --- |
| receiver aperture sensitivity guarded | `380-382` | Finite receiver aperture changes the saved Bempp receiver line enough that point receivers are not an unconditional calibrated-comparison assumption. |
| receiver aperture metadata addendum guarded | `383-385` | The preferred return metadata contract now has 35 fields, including five aperture/operator fields. |
| aperture-aware real-return preflight guarded | `386-388` | The refreshed preflight is validated and sensitivity-hardened, but fails closed until target, background, and metadata return files exist. |

## Interpretation

The BEM track now has a stronger handoff contract for future paired BEM/FDTD
returns. The handoff is guarded, but it is still not measured comparison
evidence. The missing files remain decisive.

## Decision

Use run `389` as the current BEM claim boundary after the aperture-aware
preflight block. Keep real comparison, broad BEM replacement, field transfer,
3D validation, field FWI, and GPU/HPC escalation blocked until the refreshed
return packet exists and passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_aperture_preflight_claim_boundary.py
3 passed
```

Figure check:

```text
3653x952, dynamic range=255
```
