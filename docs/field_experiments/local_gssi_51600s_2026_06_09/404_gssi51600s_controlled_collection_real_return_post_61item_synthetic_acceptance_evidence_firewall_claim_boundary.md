# Field Experiment 404: Post-Synthetic Evidence Firewall Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic-acceptance evidence firewall from runs `401-403`
into the field claim boundary.

This run records the difference between parser-regression usefulness and
measured-field evidence readiness inside the main field decision boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/404_gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      25
guarded claims:                              21
blocked claims:                              4
evidence firewall ready:                     true
firewall validation ready:                   true
firewall sensitivity ready:                  true
firewall rows:                               49
synthetic parser accepted rows:              49
parser-regression allowed rows:              49
measured-evidence allowed rows:              0
provenance-acceptance allowed rows:          0
archive-acceptance allowed rows:             0
field-FWI allowed rows:                      0
real-replacement required rows:              49
sensitivity scenarios:                       25
sensitivity expected failures:               24
sensitivity unexpected outcomes:             0
synthetic only:                              true
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

The new guarded claim records that all 49 accepted synthetic rows remain
parser-regression rows only. None may be used as measured field evidence,
provenance evidence, archive-acceptance evidence, or field-FWI input. All 49
still need real replacement before evidence promotion.

## Decision

Use this as the current field claim boundary after the synthetic evidence
firewall. Real packet files, measured evidence, provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_acceptance_evidence_firewall_claim_boundary.py
4 passed
```

Figure check:

```text
3941x910, dynamic range=255
```
