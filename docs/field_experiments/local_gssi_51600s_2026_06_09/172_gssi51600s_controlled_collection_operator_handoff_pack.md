# Field Experiment 172: Controlled Collection Operator Handoff Pack

Date: 2026-06-25

## Purpose

Consolidate the controlled-collection checklist, checksum ledger, and archive
layout contract into one operator-facing handoff sequence.

This run answers the practical collection-day question:

```text
What exactly should the operator do, in what order, to turn the current
controlled-collection plan into a real archive that can be checked by the
intake, checksum, structural, and provenance gates?
```

This is a CPU-only planning and packaging run. It does not create measured
field evidence, copy DZT files, run DZT preprocessing, launch field FWI, use
GPU/HPC, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/172_gssi51600s_controlled_collection_operator_handoff_pack
```

Key artifacts:

```text
data/field_controlled_collection_operator_sequence.csv
data/field_controlled_collection_operator_file_handoff.csv
data/field_controlled_collection_operator_metadata_handoff.csv
data/field_controlled_collection_operator_gate_crosswalk.csv
data/field_controlled_collection_operator_handoff_pack_summary.json
figures/field_controlled_collection_operator_handoff_pack.png
docs/FIELD_COLLECTION_OPERATOR_HANDOFF_PACK.md
scripts/run_gssi_field_controlled_collection_operator_handoff_pack.py
scripts/test_gssi_field_controlled_collection_operator_handoff_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
operator sequence steps:          8
file handoff rows:                9
metadata value handoff rows:      11
metadata artifact count:          3
gate crosswalk rows:              6
controlled profile files:         3
time-zero reference files:        3
amplitude-reference files:        3
script snapshots:                 2
ready for operator handoff:       true
ready for collection-day use:     true
ready for provenance acceptance:  false
ready for structural rerun:       false
field FWI ready:                  false
GPU/HPC ready:                    false
```

The eight operator phases are:

| Step | Phase | Purpose |
| ---: | --- | --- |
| 1 | prepare_archive | create the archive directories |
| 2 | write_metadata | fill real metadata artifacts |
| 3 | archive_real_files | copy the nine measured DZT files |
| 4 | checksum_real_files | hash the archived files and fill the ledger |
| 5 | run_checksum_preflight | require zero checksum-ledger findings |
| 6 | run_intake_preflight | require zero intake-manifest findings |
| 7 | rerun_packet_gates | rerun structural and provenance validation |
| 8 | hold_field_fwi | keep field FWI/GPU/HPC blocked until all gates pass |

## Interpretation

The field-side blocker is now operationally packaged rather than just
diagnosed. Runs `167`, `168`, and `171` define what must be collected, how the
nine real files must be hashed, and where files and metadata belong in the
archive. This run joins those pieces into one handoff sequence.

This is still not measured field evidence. The repository now has a concrete
operator packet, but the real archive must be filled and then pass checksum,
intake, structural, and provenance gates before any measured-field scientific
claim, field FWI, heavy GPU work, field 3D/HPC, or neural-network training.

## Decision

Use this pack as the current field-collection handoff artifact. Do not launch
field FWI, heavy GPU work, field 3D/HPC, or neural-network training from the
current dry-run archive.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_operator_handoff_pack.py
5 passed
```

Figure check:

```text
field_controlled_collection_operator_handoff_pack.png
2142x845, dynamic range=255
```
