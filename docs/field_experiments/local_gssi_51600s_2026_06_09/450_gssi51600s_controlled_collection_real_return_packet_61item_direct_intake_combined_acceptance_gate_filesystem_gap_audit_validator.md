# Field Experiment 450: Combined Acceptance Gate Filesystem Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate run `449` from its generated artifacts.

The validator checks source readiness, staging-directory presence, 33 missing
required files, zero unexpected files, zero accepted files, blocked actions,
downstream guardrails, figure quality, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/450_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
filesystem-gap validation ready:           true
required files:                            33
missing files:                             33
required directories:                      5
filesystem actions:                        4
real packet files present:                 false
real packet accepted:                      false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The passing checks are:

```text
source_chain_ready
directory_scaffold_present_without_unexpected_files
all_required_files_are_still_missing
actions_and_downstream_states_blocked
figure_and_script_snapshots_present
```

## Decision

Run `449` is internally consistent and should be used as the current live
filesystem gap before copying measured field files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validator.py
3 passed
```

Figure check:

```text
2285x840, dynamic range=255
```
