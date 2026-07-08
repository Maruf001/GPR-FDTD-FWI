# Field Experiment 416: Post Real Packet Acceptance-Gate Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded real packet acceptance gate from runs `413-415` into the
field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/416_gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      27
guarded claims:                              23
blocked claims:                              4
acceptance gate ready:                       true
acceptance-gate validation ready:            true
acceptance-gate sensitivity ready:           true
acceptance rows:                             49
direct real-input rows:                      33
generated follow-up rows:                    16
real source rows accepted:                   0
parser-accepted real rows:                   0
provenance-accepted real rows:               0
archive-accepted real rows:                  0
measured-evidence rows ready:                0
blocked acceptance rows:                     49
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Interpretation

The field claim boundary now includes the real-packet acceptance gate. The
gate is ready to evaluate future real packet artifacts, but the current packet
still has zero accepted measured-evidence rows.

## Decision

Use this as the current field claim boundary after the real-packet acceptance
gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary.py
4 passed
```

Figure check:

```text
3869x892, dynamic range=255
```
