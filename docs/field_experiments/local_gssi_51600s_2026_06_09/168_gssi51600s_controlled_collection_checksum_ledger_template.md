# Field Experiment 168: Controlled Collection Checksum Ledger Template

Date: 2026-06-25

## Purpose

Turn the nine real-file requirements from run `167` into a checksum ledger
template and command sheet.

This is a no-data operational artifact. It does not create measured field
evidence, run DZT preprocessing, launch field FWI, use GPU/HPC, or train neural
networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/168_gssi51600s_controlled_collection_checksum_ledger_template
```

Key artifacts:

```text
data/field_controlled_collection_checksum_ledger_template.csv
data/field_controlled_collection_checksum_commands.csv
data/field_controlled_collection_checksum_ledger_template_summary.json
figures/field_controlled_collection_checksum_ledger_template.png
docs/FIELD_COLLECTION_CHECKSUM_LEDGER_TEMPLATE.md
```

## Result

```text
ledger rows:                         9
command rows:                        9
controlled profile files:            3
time-zero reference files:           3
amplitude reference files:           3
ready for collection-day use:        true
ready for provenance acceptance:     false
ready for structural rerun:          false
field FWI ready:                     false
GPU work ready:                      false
field 3D/HPC ready:                  false
```

The command sheet contains one `sha256sum` command template per expected file:

```text
3 controlled profile-repeat DZT files
3 time-zero reference DZT files
3 amplitude-reference DZT files
```

## Interpretation

The nine required real files now have a checksum ledger template. This reduces
collection-day transcription ambiguity but does not create measured evidence.

## Decision

Use this ledger when the real files are archived. Keep provenance acceptance,
field FWI, GPU work, and field 3D/HPC blocked until real paths and SHA-256
values pass preflight.

## Validation

Figure check:

```text
1564x807, dynamic range=255
```
