# Field Experiment 247: Controlled Archive Real Return Acceptance Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `246` real-return acceptance boundary validator. The goal
is to verify that the validator accepts the exact run `245` boundary and
rejects controlled damage to support rows, blocker rows, next-action fields,
summary counts, and false real/downstream readiness.

This run does not contain real measured field files, accept a real archive,
promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/247_gssi51600s_controlled_archive_real_return_acceptance_boundary_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_acceptance_boundary_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_acceptance_boundary_sensitivity_summary.json
figures/field_controlled_archive_real_return_acceptance_boundary_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_ACCEPTANCE_BOUNDARY_SENSITIVITY.md
```

## Result

```text
scenarios:                         22
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        21
observed failure scenarios:        21
unexpected outcomes:               0
sensitivity ready:                 true
acceptance boundary ready:         true
empty skeleton guarded:            true
synthetic smoke guarded:           true
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The exact run `245` boundary passes. All 21 damaged variants fail as expected
for missing boundary rows, support-count drift, blocker-count drift, missing
real-data requirements, unready support rows, false real-file readiness,
missing blocker flags, missing next actions, and false real archive/downstream
readiness.

## Interpretation

The real-return archive acceptance boundary is now guarded. The field track has
a ready blank skeleton and a ready synthetic positive-control intake smoke, but
real measured files and real metadata remain required.

This result does not promote field evidence, field FWI, field 3D/HPC, or GPU
work.

## Decision

Use runs `245`-`247` as the guarded real-return acceptance boundary. Real
measured files and metadata remain required before field evidence promotion.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_acceptance_boundary_sensitivity.py
6 passed
```

Figure validation:

```text
3725x890, dynamic range=255
```
