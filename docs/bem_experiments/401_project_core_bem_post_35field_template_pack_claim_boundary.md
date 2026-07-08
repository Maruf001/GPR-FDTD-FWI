# BEM Experiment 401: Post-Template-Pack Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded 35-field BEM/FDTD return-template pack from runs `398-400`
into the current BEM claim boundary.

This run does not stage returned FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, transfer to field evidence, launch GPU work, or make a
3D validation claim.

## Output

```text
outputs/bem_experiments/401_project_core_bem_post_35field_template_pack_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_template_pack_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_template_pack_claim_boundary_summary.json
figures/project_core_bem_post_35field_template_pack_claim_boundary.png
```

## Result

```text
claims:                              19
guarded claims:                      16
blocked claims:                      3
new guarded template-pack claim:     true
template packet files:               3
frequency template files:            2
metadata template files:             1
rows per frequency file:             279
blank frequency component cells:     3348
metadata fields:                     35
blocking metadata fields:            34
blank metadata values:               12
receiver-aperture addendum fields:   5
real comparison ready:               false
3D validation claim ready:           false
field transfer ready:                false
GPU/HPC ready:                       false
```

## Interpretation

The template-pack result is now part of the guarded BEM evidence boundary. The
new claim is intentionally narrow: the project has a validated non-evidence
return-template pack, not a returned-data comparison.

The boundary still blocks real BEM/FDTD comparison, field transfer, broad BEM
replacement, GPU/HPC escalation, and 3D validation until real target,
background, and metadata files replace the templates and pass the preflight.

## Decision

Use run `401` as the post-template-pack BEM claim boundary. Validate and
sensitivity-harden it before treating the boundary as closed.

## Validation

Focused test:

```text
tests/test_project_core_bem_post_35field_template_pack_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x916, dynamic range=255
```
