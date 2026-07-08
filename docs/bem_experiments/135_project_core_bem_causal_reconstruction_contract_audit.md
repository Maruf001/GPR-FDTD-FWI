# BEM Experiment 135: Causal Reconstruction Contract Audit

Date: 2026-06-27

## Purpose

Package the source-wavelet, time-origin, reconstruction, and observable
requirements that must be closed before rerunning the project-core BEM/FDTD
scattered-field bridge.

Runs `133` and `134` showed that timing and phase explain a large part of the
scattered-field mismatch, but no tested correction passes the `0.1` comparison
gate. This run asks:

```text
What contract must be closed before another project-core scattered bridge rerun
can be interpreted?
```

This is a CPU-only audit of saved run `017`, run `133`, and run `134` outputs.
It does not rerun FDTD or BEM solvers, compare against field data, launch
GPU/HPC work, run 3D validation, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/135_project_core_bem_causal_reconstruction_contract_audit
```

Key artifacts:

```text
data/project_core_bem_causal_source_phase_candidates.csv
data/project_core_bem_causal_reconstruction_evidence.csv
data/project_core_bem_causal_reconstruction_contract.csv
data/project_core_bem_causal_reconstruction_contract_audit_summary.json
figures/project_core_bem_causal_reconstruction_contract_audit.png
docs/PROJECT_CORE_BEM_CAUSAL_RECONSTRUCTION_CONTRACT_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
evidence items:                         4
contract items:                         5
blocking contract items:                4
scattered acceptance gate:              0.1
best evidence item:                     run134_best_phase_slope_candidate
best evidence symmetric L2:             0.1866176083623045
best evidence passes gate:              false
causal contract ready:                  false
project-core bridge ready:              false
project-core FDTD comparison ready:     false
real 3D validation ready:               false
field FWI ready:                        false
gpu/hpc ready:                          false
source phase candidates:                5
```

Source-phase candidates:

| Candidate | Symmetric L2 | Relative L2 vs FDTD | Passes gate |
| --- | ---: | ---: | --- |
| source_normalized_baseline | 1.3943651626310445 | 1.4641925358593955 | false |
| multiply_source_phase_only | 1.4168452903409412 | 1.4877984291218809 | false |
| multiply_conjugate_source_phase_only | 1.3934576407325323 | 1.4632395668484495 | false |
| multiply_full_source_spectrum | 1.967066180154767 | 60.13741280883545 | false |
| multiply_conjugate_full_source_spectrum | 1.9665190619615256 | 60.12068623757206 | false |

Contract items:

| Contract item | Status | Blocking | Required before bridge |
| --- | --- | --- | --- |
| source_wavelet_phase_convention | open | true | state whether BEM spectra include the FDTD source wavelet, its phase convention, and its time origin |
| per_receiver_delay_model | open | true | define the propagation-delay convention for each source/receiver pair before inverse FFT |
| causal_hermitian_reconstruction | open | true | define selected-bin placement, conjugate symmetry, time-zero placement, and causal windowing |
| scattered_observable_definition | open | true | state the exact field component, sign, target-minus-background convention, and receiver sampling location |
| acceptance_gate | defined | false | retain the 0.1 scattered-field gate unless a documented threshold update is approved |

## Interpretation

The saved FDTD source-wavelet phase alone does not repair the scattered-field
mismatch. Applying the source phase, conjugate source phase, full source
spectrum, or conjugate full source spectrum leaves the response far outside the
gate.

The strongest current evidence remains the per-receiver phase-slope diagnostic
from run `134`, with symmetric relative L2 `0.1866176083623045`. That is a real
improvement, but it still fails the `0.1` gate.

The next project-core bridge rerun needs an explicit causal reconstruction
contract. Without that contract, another adapter run would not tell whether the
remaining error comes from source phase, per-receiver propagation delay,
Hermitian reconstruction, observable definition, or actual method disagreement.

## Decision

Keep the project-core BEM/FDTD bridge blocked. Do not run project archive
comparison, 3D validation, GPU/HPC, or field FWI from this bridge until the
source-wavelet phase, per-receiver delay, Hermitian reconstruction, and
scattered-observable contract items are closed.

## Validation

Focused test:

```text
tests/test_project_core_bem_causal_reconstruction_contract_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_causal_reconstruction_contract_audit.png
2409x847, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_causal_reconstruction_contract_audit.py
sha256=6794c3313dfa502f2276f816c5b90eac9792ae4e1b564ed972a002ae0bea1838

tests/test_project_core_bem_causal_reconstruction_contract_audit.py
sha256=ae0c8f8d6e3f57a4434759b4324dbc6b21bf0c5f61a779ee057c86bcbadcce34
```
