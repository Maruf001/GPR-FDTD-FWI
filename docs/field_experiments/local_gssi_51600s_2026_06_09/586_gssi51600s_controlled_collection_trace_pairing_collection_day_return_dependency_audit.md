# Field Experiment 586: Controlled Collection Return Dependency Audit

Date: 2026-07-01

## Purpose

Split the controlled collection return blocker into metadata-only records and
collection-coupled measured radar files.

Runs `580-585` guarded the preflight and claim boundary for the thirty-three
field return items. This run makes the next collection step more specific by
separating records that can be prepared without measured DZT files from records
that must be collected with measured DZT files.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/586_gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit_stage_dependency_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit_action_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source preflight ready:                    true
source claim boundary ready:               true
source claim sensitivity ready:            true
stages:                                    6
required return items:                     33
metadata JSON items:                       24
measured DZT items:                        9
metadata preparable without DZT:           15
metadata paired with DZT:                  9
collection-coupled stages:                 3
collection-coupled items:                  18
preflight-passed items:                    0
ready stages:                              0
action groups:                             5
ready action groups:                       0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

## Interpretation

The field blocker is now split into two practical classes:

| Class | Count | Meaning |
| --- | ---: | --- |
| Global/setup/closeout metadata | 15 | Can be prepared separately where values are known |
| Measured DZT files | 9 | Require controlled collection |
| Per-file metadata paired with DZT | 9 | Must travel with the measured DZT files |

The coupled collection stages are controlled profile repeats, time-zero
references, and amplitude references. Each requires three measured DZT files
and three paired metadata records.

## Decision

Prepare global metadata separately where possible. Keep controlled field
evidence, parser/provenance promotion, field FWI, and field 3D/HPC blocked
until all coupled measured DZT files and metadata pass preflight together.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_dependency_audit.py

3 passed
```

Figure check:

```text
2644x882, dynamic range=255
```
