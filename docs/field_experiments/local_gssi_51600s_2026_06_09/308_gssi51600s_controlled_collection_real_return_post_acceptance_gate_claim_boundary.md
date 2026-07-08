# Field Experiment 308: Real-Return Post Acceptance Gate Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the field real-return claim boundary after the guarded acceptance gate
from runs `305-307`.

This run adds the return-packet acceptance gate as a guarded claim while keeping
real packet completion, provenance/archive acceptance, controlled field
evidence, field FWI, GPU work, and field 3D/HPC blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/308_gssi51600s_controlled_collection_real_return_post_acceptance_gate_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_acceptance_gate_claim_boundary_claim_rows.csv
data/gssi51600s_controlled_collection_real_return_post_acceptance_gate_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_acceptance_gate_claim_boundary.png
scripts/
```

## Result

```text
claims:                           12
guarded claims:                   8
blocked claims:                   4
base claims:                      11
base guarded claims:              7
base blocked claims:              4
acceptance gates:                 9
ready acceptance gates:           2
blocked acceptance gates:         7
missing packet items:             57
missing measured DZT files:       9
missing metadata requirements:    32
missing checksum rows:            9
missing acceptance results:       7
real packet files present:        false
provenance acceptance ready:      false
real archive acceptance ready:    false
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
GPU priority:                     none
```

## Interpretation

The field claim boundary now includes the guarded return-packet acceptance
gate. The branch is ready to accept and validate a future measured packet, but
not to promote field evidence.

## Decision

Use run `308` as the current field claim boundary after the return-packet
acceptance gate. Do not promote field evidence or run field FWI until a
complete measured packet is present and passes the gate.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_acceptance_gate_claim_boundary.py
3 passed
```

Figure validation:

```text
3761x953, dynamic range=255
```
