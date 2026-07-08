# Field Experiment 403: Synthetic Acceptance Evidence Firewall Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `402` validator against controlled evidence-firewall
damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/403_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     25
expected pass scenarios:                   1
observed pass scenarios:                   1
expected failure scenarios:                24
observed failure scenarios:                24
unexpected outcomes:                       0
validation sensitivity ready:              true
validator accepts exact run 401:           true
validator rejects damaged variants:        true
real packet files present:                 false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

## Decision

Use runs `401-403` as the guarded synthetic-acceptance evidence-firewall block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x889, dynamic range=255
```
