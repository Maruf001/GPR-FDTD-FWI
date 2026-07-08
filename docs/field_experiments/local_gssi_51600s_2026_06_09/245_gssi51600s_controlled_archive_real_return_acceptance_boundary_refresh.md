# Field Experiment 245: Controlled Archive Real Return Acceptance Boundary Refresh

Date: 2026-06-28

## Purpose

Combine the guarded empty archive skeleton and guarded populated synthetic
archive smoke into the current real-return acceptance boundary. The goal is to
state what is mechanically ready for future real archive intake and what still
requires actual measured files and metadata.

This run does not contain real measured field files, accept a real archive,
promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/245_gssi51600s_controlled_archive_real_return_acceptance_boundary_refresh
```

Key artifacts:

```text
data/field_controlled_archive_real_return_acceptance_boundary_rows.csv
data/field_controlled_archive_real_return_acceptance_boundary_summary.json
figures/field_controlled_archive_real_return_acceptance_boundary_refresh.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_ACCEPTANCE_BOUNDARY_REFRESH.md
```

## Result

```text
boundary items:                    8
support ready items:               2
real acceptance blockers:          6
real-data blockers:                5
empty skeleton guarded:            true
synthetic smoke guarded:           true
acceptance boundary ready:         true
real files present:                false
real signoff values present:       false
real provenance values present:    false
checksum intake ready:             false
controlled evidence ready:         false
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The two ready support items are the guarded empty real-return archive skeleton
and the guarded populated synthetic archive positive control. The six blockers
are real measured DZT files, real operator signoff values, real provenance
values, real checksum intake, controlled-evidence acceptance, and all
field-FWI/3D/HPC/GPU escalation.

## Interpretation

Field real-return archive mechanics are guarded. The project now has a blank
archive skeleton and a positive synthetic smoke that proves correctly shaped
files can pass the intake checks.

The current archive still cannot become field evidence by relabeling synthetic
or blank values. Real measured files and real metadata remain required before
archive acceptance or field evidence promotion.

## Decision

Use run `245` as the current real-return archive acceptance boundary. Do not
promote field evidence, field FWI, field 3D/HPC, or GPU routes until real files
pass the guarded intake path.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_acceptance_boundary_refresh.py
3 passed
```

Figure validation:

```text
2861x847, dynamic range=255
```
