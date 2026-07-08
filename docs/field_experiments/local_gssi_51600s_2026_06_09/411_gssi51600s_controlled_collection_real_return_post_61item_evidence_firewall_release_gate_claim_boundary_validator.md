# Field Experiment 411: Post Evidence-Firewall Release-Gate Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `410` field claim boundary from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/411_gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      26
guarded claims:                              22
blocked claims:                              4
release-gate rows:                           49
direct real-input release rows:              33
generated follow-up release rows:            16
release-ready rows now:                      0
release-blocked rows now:                    49
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

The validator confirms the release-gate claim, release metrics, blocked rows,
downstream blocks, figure validation, and script snapshots.

## Decision

Use this validator as the artifact guard for run `410`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x832, dynamic range=255
```
