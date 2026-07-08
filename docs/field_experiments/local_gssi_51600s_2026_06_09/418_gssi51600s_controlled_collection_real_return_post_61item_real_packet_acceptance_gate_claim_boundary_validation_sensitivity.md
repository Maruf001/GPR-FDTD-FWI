# Field Experiment 418: Post Real Packet Acceptance-Gate Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `417` validator against controlled damage to the run `416`
field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/418_gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       35
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  34
observed failure scenarios:                  34
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 416:             true
validator rejects damaged variants:          true
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Interpretation

The validator accepts the exact run `416` boundary and rejects damaged variants
for claim-count drift, acceptance-gate readiness drift, acceptance-gate metric
drift, premature field-evidence promotion, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift.

## Decision

Use runs `416-418` as the current guarded field post-real-packet-acceptance
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_real_packet_acceptance_gate_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3671x883, dynamic range=255
```
