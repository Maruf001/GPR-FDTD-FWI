# BEM Experiment 927: Panel-116 Project-FDTD Tail Full Artifact Citation Map

Date: 2026-07-01

## Purpose

Write a full-artifact citation map for the panel-116 project-FDTD tail where
several numeric run ids are duplicated across distinct artifacts.

The map makes citations unambiguous by requiring full artifact names or paths
for duplicated ids. This is a bookkeeping and claim-boundary run. It does not
authorize FDTD execution, complete a real BEM/FDTD comparison, transfer the
result to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/927_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map
```

## Result

```text
citation rows:                         16
duplicated numeric ids:                4
duplicated ids:                        915;920;921;924
output citation rows:                  8
doc citation rows:                     8
full-name-required rows:               16
numeric-only references allowed:       0
policy rows:                           4
failed policy rows:                    0
FDTD executed now:                     false
return rows present:                   false
return values present:                 false
real BEM/FDTD comparison completed:    false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

## Interpretation

The duplicated tail ids are not a physics or solver result. They are a citation
risk. Numeric-only references such as `915` or `924` are ambiguous in this
tail block because each can refer to more than one artifact.

## Decision

Use full artifact names or paths when citing duplicated ids `915`, `920`,
`921`, and `924`. Keep FDTD execution, return-value, comparison, field-transfer,
GPU, and 3D claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map.py
4 passed
```

Figure check:

```text
nonblank citation-map figure
```
