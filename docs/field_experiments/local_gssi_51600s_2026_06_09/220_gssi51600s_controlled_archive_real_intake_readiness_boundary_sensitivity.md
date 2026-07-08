# Field Experiment 220: Controlled Archive Real-Intake Readiness Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `219` real-intake boundary validator with damaged boundary
summaries.

This run does not ingest real field files, accept a real archive, run field FWI,
launch GPU/HPC work, or run field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/220_gssi51600s_controlled_archive_real_intake_readiness_boundary_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_intake_readiness_boundary_sensitivity_scenarios.csv
data/field_controlled_archive_real_intake_readiness_boundary_sensitivity_summary.json
figures/field_controlled_archive_real_intake_readiness_boundary_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_INTAKE_READINESS_BOUNDARY_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_intake_readiness_boundary_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_intake_readiness_boundary_sensitivity.py
```

## Result

```text
scenarios:                         19
expected pass scenarios:           1
expected failure scenarios:        18
observed pass scenarios:           1
observed failure scenarios:        18
unexpected outcomes:               0
sensitivity ready:                 true
real archive intake ready:         false
provenance acceptance ready:       false
checksum intake ready:             false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The exact real-intake boundary passes. Damaged cases fail for boundary-count
drift, collection readiness drift, real-file count or role drift, real-file row
promotion, provenance placeholder drift, future-date drift, evaluator readiness
drift, synthetic guardrail removal, checksum/evidence readiness, real archive
intake readiness, provenance acceptance readiness, field-FWI readiness, and
field-3D/HPC readiness.

## Interpretation

Runs `218`-`220` form a guarded field real-intake boundary package. The current
archive is collection-ready and evaluator-ready, but not evidence-ready.

## Decision

Use runs `218`-`220` as the guarded field real-intake boundary package.

Keep real archive acceptance, provenance acceptance, checksum intake,
controlled evidence, field FWI, GPU work, and field 3D/HPC blocked until real
measured files and metadata pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_intake_readiness_boundary_sensitivity.py
5 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_real_intake_readiness_boundary_sensitivity.py: pass
tests/test_gssi_field_controlled_archive_real_intake_readiness_boundary_sensitivity.py: pass
```

Figure check:

```text
3077x878, dynamic range=255
```
