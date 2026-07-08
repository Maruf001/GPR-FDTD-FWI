# Field Experiment 368: Post-61-Item Replacement Ledger Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `365-367` real-return replacement ledger into the field
claim boundary.

This is a claim-boundary update. It does not create measured field evidence,
accept provenance, accept a real archive, run field FWI, launch GPU work, or
run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/368_gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary.png
```

## Result

```text
claim boundary ready:              true
claims:                            19
guarded claims:                    15
blocked claims:                    4
replacement ledger ready:          true
replacement sensitivity ready:     true
unique packet files:               49
packet requirements:               61
duplicate-path requirements:       12
direct collection input files:     33
generated verification files:      16
current measured-evidence payloads:0
field evidence ready:              false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The new guarded claim records that the field return packet needs 33 direct
collection inputs and 16 generated verification outputs while still covering
61 packet requirements.

## Decision

Use this as the current field claim boundary after the replacement-ledger
block. Keep measured evidence, provenance, archive acceptance, field FWI, GPU
work, and field 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary.py
4 passed
```

Figure check:

```text
3941x895, dynamic range=255
```
