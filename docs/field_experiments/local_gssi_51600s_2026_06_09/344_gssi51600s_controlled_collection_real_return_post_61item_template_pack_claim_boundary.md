# Field Experiment 344: Post 61-Item Template Pack Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the field claim boundary after the corrected 61-item field return
template pack.

This run does not stage measured field files, pass the return-packet
acceptance gate, accept provenance, promote controlled field evidence, launch
field FWI, use GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/344_gssi51600s_controlled_collection_real_return_post_61item_template_pack_claim_boundary
```

## Result

```text
claims:                              15
guarded claims:                      11
blocked claims:                      4
template-pack sensitivity ready:     true
packet requirements:                 61
unique return paths:                 49
template files written:              50
duplicate-path requirements:         12
metadata requirements:               36
metadata template files:             24
antenna metadata addendum records:   4
real packet files present:           false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

## Interpretation

The claim boundary now points the field intake handoff row to runs `341-343`,
the corrected 61-item template-pack block. The boundary is current, but the
measured field packet is still absent.

## Decision

Use this as the current field claim boundary after the corrected template-pack
block. Field evidence, field FWI, GPU work, and field 3D/HPC remain blocked
until real measured items pass the antenna-aware acceptance gate.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_template_pack_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x953, dynamic range=255
```
