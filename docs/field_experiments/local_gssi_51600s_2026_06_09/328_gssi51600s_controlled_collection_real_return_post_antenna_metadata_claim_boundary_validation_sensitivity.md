# Field Experiment 328: Post-Antenna Metadata Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `327` validator for the run `326` controlled-field
post-antenna-metadata claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/328_gssi51600s_controlled_collection_real_return_post_antenna_metadata_claim_boundary_validation_sensitivity
```

## Result

```text
scenario count:                     14
expected pass count:                1
observed pass count:                1
expected failure count:             13
observed failure count:             13
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 326:    true
validator rejects damaged variants: true
claim count:                        15
guarded claim count:                11
blocked claim count:                4
updated packet items:               61
updated metadata requirements:      36
missing packet items:               61
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The exact run `326` artifacts pass. Thirteen damaged variants fail as expected:
source identity drift, claim-count drift, antenna-row status drift,
antenna-row evidence drift, addendum readiness drift, packet-count drift,
metadata-count drift, missing-count drift, blocked-row support drift,
downstream promotion, GPU-priority drift, figure drift, and script-snapshot
drift.

## Interpretation

Runs `326-328` close the current field claim-boundary update. The current
measured packet target is 61 items. Field evidence remains blocked until that
packet exists and passes validation.

## Decision

Use runs `326-328` as the guarded field post-antenna-metadata claim-boundary
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_antenna_metadata_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x895, dynamic range=255
```
