# Field Experiment 315: Real-Return Post-Intake Worksheet Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `314` field claim boundary from artifacts.

This run checks that the new intake-worksheet claim, claim counts, blocked
claim rows, field guardrails, figure output, and script snapshots remain
internally consistent.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/315_gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:                 7
passed checks:                     7
failed checks:                     0
claim count:                       13
guarded claims:                    9
blocked claims:                    4
field intake worksheet ready:      true
accepts exact run 311:             true
rejects damaged variants:          true
missing packet items:              57
missing measured DZT files:        9
missing metadata requirements:     32
missing checksum rows:             9
missing acceptance-result files:   7
real packet files present:         false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The saved run `314` boundary is internally consistent. The intake worksheet is
guarded as a non-evidence handoff artifact, and all measured-data dependent
field claims remain blocked.

## Decision

Use run `315` as the validator for the run `314` field post-intake claim
boundary. Sensitivity hardening remains required before treating the boundary
block as guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3689x929, dynamic range=255
```
