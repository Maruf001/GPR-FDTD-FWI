# Field Experiment 276: Controlled Collection-Day Phase Gate Dependency Validator

Date: 2026-06-28

## Purpose

Validate the saved run `275` phase-gate dependency audit from artifacts.

This run uses saved artifacts only. It does not ingest real field data, run
field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/276_gssi51600s_controlled_collection_real_return_collection_day_phase_gate_dependency_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator_checks.csv
data/field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_PHASE_GATE_DEPENDENCY_VALIDATOR.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
validation ready:               true
phases:                         8
required real files:            9
metadata values:                32
checksums:                      9
acceptance gates:               7
provenance acceptance ready:    false
controlled evidence ready:      false
field FWI ready:                false
field 3D/HPC ready:             false
GPU priority:                   none
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| phase order is exact | pass |
| dependency counts | pass |
| phases and gates blocked | pass |
| field downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The saved phase-gate dependency audit validates: eight phases, nine real files,
32 metadata values, nine checksums, and seven blocked acceptance gates define
the current field critical path.

## Decision

Use run `276` as the validator for the field phase-gate dependency map. Keep
field evidence, field FWI, 3D/HPC, and GPU work blocked until the real
collection packet is completed and validators pass.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_phase_gate_dependency_validator.py
3 passed
```

Figure validation:

```text
3401x895, dynamic range=255
```
