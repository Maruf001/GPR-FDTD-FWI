# Field Experiment 447: Direct Intake Combined Acceptance Gate Validator

Date: 2026-06-30

## Purpose

Validate run `446` from its artifacts.

The combined gate should pass only when the metadata and DZT source contracts
are ready, the 33-file and 216-requirement counts match, no live files or
accepted evidence are promoted, all actions remain blocked, and figure/script
snapshots are present.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/447_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
combined gate validation ready:            true
total required files:                      33
total file/check/field requirements:       216
remaining acceptance blockers:             4
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The five validation checks confirm:

```text
source_chain_ready                         pass
combined_requirement_counts                pass
gate_is_contract_only                      pass
actions_and_downstream_states_blocked      pass
figure_and_script_snapshots_present        pass
```

## Decision

Use this validator as the artifact guard for run `446`. The next field task is
a validation-sensitivity run before any parser, provenance, archive, field FWI,
or field 3D/HPC rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
