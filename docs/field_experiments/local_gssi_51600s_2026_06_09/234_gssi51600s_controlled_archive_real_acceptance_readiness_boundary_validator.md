# Field Experiment 234: Controlled Archive Real Acceptance Readiness Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `233` real archive-acceptance readiness boundary from a
consumer perspective.

Run `233` refreshed the current real-acceptance boundary after adding synthetic
completed-worksheet intake. This validator checks the item set, status counts,
synthetic-only boundary, required real blockers, and blocked downstream states.

It does not contain real measured files, accept an archive, run field FWI,
launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/234_gssi51600s_controlled_archive_real_acceptance_readiness_boundary_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_acceptance_readiness_boundary_validator_checks.csv
data/field_controlled_archive_real_acceptance_readiness_boundary_validator_summary.json
figures/field_controlled_archive_real_acceptance_readiness_boundary_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_ACCEPTANCE_READINESS_BOUNDARY_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_real_acceptance_readiness_boundary_validator.py
scripts/test_gssi_field_controlled_archive_real_acceptance_readiness_boundary_validator.py
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
validation ready:                  true
source boundary items:             9
source real-acceptance blockers:   5
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The validator checks:

| Check | Result |
| --- | --- |
| Boundary summary counts are consistent | pass |
| Boundary items and statuses match contract | pass |
| Synthetic completed worksheet is not real acceptance | pass |
| Required real-acceptance blockers are present | pass |
| Real archive and downstream states are blocked | pass |

## Interpretation

The refreshed real archive-acceptance boundary is internally consistent. The
expected nine items are present, synthetic worksheet support is not treated as
real acceptance, and five real blockers remain explicit.

## Decision

Use run `234` as the positive validator for the field real-acceptance boundary.
Sensitivity remains required before treating the boundary as fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_acceptance_readiness_boundary_validator.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_acceptance_readiness_boundary_validator.png
2573x839, dynamic range=255
```
