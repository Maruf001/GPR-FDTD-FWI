# BEM Experiment 162: Fresh-Case Cross-Case Operator Correction Audit

Date: 2026-06-27

## Purpose

Test whether receiver- and frequency-dependent correction factors learned from
two fresh project-core cases can transfer to a third held-out case.

Runs `159` through `161` showed that the project-core mismatch is structured:
it is concentrated by receiver and by frequency. This run asks whether that
structure can be learned as an empirical scale table without refitting on the
held-out case.

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/162_project_core_bem_fresh_case_cross_case_operator_correction_audit
```

Key artifacts:

```text
data/project_core_bem_fresh_case_cross_case_operator_correction_rows.csv
data/project_core_bem_fresh_case_cross_case_operator_correction_audit_summary.json
figures/project_core_bem_fresh_case_cross_case_operator_correction_audit.png
docs/PROJECT_CORE_BEM_FRESH_CASE_CROSS_CASE_OPERATOR_CORRECTION_AUDIT.md
scripts/run_project_core_bem_fresh_case_cross_case_operator_correction_audit.py
scripts/test_project_core_bem_fresh_case_cross_case_operator_correction_audit.py
```

## Result

```text
fresh cases:                         3
correction models:                   3
leave-one-case-out rows:             9
improvement rows:                    3
strict-gate passes:                  0
all best cases pass gate:            false
worst best case:                     shifted_deeper_epsr4
worst best model:                    receiver_scale
worst best L2:                       0.5984793935748264
cross-case correction ready:         false
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

| Held-out case | Best model | Baseline L2 | Best corrected L2 |
| --- | --- | ---: | ---: |
| lower_contrast_radius_25mm | frequency_scale | 0.18685792461171657 | 0.1868579246117166 |
| shifted_deeper_epsr4 | receiver_scale | 0.5997321402926066 | 0.5984793935748264 |
| larger_high_contrast_epsr6 | frequency_scale | 0.5119171157297535 | 0.5119171157297535 |

## Interpretation

The empirical correction table does not transfer. Receiver-frequency scaling
overfits badly, frequency-only scaling is effectively neutral, and
receiver-only scaling gives at most a tiny non-gate improvement.

This rules out a simple cross-case scale-table fix for the fresh-case
project-core mismatch.

## Decision

Keep the project-core bridge blocked. The next BEM improvement should target a
physics/geometry operator change rather than empirical receiver/frequency
rescaling. Do not promote this branch to 3D validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_cross_case_operator_correction_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_fresh_case_cross_case_operator_correction_audit.png
2392x842, dynamic range=255
```
