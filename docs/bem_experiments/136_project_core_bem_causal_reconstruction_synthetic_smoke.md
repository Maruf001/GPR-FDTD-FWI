# BEM Experiment 136: Causal Reconstruction Synthetic Smoke

Date: 2026-06-27

## Purpose

Check whether the causal reconstruction contract from run `135` can distinguish
a correct synthetic per-receiver delay/scale reconstruction from wrong phase,
global-delay, missing-delay, and receiver-order alternatives.

This is a synthetic guard for the next project-core adapter rerun. It does not
run FDTD or BEM solvers, compare against field data, launch GPU/HPC work, run
3D validation, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/136_project_core_bem_causal_reconstruction_synthetic_smoke
```

Key artifacts:

```text
data/project_core_bem_causal_reconstruction_synthetic_smoke_metrics.csv
data/project_core_bem_causal_reconstruction_synthetic_smoke_summary.json
figures/project_core_bem_causal_reconstruction_synthetic_smoke.png
docs/PROJECT_CORE_BEM_CAUSAL_RECONSTRUCTION_SYNTHETIC_SMOKE.md
scripts/script_snapshot_manifest.json
```

## Result

```text
candidate count:                    5
scattered acceptance gate:          0.1
correct contract symmetric L2:      0.0
correct contract passes gate:       true
wrong contract min symmetric L2:    0.26554256916978447
wrong contract pass count:          0
smoke contract discriminates:       true
project-core bridge ready:          false
project-core FDTD comparison ready: false
real 3D validation ready:           false
field FWI ready:                    false
gpu/hpc ready:                      false
```

Candidate metrics:

| Candidate | Symmetric L2 | Passes gate |
| --- | ---: | --- |
| correct_per_receiver_delay_and_scale | 0.0 | true |
| no_delay_or_scale | 1.447317547533237 | false |
| global_mean_delay_and_scale | 1.5700724189128519 | false |
| wrong_phase_sign_per_receiver | 1.4512985931949443 | false |
| receiver_reversed_contract | 0.26554256916978447 | false |

## Interpretation

The synthetic smoke proves that the contract machinery can discriminate. The
correct per-receiver delay, complex scale, and Hermitian reconstruction passes
exactly. Missing delay, one global delay, opposite phase sign, and receiver
reversal all fail the `0.1` scattered-field gate.

This validates the synthetic mechanics of the contract, not the real
project-core BEM/FDTD bridge.

## Decision

Use this smoke as the synthetic contract guard for the next project-core adapter
rerun. Project-core FDTD/BEM agreement, 3D validation, GPU/HPC, and field FWI
remain blocked until the real adapter passes the contract and comparison gates.

## Validation

Focused test:

```text
tests/test_project_core_bem_causal_reconstruction_synthetic_smoke.py
5 passed
```

Figure validation:

```text
project_core_bem_causal_reconstruction_synthetic_smoke.png
2859x839, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_causal_reconstruction_synthetic_smoke.py
sha256=bda4bb0436e322b21ca642792598c1b5d70eb99b4f2685d132477997917e2ca1

tests/test_project_core_bem_causal_reconstruction_synthetic_smoke.py
sha256=673fd5f34aa9945fa2f903efc2cd29fcddd01e9765b161ae5ff309b3c2d0a7a3
```
