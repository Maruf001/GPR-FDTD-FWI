# BEM Experiment 928: Panel-116 Project-FDTD Tail Full Artifact Citation Map Validator

Date: 2026-07-01

## Purpose

Validate the run `927` full-artifact citation map from saved artifacts.

This run checks that the map preserves the duplicated-id boundary, requires
full artifact citations, blocks numeric-only references, and keeps FDTD,
comparison, field-transfer, GPU, and 3D states unpromoted.

## Output

```text
outputs/bem_experiments/928_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validator
```

## Result

```text
validation checks:                     6
passed checks:                         6
failed checks:                         0
citation rows:                         16
duplicated numeric ids:                4
duplicated ids:                        915;920;921;924
output citation rows:                  8
doc citation rows:                     8
full-name-required rows:               16
numeric-only references allowed:       0
policy rows:                           4
FDTD executed now:                     false
return rows present:                   false
return values present:                 false
real BEM/FDTD comparison completed:    false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

## Interpretation

The citation map validates as a stable guard around duplicated numeric ids.
The validator confirms that full names or paths are required for the affected
artifacts and that no solver or downstream claim was promoted.

## Decision

Use the validated map when citing duplicated ids `915`, `920`, `921`, and
`924`.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validator.py
4 passed
```

Figure check:

```text
nonblank validation figure
```
