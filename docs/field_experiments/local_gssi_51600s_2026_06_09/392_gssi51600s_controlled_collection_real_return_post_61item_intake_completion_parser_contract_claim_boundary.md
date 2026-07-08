# Field Experiment 392: Post-Parser-Contract Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded intake-completion parser contract from runs `389-391` into
the field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/392_gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary.png
```

## Result

```text
claims:                              23
guarded claims:                      19
blocked claims:                      4
parser contract ready:               true
parser sensitivity ready:            true
worksheet rows:                      49
direct real-input rows:              33
generated follow-up rows:            16
completion rules:                    6
required completion columns:         5
status rules:                        8
blank completion cells:              294
parser-accepted current rows:        0
parser-rejected current rows:        49
current measured-evidence rows:      0
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

The new guarded claim records that the future filled worksheet must pass the
parser contract before any real-return packet can move toward provenance or
archive acceptance.

## Decision

Use this as the current field claim boundary after the parser-contract block.
Measured evidence, provenance acceptance, archive acceptance, field FWI, GPU
work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary.py
4 passed
```

Figure check:

```text
3941x910, dynamic range=255
```
