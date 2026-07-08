# Field Experiment 410: Post Evidence-Firewall Release-Gate Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded evidence-firewall release gate from runs `407-409` into the
current field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/410_gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      26
guarded claims:                              22
blocked claims:                              4
release gate ready:                          true
release-gate validation ready:               true
release-gate sensitivity ready:              true
release-gate rows:                           49
direct real-input release rows:              33
generated follow-up release rows:            16
release actions:                             6
dependency edges:                            6
release-ready rows now:                      0
release-blocked rows now:                    49
real replacements required:                  49
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

The new guarded claim records the release-gate sequence without changing the
evidence state. The current archive remains synthetic-only and blocked from
measured field evidence.

## Decision

Use this as the current field claim boundary after the evidence-firewall
release-gate block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_evidence_firewall_release_gate_claim_boundary.py
4 passed
```

Figure check:

```text
3941x910, dynamic range=255
```
