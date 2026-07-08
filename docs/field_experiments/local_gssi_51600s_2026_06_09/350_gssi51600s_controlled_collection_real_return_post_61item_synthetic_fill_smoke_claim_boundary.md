# Field Experiment 350: Post-Synthetic-Fill-Smoke Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic consumer-smoke result from runs `347-349` into the
current field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/350_gssi51600s_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary
```

## Result

```text
claims:                              16
guarded claims:                      12
blocked claims:                      4
synthetic smoke sensitivity ready:   true
packet requirements:                 61
unique return paths:                 49
synthetic packet files:              49
synthetic packet items present:      61
open action groups:                  0
synthetic packet structurally full:  true
synthetic packet is measured:        false
real packet files present:           false
field evidence ready:                false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

The field boundary now records that the 61-item template pack is structurally
fillable. The new claim does not promote synthetic files to measured evidence.

## Validation

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x953, dynamic range=255
```
