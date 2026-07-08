# Field Experiment 219: Controlled Archive Real-Intake Readiness Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `218` real-intake boundary from a consumer perspective.

This run does not ingest real field files, accept a real archive, run field FWI,
launch GPU/HPC work, or run field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/219_gssi51600s_controlled_archive_real_intake_readiness_boundary_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_intake_readiness_boundary_validation_checks.csv
data/field_controlled_archive_real_intake_readiness_boundary_validator_summary.json
figures/field_controlled_archive_real_intake_readiness_boundary_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_INTAKE_READINESS_BOUNDARY_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_real_intake_readiness_boundary_validator.py
scripts/test_gssi_field_controlled_archive_real_intake_readiness_boundary_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
validation ready:                   true
real files required:                9
real archive intake ready:          false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The validator confirms the nine-item boundary table, collection checklist
readiness, nine real-file requirement with three profile, three time-zero, and
three amplitude-reference files, real provenance blockers, evaluator readiness,
synthetic positive-control limits, checksum/evidence blockers, and blocked
downstream field states.

## Interpretation

The run `218` real-intake boundary is internally consistent. It is now
positively validated, but not yet stress-tested by negative controls.

## Decision

Use run `219` as the positive validator for the real-intake boundary.

Run sensitivity testing before treating this boundary as fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_intake_readiness_boundary_validator.py
5 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_real_intake_readiness_boundary_validator.py: pass
tests/test_gssi_field_controlled_archive_real_intake_readiness_boundary_validator.py: pass
```

Figure check:

```text
2465x841, dynamic range=255
```
