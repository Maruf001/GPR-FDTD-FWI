# Experiment 804: Archive Location Ambiguity Family Breakdown

Date: 2026-06-17

## Purpose

CPU-only breakdown of the exact-strong ambiguous rows found by experiment 803.
This run groups the archive strict-clean exceptions by experiment family so the
paper-facing policy can distinguish legacy/reporting caveats from new GPU work.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1282_archive_location_ambiguity_family_breakdown
```

Artifacts:

```text
data/archive_location_ambiguity_rows.csv
data/archive_location_ambiguity_family_breakdown.csv
data/archive_location_ambiguity_family_breakdown_summary.json
data/figure_validation.csv
figures/archive_location_ambiguity_family_breakdown.png
run_manifest.json
```

## Result

Policy label:

```text
archive_location_ambiguity_target2_family_breakdown_cpu_no_gpu
```

Summary:

```text
input rows:                         687
exact-strong ambiguous rows:        21
family count:                       4
target indices:                     2
x-ambiguous rows:                   19
z-ambiguous rows:                   2
radius-ambiguous rows:              2
nominal rows:                       14
source-mismatch rows:               7
max x ambiguity width:              1.000 mm
max z ambiguity width:              1.000 mm
max radius ambiguity width:         0.750 mm
gpu priority:                       none_now
```

Family table:

```text
target2_variable_radius_legacy: 12 rows, x only
target2_close14:                 4 rows, x only
target2_close50:                 3 rows, x only
target2_variable_depth_radius:   2 rows, z + radius
```

## Interpretation

The strict-clean exceptions are all target2 archive-family caveats. They should
be excluded from strict location-clean threshold claims, but they do not justify
a broad GPU sweep.

The most paper-relevant use is reporting discipline: archive tables should
distinguish exact/strong rows from strict location-clean rows. The family-level
breakdown also points to possible future CPU objective-design work for target2
branch ambiguity, especially legacy variable-radius and close-spacing cases.

## Validation

Focused tests:

```text
tests/test_archive_location_ambiguity_family_breakdown.py: 3 passed
```

Figure validation:

```text
archive_location_ambiguity_family_breakdown.png: 2297x835,
nonwhite=0.2739, dynamic range=255
```
