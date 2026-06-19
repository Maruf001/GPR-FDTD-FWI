# Field Experiment 145: Time-Zero Reference Requirement

Date: 2026-06-18

## Purpose

Quantify the external timing-reference requirement needed to move from
relative short-profile time-zero QC toward absolute time-zero calibration.

This is CPU-only field-readiness synthesis. It does not run FDTD, FWI, GPU
kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/145_gssi51600s_field_time_zero_reference_requirement
```

Key artifacts:

```text
data/field_time_zero_reference_requirement_summary.json
data/field_time_zero_reference_requirement_rows.csv
data/field_time_zero_reference_requirement_gates.csv
figures/field_time_zero_reference_requirement.png
```

## Result

```text
dielectric epsr:                                  2.25
velocity:                                        0.1998616387 m/ns
required external reference repeats:             3
reference uncertainty gate:                      0.02 ns
reference-gate depth equivalent:                 1.9986 mm
conservative relative half-width equivalent:     5.8898 mm
short-vs-early conflict equivalent:             12.7613 mm
current packet time-zero reference ready:        false
current packet blocking findings:               67
current archive absolute time-zero ready:        false
current archive field FWI ready:                 false
current archive heavy field ready:               false
field 3D/HPC ready:                              false
gpu priority:                                    none
```

## Interpretation

The next controlled field pass needs at least three repeatable air/direct-wave
or metal-plate timing references with uncertainty at or below `0.02 ns`.
At the current archive dielectric setting, that is about `2 mm` two-way
depth-equivalent timing error.

The current archive has zero such references. It supports relative
short-profile timing QC only; absolute time-zero, calibrated depth, field FWI,
heavy field GPU work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_time_zero_reference_requirement.py
3 passed
```
