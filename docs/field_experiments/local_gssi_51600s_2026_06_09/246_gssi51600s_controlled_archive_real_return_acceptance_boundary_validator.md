# Field Experiment 246: Controlled Archive Real Return Acceptance Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `245` real-return acceptance boundary from saved artifacts.
The goal is to confirm that a downstream consumer can read the boundary rows
and summary while preserving the split between ready synthetic support and
blocked real archive acceptance.

This run does not contain real measured field files, accept a real archive,
promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/246_gssi51600s_controlled_archive_real_return_acceptance_boundary_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_return_acceptance_boundary_validator_checks.csv
data/field_controlled_archive_real_return_acceptance_boundary_validator_summary.json
figures/field_controlled_archive_real_return_acceptance_boundary_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_ACCEPTANCE_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:                 5
validation checks passed:          5
blocking failures:                 0
boundary validation ready:         true
acceptance boundary ready:         true
empty skeleton guarded:            true
synthetic smoke guarded:           true
real files present:                false
real signoff values present:       false
real provenance values present:    false
checksum intake ready:             false
controlled evidence ready:         false
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The five validation checks confirm:

| Check | Result |
| --- | --- |
| Boundary counts are consistent | pass |
| Synthetic support items are ready only | pass |
| Real acceptance blockers are present | pass |
| Next actions are recorded | pass |
| Real archive and downstream states are blocked | pass |

## Interpretation

The saved real-return acceptance boundary is internally consistent. The empty
archive skeleton and synthetic populated archive smoke are ready support items,
but they do not count as real archive acceptance.

Real measured files and real metadata remain required before field evidence,
field FWI, field 3D/HPC, or GPU routes can be promoted.

## Decision

Use runs `245`-`246` as the consumer-validated real-return acceptance boundary.
Sensitivity remains required before treating it as fully guarded.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_acceptance_boundary_validator.py
5 passed
```

Figure validation:

```text
2717x822, dynamic range=255
```
