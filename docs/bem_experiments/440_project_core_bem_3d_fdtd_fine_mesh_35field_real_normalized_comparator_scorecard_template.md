# BEM Experiment 440: 35-Field Real Normalized-Comparator Scorecard Template

Date: 2026-06-29

## Purpose

Convert the guarded synthetic normalized-comparator score and threshold
contracts into a non-evidence scorecard template for a future real returned
BEM/FDTD comparison packet.

## Output

```text
outputs/bem_experiments/440_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_scorecard_template_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_acceptance_rule_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template.png
```

## Result

```text
source ready:                       true
scorecard template ready:           true
template rows:                      279
receivers:                          31
frequencies:                        9
relative tolerance:                 1e-12
reference coefficient:              0.01907878402833891
required real input cells:          1116
generated score cells:              1116
acceptance rules:                   5
template rows currently evidence:   0
real return values present:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The template preserves the 31-by-9 receiver/frequency grid and leaves all real
returned values and hashes blank. It is a handoff artifact for future returned
files, not comparison evidence.

## Decision

Use this as the non-evidence scorecard template for a future real returned
BEM/FDTD comparison packet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template.py
3 passed
```

Figure check:

```text
3221x893, dynamic range=255
```
