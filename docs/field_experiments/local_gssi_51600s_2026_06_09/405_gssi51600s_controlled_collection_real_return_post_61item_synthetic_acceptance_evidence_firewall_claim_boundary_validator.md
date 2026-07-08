# Field Experiment 405: Post-Synthetic Evidence Firewall Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `404` from saved artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/405_gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation passes:                           5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      25
guarded claims:                              21
blocked claims:                              4
firewall rows:                               49
parser-regression allowed rows:              49
measured-evidence allowed rows:              0
real-replacement required rows:              49
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Decision

Use this validator as the artifact guard for run `404`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
