# BEM Experiment 139: Phase-Corrected Band-Window Validator

Date: 2026-06-27

## Purpose

Validate the run `138` band-window no-go result from a consumer perspective.

This run checks that the band-window table is internally consistent: exactly
one isolated single-bin window passes, no multi-bin window passes, and the
project-core BEM/FDTD bridge remains blocked.

This is a CPU-only validation. It does not rerun FDTD or BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
train neural networks.

## Output

```text
outputs/bem_experiments/139_project_core_bem_phase_corrected_band_window_validator
```

Key artifacts:

```text
data/project_core_bem_phase_corrected_band_window_validation_checks.csv
data/project_core_bem_phase_corrected_band_window_validator_summary.json
figures/project_core_bem_phase_corrected_band_window_validator.png
docs/PROJECT_CORE_BEM_PHASE_CORRECTED_BAND_WINDOW_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
validation passes:                  7
blocking failures:                  0
source windows:                     153
source passing windows:             1
source passing multi-bin windows:   0
band-window no-go valid:            true
multi-bin band ready:               false
project-core bridge ready:          false
project-core FDTD comparison ready: false
real 3D validation ready:           false
field FWI ready:                    false
gpu/hpc ready:                      false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| window_rows_nonempty | pass | 153 rows |
| row_count_matches_summary | pass | 153 observed / 153 summary |
| single_passing_window_matches_summary | pass | 1 passing windows |
| no_multi_bin_passing_window | pass | 0 multi-bin passing windows |
| best_any_window_is_single_bin | pass | 1 best-bin count |
| best_multi_bin_window_still_fails | pass | best multi-bin L2 0.10447496219871069 |
| bridge_not_promoted | pass | bridge, 3D, GPU/HPC, and field FWI blocked |

## Interpretation

The run `138` no-go result is internally consistent. Exactly one isolated
single-bin window passes, no multi-bin window passes, and the bridge remains
blocked.

## Decision

Use run `139` as the consumer-side validator for the band-window no-go. Do not
promote band-limited project-core BEM/FDTD comparison, 3D validation, GPU/HPC,
or field FWI from this bridge.

## Validation

Focused test:

```text
tests/test_project_core_bem_phase_corrected_band_window_validator.py
3 passed
```

Figure validation:

```text
project_core_bem_phase_corrected_band_window_validator.png
2249x839, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_phase_corrected_band_window_validator.py
sha256=4d55cf0bb437170e54fa6a9c96bc18da0610073617aca8450d22b7fc0794c7bc

tests/test_project_core_bem_phase_corrected_band_window_validator.py
sha256=bca32b7ce30098295ad28b3fd52ebb2f6226a97e201c6a07823ac09571971ccc
```
