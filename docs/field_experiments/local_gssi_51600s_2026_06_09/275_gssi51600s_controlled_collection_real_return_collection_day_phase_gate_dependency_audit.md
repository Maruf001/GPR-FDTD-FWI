# Field Experiment 275: Controlled Collection-Day Phase Gate Dependency Audit

Date: 2026-06-28

## Purpose

Map the controlled collection-day execution phases to the concrete acceptance
gates they unblock.

This run uses saved artifacts only. It does not ingest real field data, run
field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/275_gssi51600s_controlled_collection_real_return_collection_day_phase_gate_dependency_audit
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_phase_gate_dependency_rows.csv
data/field_controlled_collection_real_return_collection_day_phase_gate_dependency_audit_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_phase_gate_dependency_audit.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_PHASE_GATE_DEPENDENCY_AUDIT.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_audit.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
phases:                          8
required real files:             9
global metadata values:          11
file metadata values:            21
checksums:                       9
acceptance gates:                7
blocked acceptance gates:        7
all phases nonexecuted:          true
all phases block downstream:     true
all linked gates blocked now:    true
dependency audit ready:          true
provenance acceptance ready:     false
controlled evidence ready:       false
field FWI ready:                 false
field 3D/HPC ready:              false
GPU priority:                    none
```

Phase dependencies:

| Phase | Real files | Metadata values | Checksums | Linked gates |
| --- | ---: | ---: | ---: | --- |
| session metadata capture | 0 | 11 | 0 | stage global metadata |
| controlled profile repeats | 3 | 0 | 0 | stage required DZT files |
| time-zero references | 3 | 0 | 0 | stage required DZT files |
| amplitude references | 3 | 0 | 0 | stage required DZT files |
| return inbox copy | 9 | 0 | 0 | stage required DZT files |
| checksum recording | 0 | 0 | 9 | record file metadata and checksums |
| file metadata fill | 0 | 21 | 0 | record file metadata and checksums |
| validator rerun | 0 | 0 | 0 | structural validation, provenance gate, evidence promotion, field-FWI/3D/GPU consideration |

## Interpretation

The collection-day sequence is a strict dependency chain. Metadata capture,
real file collection and copying, checksum recording, file metadata fill, and
validator reruns must all complete before field evidence or downstream FWI/GPU
work can be considered.

## Decision

Use run `275` as the field phase-gate dependency map. Keep provenance
acceptance, controlled field evidence, field FWI, 3D/HPC, and GPU work blocked
until the real collection packet is completed and validators pass.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_audit.py
3 passed
```

Figure validation:

```text
3293x912, dynamic range=255
```
