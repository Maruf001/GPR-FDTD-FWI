# Experiment 49: Material/Source Branch Animation Summary

## Goal

Close the remaining material/source visualization item from the master plan
using only branches that were real competitors in previous objective results.

This is not a new optimizer claim. It packages visual evidence for two already
observed ambiguity mechanisms:

```text
material branch: experiment 056, same true geometry with lower effective steel
conductivity

source branch: experiment 052, fixed-source inversion choosing high-radius
candidates when the observed wavelet was perturbed
```

## Code Change

Extended `run_wavefield_comparison_animation.py` so true and candidate panels
can use separate single-rebar material overrides:

```text
truth/candidate concrete epsr
truth/candidate concrete sigma
truth/candidate rebar epsr
truth/candidate rebar sigma
```

The material override guard remains inherited from `run_wavefield_animation.py`:
material-aware animations currently support exactly one rebar. Multi-rebar
geometry-only and source-mismatch comparison animations keep the existing path.

Focused validation:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_wavefield_animation.py
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile run_wavefield_comparison_animation.py run_wavefield_animation.py
```

Result:

```text
10 passed in 0.34 s
py_compile passed
```

## Run 420

Output:

```text
outputs/experiments/420_material_source_branch_animation_summary
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_wavefield_comparison_animation.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --truth-x-values-mm 250 \
  --truth-z-values-mm 90 \
  --truth-radius-values-mm 6 \
  --candidate-x-values-mm 250 \
  --candidate-z-values-mm 90 \
  --candidate-radius-values-mm 6 \
  --truth-concrete-epsr 6.0 \
  --truth-rebar-sigma 1e7 \
  --candidate-concrete-epsr 6.0 \
  --candidate-rebar-sigma 1e5 \
  --frequency-ghz 1.5 \
  --source-x-mm 240 \
  --save-every 80 \
  --fps 12 \
  --label material_sigma1e5_vs_true \
  --title 'Material branch: true sigma 1e7 vs saturated sigma 1e5' \
  --outdir outputs/experiments/420_material_source_branch_animation_summary
```

Generated artifact:

| Animation | Branch | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `figures/material_sigma1e5_vs_true_comparison.gif` | experiment 056 true `1e7 S/m` steel vs same-radius `1e5 S/m` steel candidate | 48 | `1550x560` | 255 | 39.3504 |

Figure notes:

```text
outputs/experiments/420_material_source_branch_animation_summary/figures/FIGURE_NOTES.md
```

Manifest:

```text
outputs/experiments/420_material_source_branch_animation_summary/data/branch_animation_manifest.json
```

## Referenced Source-Mismatch Branches

These were already generated and validated in experiment 052. They are included
in the run 420 manifest because they satisfy the same "actual branch" rule for
source ambiguity.

| Source comparison | Actual fixed-source wrong candidate | Frames | Size | Dynamic range | Mean frame std |
| --- | --- | ---: | --- | ---: | ---: |
| `fc_high10_truth_vs_nominal_r7p8_candidate_comparison.gif` | nominal-source `r=7.8 mm` | 48 | `1550x560` | 255 | 38.9175 |
| `delay_minus50ps_truth_vs_nominal_r7p8_candidate_comparison.gif` | nominal-source `r=7.8 mm` | 48 | `1550x560` | 255 | 39.6986 |
| `amp_high10_truth_vs_nominal_r7p0_z91_candidate_comparison.gif` | nominal-source `z=91 mm, r=7.0 mm` | 48 | `1550x560` | 255 | 39.6960 |

## Interpretation

The material and source cases are different kinds of ambiguity.

Material result:

```text
Rebar conductivity is nearly saturated for the standard single-rebar setup.
Changing effective steel conductivity from 1e7 to 1e5 S/m gives a visually and
objectively similar wavefield at the true 6.0 mm radius. This does not erase
radius evidence; it says steel conductivity should be treated as a reporting
or calibration nuisance, not as a free production optimizer parameter.
```

Source result:

```text
Source wavelet mismatch can create real wrong-radius branches under fixed-source
least squares. The source-aware comparison GIFs show perturbed observed truth
against the nominal-source candidates that caused the original radius bias.
This is why source amplitude, timing, and center-frequency profiling remains
mandatory before trusting radius estimates under mismatch or field-like data.
```

## Decision

The master-plan animation item is closed. Future material/source animations
should only be added when a new objective matrix exposes a real competing
branch worth visualizing.

Next marathon branch:

```text
Choose a new stressor from the handoff matrix instead of reopening close14
noise bisection: field-like source calibration, a material perturbation tied
to a known ambiguity branch, or an uncovered staged variable-radius geometry.
```
