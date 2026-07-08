# BEM Experiment 027: Project-Core Direct-Wave Effective Wavenumber Audit

Date: 2026-06-25

## Purpose

Check whether the project-core direct-wave mismatch can be explained by FDTD
numerical dispersion, modeled as a fitted real effective wavenumber for each
frequency.

This run reads the dense no-target direct-wave grid from run `023` and fits
`k_eff` against the offset-averaged direct response. It does not launch a new
FDTD solve.

## Output

```text
outputs/bem_experiments/027_project_core_direct_wave_effective_wavenumber_audit
```

Key artifacts:

```text
data/direct_wave_effective_wavenumber_summary.json
data/direct_wave_effective_wavenumber_frequency_metrics.csv
figures/direct_wave_effective_wavenumber.png
docs/DIRECT_WAVE_EFFECTIVE_WAVENUMBER_AUDIT.md
```

## Result

```text
source run:                         outputs/bem_experiments/023_project_core_dense_direct_wave_green_transfer_audit
frequency count:                    17
mean analytic-k symmetric L2:       1.6246350401682335
mean fitted-k symmetric L2:         1.5074140243698353
median effective k ratio:           0.835753777485865
effective wavenumber model ready:   false
```

## Interpretation

Fitting a real effective wavenumber helps only slightly and does not make the
direct-wave model usable. The optimizer often hits broad bounds or produces
unstable `k` ratios, which means the mismatch is not just a simple FDTD phase
velocity correction.

## Decision

Do not build a dispersion-corrected continuous Green-function bridge from this
result. The blocker remains source/receiver coupling or discrete
Green-function structure.

## Validation

```text
python -m py_compile run_project_core_direct_wave_effective_wavenumber_audit.py
conda run -n gpr-fdtd-fwi python run_project_core_direct_wave_effective_wavenumber_audit.py
```

Figure check:

```text
1 PNG figure, nonblank dynamic range, 1816x701
```
