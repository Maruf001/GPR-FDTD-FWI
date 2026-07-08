# BEM Experiment 141: Phase-Corrected Observable-Scaling Audit

Date: 2026-06-27

## Purpose

Test whether the remaining phase-corrected BEM/FDTD mismatch can be explained
by simple observable scaling.

Runs `137`-`140` narrowed the bridge blocker: phase correction helps, weak
source-spectrum bins do not explain the no-go, and no source-conditioned
multi-bin frequency band passes the gate. This run checks global,
per-receiver, per-frequency, and separable receiver/frequency complex scaling
after the best phase correction.

This is a CPU-only post-processing audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/141_project_core_bem_phase_corrected_observable_scaling_audit
```

Key artifacts:

```text
data/project_core_bem_phase_corrected_observable_scaling_candidates.csv
data/project_core_bem_phase_corrected_observable_scaling_frequency_residuals.csv
data/project_core_bem_phase_corrected_observable_scaling_audit_summary.json
figures/project_core_bem_phase_corrected_observable_scaling_audit.png
docs/PROJECT_CORE_BEM_PHASE_CORRECTED_OBSERVABLE_SCALING_AUDIT.md
scripts/run_project_core_bem_phase_corrected_observable_scaling_audit.py
scripts/test_project_core_bem_phase_corrected_observable_scaling_audit.py
```

## Result

```text
candidate count:                    5
baseline spectral relative L2:      0.18500684021427602
best candidate:                     separable_receiver_frequency_complex_scale
best candidate spectral L2:         0.117062890994582
best candidate scale parameters:    24
improvement factor:                 1.5804055293905108
best candidate passes gate:         false
simple observable scaling ready:    false
project-core bridge ready:          false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Candidate table:

| Candidate | Scale parameters | Spectral L2 | Frequency bins passing | Receiver rows passing | Passes gate |
| --- | ---: | ---: | ---: | ---: | --- |
| phase_corrected_baseline | 0 | 0.18500684021427602 | 1 | 0 | false |
| global_complex_scale | 1 | 0.18500684021427607 | 1 | 0 | false |
| per_receiver_complex_scale | 7 | 0.18500684021427607 | 1 | 0 | false |
| per_frequency_complex_scale | 17 | 0.1171692949091954 | 7 | 3 | false |
| separable_receiver_frequency_complex_scale | 24 | 0.117062890994582 | 8 | 3 | false |

## Interpretation

The remaining mismatch is not a global amplitude/phase scaling error and is
not a receiver-only scaling error. Per-frequency scaling helps substantially,
reducing the phase-corrected spectral relative L2 from `0.18500684021427602`
to `0.1171692949091954`. A separable receiver/frequency scaling gives a very
similar best value, `0.117062890994582`.

Those improvements still do not pass the `0.1` gate. This means the project
bridge is not ready, but the residual has a strong frequency-local component.

## Decision

Keep the project-core BEM/FDTD bridge blocked. The next adapter work should
examine frequency-local residual patterns and the scattered-field observable
contract before any 3D validation, GPU/HPC escalation, or field FWI claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_phase_corrected_observable_scaling_audit.py
6 passed
```

Figure validation:

```text
project_core_bem_phase_corrected_observable_scaling_audit.png
2950x840, dynamic range=255
```
