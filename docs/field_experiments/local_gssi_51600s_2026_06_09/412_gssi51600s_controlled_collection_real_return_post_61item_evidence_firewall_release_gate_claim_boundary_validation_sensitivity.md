# Field Experiment 412: Post Evidence-Firewall Release-Gate Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `411` validator against controlled damage to the
post-release-gate claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/412_gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       33
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  32
observed failure scenarios:                  32
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 410:             true
validator rejects damaged variants:          true
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

The validator accepts the exact run `410` boundary and rejects count drift,
release-gate claim drift, release-gate metric drift, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift.

## Decision

Use runs `410-412` as the current guarded field post-release-gate
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x886, dynamic range=255
```
