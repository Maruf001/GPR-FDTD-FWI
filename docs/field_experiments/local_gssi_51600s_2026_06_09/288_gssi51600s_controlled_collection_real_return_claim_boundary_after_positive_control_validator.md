# Field Experiment 288: Claim Boundary After Positive Control Validator

Date: 2026-06-28

## Purpose

Validate the saved run `287` field claim boundary from artifacts.

This validator checks claim counts, current real-packet counts, the
synthetic-only positive-control boundary, blocked broader claims, downstream
guardrails, figure validation, and script snapshots.

This uses saved artifacts only. It does not stage real measured field data,
modify the real return inbox, accept provenance, accept a real archive, run
field FWI, or launch GPU/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/288_gssi51600s_controlled_collection_real_return_claim_boundary_after_positive_control_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_claim_boundary_after_positive_control_validator_checks.csv
data/field_controlled_collection_real_return_claim_boundary_after_positive_control_validator_summary.json
figures/field_controlled_collection_real_return_claim_boundary_after_positive_control_validator.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_CLAIM_BOUNDARY_AFTER_POSITIVE_CONTROL_VALIDATOR.md
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
claims:                             7
guarded claims:                     3
blocked claims:                     4
ready claims:                       3
measured requirements complete:     0 / 50
real files present:                 0 / 9
metadata values present:            0 / 32
checksums present:                  0 / 9
acceptance gates ready:             0 / 7
real measured data present:         false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

Run `287` validates as a field claim boundary: process mechanics and
current-state accounting are guarded, but there is still no measured packet, no
provenance acceptance, no controlled evidence, and no field FWI, 3D/HPC, or GPU
escalation.

## Decision

Use run `288` as the validator for the post-positive-control field claim
boundary. Sensitivity hardening remains the next guard step.
