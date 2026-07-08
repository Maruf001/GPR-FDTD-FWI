# Field Experiment 443: Direct Intake DZT File Schema Contract

Date: 2026-06-30

## Purpose

Define the acceptance schema for the nine real DZT files required by the direct
field-intake packet.

Runs `440-442` guarded the metadata JSON side. This run guards the measured
data side:

```text
What DZT files, checksums, parser checks, and metadata links must exist before
field files can be accepted?
```

This is a CPU-only contract run. It does not create DZT files, parse measured
DZT files, run FDTD, run FWI, use GPU kernels, run field FWI, run 3D/HPC work,
or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/443_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_dzt_file_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_dzt_check_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_dzt_family_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source receipt audit ready:                true
source receipt validator ready:            true
source receipt sensitivity ready:          true
source metadata schema ready:              true
source metadata validator ready:           true
source metadata sensitivity ready:         true
DZT files required:                        9
DZT file families:                         3
DZT check requirements:                    54
real DZT files present now:                0
nonempty DZT files now:                    0
SHA-256 hashes present now:                0
DZT header parses ready now:               0
trace-geometry parses ready now:           0
linked metadata ready now:                 0
DZT schemas accepted now:                  0
template/synthetic DZT files allowed:      0
DZT schema contract ready:                 true
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The three required DZT families are:

| DZT family | Required files | Present now | Accepted now |
| --- | ---: | ---: | ---: |
| `amplitude_reference` | 3 | 0 | 0 |
| `controlled_profile_repeat` | 3 | 0 | 0 |
| `time_zero_reference` | 3 | 0 | 0 |

Each DZT file has six required checks: `.DZT` extension, nonzero file size,
SHA-256 checksum, GSSI/DZT header parse, trace-geometry parse, and linked
per-file metadata.

## Decision

Use this schema before accepting DZT files or rerunning parser, provenance, or
archive gates. The next field task is a validator for this DZT contract,
followed by sensitivity hardening.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
