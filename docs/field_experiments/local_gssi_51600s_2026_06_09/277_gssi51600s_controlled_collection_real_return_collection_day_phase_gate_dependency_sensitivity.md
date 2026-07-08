# Field Experiment 277: Controlled Collection-Day Phase Gate Dependency Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `276` phase-gate dependency validator. Runs `275-276`
mapped the collection-day phases to the acceptance gates that must remain
blocked until real files, measured metadata, and checksums are staged. This run
checks whether that validator rejects damaged variants.

This is an artifact-only field-side test. It does not ingest real field data,
run field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/277_gssi51600s_controlled_collection_real_return_collection_day_phase_gate_dependency_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_phase_gate_dependency_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_collection_day_phase_gate_dependency_sensitivity_summary.json
figures/field_controlled_collection_real_return_collection_day_phase_gate_dependency_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_PHASE_GATE_DEPENDENCY_SENSITIVITY.md
```

## Result

```text
scenarios:                 19
expected pass:             1
observed pass:             1
expected failures:         18
observed failures:         18
unexpected outcomes:       0
sensitivity ready:         true
real files present:        false
metadata values present:   false
checksums present:         false
provenance ready:          false
controlled evidence ready: false
field FWI ready:           false
field 3D/HPC ready:        false
GPU priority:              none
```

The exact run `275` phase-gate dependency audit passes. All damaged variants
fail as expected. The damaged cases cover:

- source policy/count drift,
- phase-order drift,
- required file, metadata, checksum, and gate-count drift,
- phase execution state drift,
- downstream block-flag drift,
- false provenance/evidence/FWI/GPU promotion,
- figure-validation drift,
- missing script snapshots.

## Interpretation

The run `276` validator is sensitive to the changes that would matter for field
readiness. It accepts the exact dependency map and rejects variants that would
pretend the field side is ready without real measured files, measured metadata,
checksums, and rerun validators.

## Decision

Use runs `275-277` as the guarded field phase-gate dependency block. Keep
provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU work blocked until nine real DZT files,
32 measured metadata values, and nine checksums are staged and accepted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator.py
tests/test_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_sensitivity.py

6 passed
```

Figure validation:

```text
3473x897, dynamic range=255
```
