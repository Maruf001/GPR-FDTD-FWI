# Field Experiment 415: Real Packet Acceptance-Gate Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `414` validator against controlled damage to the run `413`
acceptance gate.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/415_gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       29
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  28
observed failure scenarios:                  28
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 413:             true
validator rejects damaged variants:          true
real packet files present:                   false
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Interpretation

The validator accepts the exact run `413` gate and rejects damaged variants for
count drift, premature real-source acceptance, parser/provenance/archive
promotion, measured-evidence promotion, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift.

## Decision

Use runs `413-415` as the guarded field real-packet acceptance-gate block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3653x888, dynamic range=255
```
