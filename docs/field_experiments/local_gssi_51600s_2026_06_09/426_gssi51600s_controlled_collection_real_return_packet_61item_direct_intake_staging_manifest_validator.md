# Field Experiment 426: Direct Intake Staging Manifest Validator

Date: 2026-06-30

## Purpose

Validate run `425`, the direct-intake staging manifest for the 61-item field
packet.

Run `425` turned the 33 open direct real-input gaps into a concrete staging
manifest. This validator checks that the manifest preserves the required
counts, disallows template or synthetic substitutions, keeps parser/provenance
and archive gates after staging, and does not promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/426_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation checks passed:                  5
blocking failures:                         0
direct-intake manifest validation ready:   true
direct real-input slots:                   33
staging actions:                           5
staged real files:                         0
accepted measured-evidence files:          0
real packet files present:                 false
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Decision

Use run `426` as the artifact guard for the run `425` staging manifest. The
field stream remains blocked until real files are staged and pass parser,
provenance, and archive gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_staging_manifest_validator.py
9 passed
```

Figure check:

```text
2177x831, dynamic range=255
```
