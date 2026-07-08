# BEM Experiment 137: Phase-Corrected Residual Spectrum Audit

Date: 2026-06-27

## Purpose

Analyze the residual spectrum after applying the best per-receiver phase
correction from run `134`.

Run `134` showed that per-receiver phase correction improves the project-core
BEM/FDTD bridge but does not pass the `0.1` scattered-field gate. This run asks:

```text
Where does the residual remain after that best phase correction?
```

This is a CPU-only audit of saved spectra. It does not rerun FDTD or BEM
solvers, compare against field data, launch GPU/HPC work, run 3D validation,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/137_project_core_bem_phase_corrected_residual_spectrum_audit
```

Key artifacts:

```text
data/project_core_bem_phase_corrected_frequency_residuals.csv
data/project_core_bem_phase_corrected_receiver_residuals.csv
data/project_core_bem_phase_corrected_residual_spectrum_audit_summary.json
figures/project_core_bem_phase_corrected_residual_spectrum_audit.png
docs/PROJECT_CORE_BEM_PHASE_CORRECTED_RESIDUAL_SPECTRUM_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
frequency count:                      17
receiver count:                       7
overall spectral relative L2:         0.18500684021427602
frequency bins passing 0.1 gate:      1
receiver rows passing 0.1 gate:       0
worst frequency:                      0.6247724137942329 GHz
worst frequency relative L2:          0.45939283372879625
best frequency:                       1.3744993103473124 GHz
best frequency relative L2:           0.0953354196293874
median frequency relative L2:         0.1811125268125065
worst receiver index:                 3
worst receiver spectral relative L2:  0.20025157145242628
global amplitude ratio min/median/max: 0.6359276019772239 / 0.9893038652215023 / 1.3260375042484889
phase-corrected bridge ready:         false
project-core FDTD comparison ready:   false
real 3D validation ready:             false
field FWI ready:                      false
gpu/hpc ready:                        false
```

Key frequency residuals:

| Frequency (GHz) | Relative L2 | Passes gate |
| ---: | ---: | --- |
| 0.6247724137942329 | 0.45939283372879625 | false |
| 0.7497268965530794 | 0.36959706921344904 | false |
| 1.3744993103473124 | 0.0953354196293874 | true |
| 2.374135172418085 | 0.22498849682021174 | false |

## Interpretation

After per-receiver phase correction, the residual is largest at the
low-frequency edge and smaller in the midband. The best bin, near `1.3745 GHz`,
passes the `0.1` gate, but the overall spectrum remains at relative L2
`0.1850`, and no receiver passes as a whole.

The remaining blocker is not one global phase shift. The next adapter work
should focus on band-edge handling, source spectrum conditioning, and observable
scaling.

## Decision

Keep the phase-corrected project-core bridge blocked. Do not promote
project-core FDTD/BEM comparison, 3D validation, GPU/HPC, or field FWI from this
bridge.

## Validation

Focused test:

```text
tests/test_project_core_bem_phase_corrected_residual_spectrum_audit.py
4 passed
```

Figure validation:

```text
project_core_bem_phase_corrected_residual_spectrum_audit.png
2896x845, dynamic range=255
```

Script snapshots:

```text
run_project_core_bem_phase_corrected_residual_spectrum_audit.py
sha256=96713d4f566e875a54ec446c2b326b4136a8248d70a8f8bcd728582fd744b421

tests/test_project_core_bem_phase_corrected_residual_spectrum_audit.py
sha256=f99d7d2cf7f8b7e3b189b2744b71c56de51ded09675858565c7c293916a3bb9b
```
