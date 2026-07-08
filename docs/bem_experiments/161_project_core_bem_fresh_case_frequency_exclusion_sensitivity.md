# BEM Experiment 161: Fresh-Case Frequency Exclusion Sensitivity

Date: 2026-06-27

## Purpose

Test whether dropping residual-heavy frequency bins can close the fresh-case
project-core comparison gap.

Run `159` showed that the top five frequency bins carry more than 63 percent
of residual energy in each fresh case. This run checks whether excluding the
largest residual-frequency bins is enough to pass the strict comparison gate.

This is a CPU-only audit from saved BEM-track arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/161_project_core_bem_fresh_case_frequency_exclusion_sensitivity
```

Key artifacts:

```text
data/project_core_bem_fresh_case_frequency_exclusion_rows.csv
data/project_core_bem_fresh_case_frequency_exclusion_sensitivity_summary.json
figures/project_core_bem_fresh_case_frequency_exclusion_sensitivity.png
docs/PROJECT_CORE_BEM_FRESH_CASE_FREQUENCY_EXCLUSION_SENSITIVITY.md
scripts/run_project_core_bem_fresh_case_frequency_exclusion_sensitivity.py
scripts/test_project_core_bem_fresh_case_frequency_exclusion_sensitivity.py
```

## Result

```text
fresh cases:                             3
drop-top count settings:                 5
frequency subset rows:                   15
strict-gate passes:                      0
all best subsets pass gate:              false
worst best case:                         shifted_deeper_epsr4
worst best drop-top count:               8
worst best relative L2:                  0.518283007674826
frequency exclusion promotes bridge:     false
frequency-local operator model needed:   true
project-core bridge ready:               false
3D validation ready:                     false
field FWI ready:                         false
GPU/HPC ready:                           false
```

Best diagnostic exclusions:

| Case | All-frequency L2 | Best drop count | Best L2 |
| --- | ---: | ---: | ---: |
| lower_contrast_radius_25mm | 0.18685792461171663 | 8 | 0.10351457807041381 |
| shifted_deeper_epsr4 | 0.5997321402926066 | 8 | 0.518283007674826 |
| larger_high_contrast_epsr6 | 0.5119171157297535 | 8 | 0.30121231093972745 |

## Interpretation

Dropping residual-heavy frequency bins reduces error but does not close the
gate on the high-error fresh cases. Frequency exclusion would hide part of the
mismatch without promoting the bridge.

## Decision

Keep the project-core bridge blocked. Use the frequency localization as a
target for frequency-local operator modeling, not as permission to trim bands
or promote 3D validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_frequency_exclusion_sensitivity.py
3 passed
```

Figure validation:

```text
project_core_bem_fresh_case_frequency_exclusion_sensitivity.png
2392x845, dynamic range=255
```
