# Field Experiment 265: Controlled Collection Real-Return Empty Intake Layout Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `264` empty-layout validator with controlled damage cases.

This run checks whether the validator accepts only the exact run `263` empty
layout and rejects plausible artifact drift: required-file drift, placeholder
permission, false file presence, metadata prefill, checksum prefill, summary
drift, downstream promotion, figure-validation drift, and script-snapshot
drift.

It does not create DZT files, fabricate metadata, accept an archive, promote
controlled field evidence, run field FWI, launch field 3D/HPC, or use GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/265_gssi51600s_controlled_collection_real_return_empty_intake_layout_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_empty_intake_layout_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_empty_intake_layout_sensitivity_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_empty_intake_layout_sensitivity.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_EMPTY_INTAKE_LAYOUT_SENSITIVITY.md
scripts/run_gssi_field_controlled_collection_real_return_empty_intake_layout_sensitivity.py
scripts/test_gssi_field_controlled_collection_real_return_empty_intake_layout_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         41
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:        40
observed failure scenarios:        40
unexpected outcomes:                0
sensitivity ready:               true
exact run 263 accepted:          true
damaged variants rejected:       true
real files present:              false
provenance acceptance ready:     false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

## Interpretation

The empty-layout validator accepts the exact run `263` artifacts and rejects
every damaged variant. The rejected cases cover required-file drift,
placeholder permission, false file presence, metadata prefill, checksum
prefill, summary drift, downstream promotion, figure-validation drift, and
script-snapshot drift.

## Decision

Use runs `263-265` as the guarded empty real-return intake layout. Real files,
measured metadata, checksums, structural validation, provenance validation,
archive acceptance, controlled evidence, field FWI, field 3D/HPC, and GPU
escalation remain blocked.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_empty_intake_layout_sensitivity.py
3 passed
```

Figure validation:

```text
4031x883, dynamic range=255
```
