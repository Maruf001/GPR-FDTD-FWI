# Field Experiment 408: Evidence-Firewall Release-Gate Validator

Date: 2026-06-29

## Purpose

Validate the saved run `407` release gate from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/408_gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
release-gate validation ready:               true
release-gate rows:                           49
direct real-input release rows:              33
generated follow-up release rows:            16
release actions:                             6
dependency edges:                            6
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

The validator confirms the release-gate row counts, direct/generated split,
action order, dependency order, downstream blocking, figure validation, and
script snapshots.

## Decision

Use this validator as the artifact guard for run `407`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validator.py
6 passed
```

Figure check:

```text
2645x830, dynamic range=255
```
