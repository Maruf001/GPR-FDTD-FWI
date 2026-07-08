# BEM Experiment 140: Source-Amplitude-Conditioned Band-Window Sensitivity

Date: 2026-06-27

## Purpose

Test whether the phase-corrected project-core BEM/FDTD band-window no-go is
only caused by weak source-spectrum bins.

Runs `137`-`139` showed that after the best per-receiver phase correction,
only one isolated frequency bin passes the scattered-field gate and no
contiguous multi-bin band can be promoted. This run conditions the same
window search on source-spectrum amplitude thresholds.

This is a CPU-only post-processing audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/140_project_core_bem_source_amplitude_conditioned_band_window_sensitivity
```

Key artifacts:

```text
data/project_core_bem_source_amplitude_by_frequency.csv
data/project_core_bem_source_amplitude_conditioned_window_rows.csv
data/project_core_bem_source_amplitude_conditioned_threshold_summary.csv
data/project_core_bem_source_amplitude_conditioned_band_window_sensitivity_summary.json
figures/project_core_bem_source_amplitude_conditioned_band_window_sensitivity.png
docs/PROJECT_CORE_BEM_SOURCE_AMPLITUDE_CONDITIONED_BAND_WINDOW_SENSITIVITY.md
scripts/run_project_core_bem_source_amplitude_conditioned_band_window_sensitivity.py
scripts/test_project_core_bem_source_amplitude_conditioned_band_window_sensitivity.py
```

## Result

```text
frequency count:                         17
source thresholds:                       10
conditioned windows:                     860
thresholds with any passing window:      10
thresholds with passing multi-bin band:  0
best source-conditioned >=2-bin L2:      0.10447496219871069
best source-conditioned >=2-bin range:   1.3744993103473124 to 1.499453793106159 GHz
source conditioning changes no-go:       false
multi-bin band ready:                    false
project-core bridge ready:               false
field FWI ready:                         false
GPU/HPC ready:                           false
```

The same best two-bin window remains the best candidate at all tested source
amplitude thresholds:

| Source threshold | Kept bins | Windows | Passing windows | Passing multi-bin windows | Best >=2-bin L2 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.0 | 17 | 153 | 1 | 0 | 0.10447496219871069 |
| 0.1 | 17 | 153 | 1 | 0 | 0.10447496219871069 |
| 0.2 | 16 | 136 | 1 | 0 | 0.10447496219871069 |
| 0.3 | 15 | 120 | 1 | 0 | 0.10447496219871069 |
| 0.4 | 13 | 91 | 1 | 0 | 0.10447496219871069 |
| 0.5 | 12 | 78 | 1 | 0 | 0.10447496219871069 |
| 0.6 | 10 | 55 | 1 | 0 | 0.10447496219871069 |
| 0.7 | 8 | 36 | 1 | 0 | 0.10447496219871069 |
| 0.8 | 7 | 28 | 1 | 0 | 0.10447496219871069 |
| 0.9 | 4 | 10 | 1 | 0 | 0.10447496219871069 |

## Interpretation

Weak source-spectrum edges are not the main reason the multi-bin band fails.
Even after restricting candidate windows to bins with stronger source
amplitude, the best multi-bin relative-L2 value remains `0.10447496219871069`,
which is still above the `0.1` gate.

This narrows the next adapter work. The current blocker is more likely in the
scattered observable scaling, residual structure, or BEM/FDTD scattered-field
contract than in simple source-spectrum edge removal.

## Decision

Do not promote a source-conditioned project-core BEM/FDTD bridge. Continue
adapter work on observable scaling and residual structure before any
project-core comparison, 3D validation, GPU/HPC escalation, or field FWI claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_source_amplitude_conditioned_band_window_sensitivity.py
6 passed
```

Figure validation:

```text
project_core_bem_source_amplitude_conditioned_band_window_sensitivity.png
2914x845, dynamic range=255
```
