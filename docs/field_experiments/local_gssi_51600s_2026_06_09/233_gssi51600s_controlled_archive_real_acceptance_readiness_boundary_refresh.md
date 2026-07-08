# Field Experiment 233: Controlled Archive Real Acceptance Readiness Boundary Refresh

Date: 2026-06-28

## Purpose

Refresh the real archive-acceptance boundary after adding the synthetic
completed-worksheet intake package.

Runs `230-232` proved that completed-worksheet intake mechanics work on a
clearly synthetic fixture. This run joins that result with the earlier real
intake boundary and signoff guard to show what remains missing before a real
archive can be accepted.

It does not contain real measured files, accept an archive, run field FWI,
launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/233_gssi51600s_controlled_archive_real_acceptance_readiness_boundary_refresh
```

Key artifacts:

```text
data/field_controlled_archive_real_acceptance_readiness_boundary_rows.csv
data/field_controlled_archive_real_acceptance_readiness_boundary_summary.json
figures/field_controlled_archive_real_acceptance_readiness_boundary_refresh.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_ACCEPTANCE_READINESS_BOUNDARY_REFRESH.md
scripts/run_gssi_field_controlled_archive_real_acceptance_readiness_boundary_refresh.py
scripts/test_gssi_field_controlled_archive_real_acceptance_readiness_boundary_refresh.py
```

## Result

```text
boundary items:                    9
ready items:                       2
ready synthetic-only items:        1
real acceptance blockers:          5
real files required:               9
real files present:                false
real signoff values present:       false
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The five real-acceptance blockers are:

| Blocker | Needed next |
| --- | --- |
| real measured files | collect and stage the nine real GSSI DZT files |
| real operator signoff values | record real initials, local collection times, staged SHA-256 values, and optional notes |
| provenance acceptance | replace placeholders and future-date entries with measured session/provenance values |
| checksum intake | run checksum intake on staged real files |
| controlled evidence acceptance | rerun structural, provenance, command-plan, checksum, and evidence gates on real data |

## Interpretation

The field archive has guarded collection and synthetic worksheet mechanics, but
real archive acceptance remains blocked by missing measured files, missing real
signoff values, missing real provenance, checksum intake, and controlled-
evidence acceptance.

## Decision

Use run `233` as the current real archive-acceptance boundary. Collect the nine
real DZT files and real operator/provenance values, then rerun structural,
provenance, command-plan, checksum, and evidence gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_acceptance_readiness_boundary_refresh.py
4 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_acceptance_readiness_boundary_refresh.png
2680x858, dynamic range=255
```
