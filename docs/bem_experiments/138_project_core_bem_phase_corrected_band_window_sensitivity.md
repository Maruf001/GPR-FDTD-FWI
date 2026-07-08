# BEM Experiment 138: Phase-Corrected Band-Window Sensitivity

Date: 2026-06-27

## Purpose

Check whether a contiguous frequency band can pass after the best per-receiver
phase correction.

Run `137` showed that only one frequency bin passes the `0.1` gate after phase
correction. This run asks:

```text
Can any defensible multi-bin contiguous band pass the bridge gate?
```

This is a CPU-only audit of saved spectra. It does not rerun FDTD or BEM
solvers, compare against field data, launch GPU/HPC work, run 3D validation,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/138_project_core_bem_phase_corrected_band_window_sensitivity
```

Key artifacts:

```text
data/project_core_bem_phase_corrected_band_window_rows.csv
data/project_core_bem_phase_corrected_band_window_best_by_min_length.csv
data/project_core_bem_phase_corrected_band_window_sensitivity_summary.json
figures/project_core_bem_phase_corrected_band_window_sensitivity.png
docs/PROJECT_CORE_BEM_PHASE_CORRECTED_BAND_WINDOW_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
window count:                         153
passing windows:                      1
passing multi-bin windows:            0
best any-window bins:                 1
best any-window relative L2:          0.0953354196293874
best any-window frequency:            1.3744993103473124 GHz
best >=2-bin relative L2:             0.10447496219871069
best >=2-bin count:                   2
best >=3-bin relative L2:             0.11287493942418508
best >=3-bin count:                   3
only single bin passes:               true
multi-bin band ready:                 false
project-core bridge ready:            false
project-core FDTD comparison ready:   false
real 3D validation ready:             false
field FWI ready:                      false
gpu/hpc ready:                        false
```

Best windows by minimum length:

| Minimum bins | Best bins | Start GHz | Stop GHz | Relative L2 | Passes gate |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1 | 1.3744993103473124 | 1.3744993103473124 | 0.0953354196293874 | true |
| 2 | 2 | 1.3744993103473124 | 1.499453793106159 | 0.10447496219871069 | false |
| 3 | 3 | 1.3744993103473124 | 1.6244082758650056 | 0.11287493942418508 | false |
| 4 | 4 | 1.2495448275884657 | 1.6244082758650056 | 0.12919052631061526 | false |
| 5 | 5 | 1.124590344829619 | 1.6244082758650056 | 0.1343670846198178 | false |
| 6 | 6 | 0.8746813793119261 | 1.6244082758650056 | 0.1402640883805986 | false |

## Interpretation

Only one isolated frequency bin passes the `0.1` gate after phase correction.
The best two-bin window is `0.10447496219871069`, just outside the gate, and the
best three-bin window is `0.11287493942418508`.

This means the current bridge cannot be promoted by selecting a defensible
contiguous band. A single-bin pass is not sufficient evidence for BEM/FDTD
agreement.

## Decision

Do not promote a band-limited project-core BEM/FDTD bridge from this result.
Continue adapter work on band-edge handling and source/observable conditioning
before project-core comparison, 3D validation, GPU/HPC, or field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_phase_corrected_band_window_sensitivity.py
4 passed
```

Figure validation:

```text
project_core_bem_phase_corrected_band_window_sensitivity.png
2284x845, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_phase_corrected_band_window_sensitivity.py
sha256=0fbd8fa4e3df047a165c23e9b50a2545841f75e62264a852377fd5567f78a9f1

tests/test_project_core_bem_phase_corrected_band_window_sensitivity.py
sha256=9f74c7a70a87808dab3c72e174f1e221389a8121332abf6abe70719a9a80448b
```
