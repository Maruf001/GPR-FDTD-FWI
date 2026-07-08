# Field Experiment 380: Post Operator-Handoff Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `377-379` operator handoff manifest into the current
field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/380_gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary.png
```

## Result

```text
claims:                            21
guarded claims:                    17
blocked claims:                    4
operator handoff ready:            true
handoff sensitivity ready:         true
stages:                            4
handoff rows:                      49
direct operator items:             33
generated follow-up items:         16
packet requirements:               61
duplicate-path requirements:       12
current measured-evidence payloads:0
generated outputs ready now:       false
real packet files present:         false
provenance acceptance ready:       false
archive acceptance ready:          false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
claim boundary ready:              true
```

The new guarded claim records the operator handoff manifest and keeps the
measured-evidence and downstream-compute blockers explicit.

## Decision

Use this as the current field claim boundary after the operator-handoff block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary.py
4 passed as part of the 12-test focused set
```

Figure check:

```text
3941x910, dynamic range=255
```
