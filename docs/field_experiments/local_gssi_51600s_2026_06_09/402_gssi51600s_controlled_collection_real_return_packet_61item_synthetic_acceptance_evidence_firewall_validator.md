# Field Experiment 402: Synthetic Acceptance Evidence Firewall Validator

Date: 2026-06-29

## Purpose

Validate the synthetic acceptance evidence firewall from run `401`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/402_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
firewall validation ready:                 true
firewall rows:                             49
parser-regression allowed rows:            49
measured-evidence allowed rows:            0
real-replacement required rows:            49
real packet files present:                 false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

## Decision

Use this validator as the artifact guard for run `401`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_acceptance_evidence_firewall_validator.py
4 passed
```

Figure check:

```text
2609x840, dynamic range=255
```
