# Field Experiment 409: Evidence-Firewall Release-Gate Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `408` validator against controlled damage to the field
release gate.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/409_gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       27
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  26
observed failure scenarios:                  26
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 407:             true
validator rejects damaged variants:          true
real packet files present:                   false
provenance acceptance ready:                 false
archive acceptance ready:                    false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

The validator accepts the exact run `407` release gate and rejects count drift,
row promotion, action-order drift, dependency drift, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift.

## Decision

Use runs `407-409` as the guarded field evidence-firewall release-gate block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_evidence_firewall_release_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3509x886, dynamic range=255
```
