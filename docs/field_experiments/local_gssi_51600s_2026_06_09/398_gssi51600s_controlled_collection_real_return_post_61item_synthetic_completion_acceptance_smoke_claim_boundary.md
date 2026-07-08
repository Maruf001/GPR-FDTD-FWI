# Field Experiment 398: Post-Synthetic Completion Smoke Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic completion acceptance-smoke block from runs
`395-397` into the field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/398_gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary.png
```

## Result

```text
claims:                                  24
guarded claims:                          20
blocked claims:                          4
synthetic acceptance smoke ready:        true
synthetic smoke validation ready:        true
synthetic smoke sensitivity ready:       true
filled rows:                             49
required completion cells filled:        245
synthetic parser accepted rows:          49
synthetic parser rejected rows:          0
synthetic measured-evidence rows:        0
sensitivity scenarios:                   31
sensitivity expected failures:           30
sensitivity unexpected outcomes:         0
synthetic only:                          true
real packet files present:               false
provenance acceptance ready:             false
archive acceptance ready:                false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The new guarded claim records that the parser acceptance path works for a
complete worksheet shape, while making clear that the accepted rows are
synthetic and not measured field evidence.

## Decision

Use this as the current field claim boundary after the synthetic
acceptance-path block. Real evidence, provenance, archive acceptance, field
FWI, GPU work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary.py
4 passed
```

Figure check:

```text
3941x910, dynamic range=255
```
