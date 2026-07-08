# Field Experiment 278: Collection-Day Critical Path Audit

Date: 2026-06-28

## Purpose

Convert the guarded field fill packet and phase-gate map into a three-stage
critical path.

This run separates the remaining work into field-day capture, post-return
archive completion, and validation/acceptance. It uses saved field planning
artifacts only. It does not create measured DZT files, run field preprocessing,
run FDTD, run field FWI, launch GPU/HPC work, or claim field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/278_gssi51600s_controlled_collection_real_return_collection_day_critical_path_audit
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_critical_path_audit_requirement_rows.csv
data/field_controlled_collection_real_return_collection_day_critical_path_audit_stage_rows.csv
data/field_controlled_collection_real_return_collection_day_critical_path_audit_summary.json
figures/field_controlled_collection_real_return_collection_day_critical_path_audit.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_CRITICAL_PATH_AUDIT.md
```

## Result

```text
critical-path stages:              3
requirement rows:                  57
measured requirements:             50
measured requirements complete:    0
required real DZT files:           9
metadata values:                   32
checksums:                         9
acceptance gates:                  7
acceptance gates ready:            0
field-day measured requirements:   20
post-return measured requirements: 30
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The three stages are:

| Stage | Measured requirements | Main work |
| --- | ---: | --- |
| field-day capture/acquisition | 20 | capture 9 real DZT files and 11 global metadata values |
| post-return archive completion | 30 | fill 21 file metadata values and 9 checksums |
| validation and acceptance | 0 measured values, 7 gates | rerun validators and decide whether evidence can be promoted |

## Interpretation

The field blocker is now expressed as an operational critical path. The current
archive has zero of the 50 measured requirements complete. Completing the
field-day stage alone is not sufficient: post-return file metadata, checksums,
and validation gates still control whether the packet can become field
evidence.

## Decision

Use run `278` as the operational critical-path view for the field packet. Keep
provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU work blocked until the measured requirements
and gates are completed.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_critical_path_audit.py
3 passed
```

Figure validation:

```text
3365x914, dynamic range=255
```
