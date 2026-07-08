# Field Experiment 218: Controlled Archive Real-Intake Readiness Boundary

Date: 2026-06-28

## Purpose

Combine the run `163` provenance-closure checklist with the guarded command-plan
evaluator contract from runs `215`-`217`.

This run does not ingest real field files, accept a real archive, run field FWI,
launch GPU/HPC work, or run field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/218_gssi51600s_controlled_archive_real_intake_readiness_boundary
```

Key artifacts:

```text
data/field_controlled_archive_real_intake_readiness_boundary_rows.csv
data/field_controlled_archive_real_intake_readiness_boundary_summary.json
figures/field_controlled_archive_real_intake_readiness_boundary.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_INTAKE_READINESS_BOUNDARY.md
scripts/run_gssi_field_controlled_archive_real_intake_readiness_boundary.py
scripts/test_gssi_field_controlled_archive_real_intake_readiness_boundary.py
```

## Result

```text
boundary items:                    9
ready items:                       2
real acceptance blockers:          7
closure actions:                   6
real files required:               9
controlled profile files:          3
time-zero reference files:         3
amplitude reference files:         3
placeholder findings:              32
future-date findings:              1
evaluator contract ready:          true
evaluator sensitivity ready:       true
collection-day execution ready:    true
real archive intake ready:         false
provenance acceptance ready:       false
checksum intake ready:             false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The field side now has two ready pieces: a concrete collection-day checklist and
a guarded command-plan evaluator. Real acceptance remains blocked by seven
items, including the nine missing real DZT files, real provenance values,
future-date cleanup, checksum intake on real files, controlled evidence
acceptance, and downstream field-FWI/3D/GPU escalation.

## Interpretation

The archive is ready to be collected against and ready to be evaluated after
collection. It is not accepted field evidence yet.

The synthetic positive-control pass proves evaluator behavior only. It does not
replace the nine measured files or measured metadata.

## Decision

Use run `218` as the real-intake boundary.

Collect the nine real files and measured metadata, then rerun provenance and
command-plan gates. Keep real archive acceptance, checksum intake, controlled
evidence, field FWI, GPU work, and field 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_intake_readiness_boundary.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_real_intake_readiness_boundary.py: pass
tests/test_gssi_field_controlled_archive_real_intake_readiness_boundary.py: pass
```

Figure check:

```text
2861x877, dynamic range=255
```
