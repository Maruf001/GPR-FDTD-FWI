# BEM Experiment 166: Fresh-Case Operator Branch Synthesis

Date: 2026-06-27

## Purpose

Synthesize the fresh-case BEM operator branches from runs `159` through `165`
into one case-by-case decision table.

This run compares the baseline adapter, receiver exclusion, frequency
exclusion, empirical cross-case scale tables, time-delay phase ramps,
target-weight discretization, and lateral aperture averaging.

This is a CPU-only synthesis from saved BEM-track artifacts. It does not rerun
FDTD or BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/166_project_core_bem_fresh_case_operator_branch_synthesis
```

Key artifacts:

```text
data/project_core_bem_fresh_case_operator_branch_rows.csv
data/project_core_bem_fresh_case_operator_branch_case_summary.csv
data/project_core_bem_fresh_case_operator_branch_synthesis_summary.json
figures/project_core_bem_fresh_case_operator_branch_synthesis.png
docs/PROJECT_CORE_BEM_FRESH_CASE_OPERATOR_BRANCH_SYNTHESIS.md
scripts/run_project_core_bem_fresh_case_operator_branch_synthesis.py
scripts/test_project_core_bem_fresh_case_operator_branch_synthesis.py
```

## Result

```text
fresh cases:                         3
branch labels:                       7
branch-case rows:                    21
physical operator branches:          3
diagnostic branches:                 2
strict-gate passes:                  0
worst best-any case:                 shifted_deeper_epsr4
worst best-any branch:               frequency_exclusion_best
worst best-any L2:                   0.518283007674826
worst best-physical branch:          time_delay_best
worst best-physical L2:              0.5924545602816863
max any improvement:                 0.21070480479002607
max physical improvement:            0.00727758001092027
local operator tweaks exhausted:     true
Green/interface priority:            true
project-core bridge ready:           false
3D validation ready:                 false
field FWI ready:                     false
GPU/HPC ready:                       false
```

| Case | Baseline L2 | Best any branch | Best any L2 | Best physical branch | Best physical L2 |
| --- | ---: | --- | ---: | --- | ---: |
| lower_contrast_radius_25mm | 0.18685792461171657 | frequency_exclusion_best | 0.10351457807041381 | target_weight_best | 0.18052318332440823 |
| shifted_deeper_epsr4 | 0.5997321402926066 | frequency_exclusion_best | 0.518283007674826 | time_delay_best | 0.5924545602816863 |
| larger_high_contrast_epsr6 | 0.5119171157297535 | frequency_exclusion_best | 0.30121231093972745 | aperture_average_best | 0.5102417712653161 |

## Interpretation

The local fresh-case operator tweaks do not close the project-core bridge. Even
the best diagnostic branch leaves the worst case above `0.5` relative L2, and
the best physical operator branch remains near `0.598` relative L2.

## Decision

Treat the current local operator tweaks as exhausted for bridge promotion.
Prioritize Green-function/interface physics, material modeling, or a more
faithful antenna model before 3D validation, GPU/HPC, or field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fresh_case_operator_branch_synthesis.py
4 passed
```

Figure validation:

```text
project_core_bem_fresh_case_operator_branch_synthesis.png
3113x842, dynamic range=255
```
