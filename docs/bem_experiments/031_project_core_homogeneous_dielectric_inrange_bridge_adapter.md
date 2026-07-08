# BEM Experiment 031: Homogeneous Dielectric In-Range Bridge Adapter

Date: 2026-06-25

## Purpose

Rerun the homogeneous dielectric project-core bridge with source positions and
Tx/Rx offset inside the empirical direct-wave Green surface from run `029`.

This run uses project-core FDTD and the analytic 2D TMz dielectric-cylinder
reference. It does not use field data, launch GPU work, run FWI, or touch the
historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/031_project_core_homogeneous_dielectric_inrange_bridge_adapter
```

## Result

```text
scan positions:                         7
source range:                           0.06 to 0.18 m
Tx/Rx offset:                           0.02 m
cylinder epsr:                          4.0
cylinder center:                        x=0.13 m, z=0.16 m
direct/background relative L2:          0.24273323569821098
total time symmetric L2:                0.42038566376997455
scattered time symmetric L2:            1.5431553591086644
residual best scale abs:                0.5718653985359872
homogeneous dielectric bridge ready:    false
```

## Interpretation

Moving the target bridge inside the empirical direct-wave source range does not
make the analytic/direct-calibrated target-scattering comparison pass. The
scattered-field mismatch remains large.

## Decision

Use this as the clean in-range target source run for empirical replay. Do not
use it as a BEM/project-core validation claim.

## Validation

```text
python run_project_core_homogeneous_dielectric_bridge_adapter.py \
  --outdir outputs/bem_experiments/031_project_core_homogeneous_dielectric_inrange_bridge_adapter \
  --scan-start-m 0.06 --scan-end-m 0.18 --scan-count 7 \
  --tx-rx-offset-m 0.02 --cylinder-x-m 0.13
```

