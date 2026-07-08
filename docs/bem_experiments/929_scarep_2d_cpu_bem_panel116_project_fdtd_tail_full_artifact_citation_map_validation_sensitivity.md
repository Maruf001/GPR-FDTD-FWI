# BEM Experiment 929: Panel-116 Project-FDTD Tail Full Artifact Citation Map Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `928` citation-map validator.

This run checks that the validator accepts only the exact full-artifact
citation-map state and rejects damaged citation policies or premature FDTD,
comparison, field-transfer, GPU, and 3D promotion.

## Output

```text
outputs/bem_experiments/929_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             22
expected pass scenarios:               1
expected fail scenarios:               21
observed pass scenarios:               1
observed fail scenarios:               21
unexpected outcomes:                   0
damaged scenarios:                     21
damaged scenarios rejected:            21
FDTD launch packet written:            true
FDTD execution authorized now:         false
return rows present:                   false
return values present:                 false
real BEM/FDTD comparison completed:    false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

Rejected damaged states include:

```text
map-not-ready state
citation row-count damage
duplicate-id set damage
output citation-count damage
doc citation-count damage
full-name-required damage
numeric-only-reference promotion
canonical-citation damage
policy-row failure
policy-row removal
launch-packet demotion
FDTD execution authorization
FDTD execution promotion
return-row promotion
return-value promotion
comparison promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The citation-map validator is fail-closed. It accepts the exact validated
citation map and rejects every tested damaged or prematurely promoted state.

## Decision

Use runs `927-929` as the guarded citation-map block for duplicated BEM
project-FDTD tail ids. Continue using full artifact names or paths for
duplicated ids and keep real BEM/FDTD comparison blocked until real returned
FDTD values are accepted.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validator.py
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_tail_full_artifact_citation_map_validation_sensitivity.py
11 passed
```

Figure check:

```text
3257x891, dynamic range=255
```
