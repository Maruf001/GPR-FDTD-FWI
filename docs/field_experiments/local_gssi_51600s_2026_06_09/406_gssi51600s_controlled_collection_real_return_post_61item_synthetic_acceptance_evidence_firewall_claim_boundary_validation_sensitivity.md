# Field Experiment 406: Post-Synthetic Evidence Firewall Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `405` validator with controlled damage to claim counts,
firewall readiness, firewall metrics, claim support, downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/406_gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       33
expected passes:                             1
observed passes:                             1
expected failures:                           32
observed failures:                           32
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 404:             true
validator rejects damaged variants:          true
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Decision

Use runs `404-406` as the current guarded field
post-synthetic-acceptance-firewall claim-boundary block. The current field
archive remains blocked from measured-evidence promotion and downstream field
FWI.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x887, dynamic range=255
```
