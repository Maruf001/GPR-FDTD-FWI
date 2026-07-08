# Field Experiment 260: Controlled Collection Real-Return Staging Contract

Date: 2026-06-28

## Purpose

Convert the guarded collection-return readiness pack from run `257` into a
concrete staging contract for a future real controlled collection return.

This run defines the file slots, metadata slots, checksum requirements, and
ordered gates that must be filled before the controlled field archive can be
accepted.

It does not create or inspect real measured files, accept a real archive,
promote field evidence, run field FWI, or launch field 3D/HPC/GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/260_gssi51600s_controlled_collection_real_return_staging_contract
```

Key artifacts:

```text
data/field_controlled_collection_real_return_file_slots.csv
data/field_controlled_collection_real_return_global_metadata_slots.csv
data/field_controlled_collection_real_return_gate_rows.csv
data/field_controlled_collection_real_return_staging_contract_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_staging_contract.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_STAGING_CONTRACT.md
scripts/run_gssi_field_controlled_collection_real_return_staging_contract.py
scripts/test_gssi_field_controlled_collection_real_return_staging_contract.py
scripts/script_snapshot_manifest.json
```

## Result

```text
file slots:                         9
controlled profile file slots:      3
time-zero reference file slots:     3
amplitude reference file slots:     3
global metadata fields:             11
file metadata cells:                21
checksum requirements:              9
gate rows:                          7
staging contract ready:             true
real files present:                 false
global metadata present:            false
file metadata present:              false
checksums present:                  false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The nine required file slots are:

| File role | Count | Contract location |
| --- | ---: | --- |
| Controlled profile repeat | 3 | `raw/profiles/controlled_profile_repeat_*.DZT` |
| Time-zero reference | 3 | `references/time_zero/time_zero_reference_*.DZT` |
| Amplitude reference | 3 | `references/amplitude/amplitude_reference_*.DZT` |

## Interpretation

The future real-return package now has a concrete staging shape: nine measured
DZT file slots, eleven global metadata fields, twenty-one per-file metadata
cells, nine checksum requirements, and seven ordered gates before any field
evidence or downstream FWI/3D/GPU promotion.

## Decision

Use run `260` as the field real-return staging contract. Real files, real
metadata, checksums, structural validation, and provenance validation remain
required before archive acceptance or downstream field work.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_staging_contract.py
3 passed
```

Figure validation:

```text
3221x869, dynamic range=255
```
