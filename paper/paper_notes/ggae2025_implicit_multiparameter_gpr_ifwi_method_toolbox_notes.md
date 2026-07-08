# GGAE2025 IFWI Method Toolbox Notes

Paper: Sun, Liu, Lin, Xing, and Liu, "Implicit multiparameter full waveform inversion of multioffset ground penetrating radar data", Geophysical Journal International, 240, 904-919, DOI `10.1093/gji/ggae420`.

Local file: `paper/ggae2025.pdf`

Reading artifacts:

- Extracted text: `outputs/literature_method_work/2026-07-03_ggae2025/raw_text/ggae2025.txt`
- Rendered pages: `outputs/literature_method_work/2026-07-03_ggae2025/pages/`
- Contact sheets inspected:
  - `outputs/literature_method_work/2026-07-03_ggae2025/contact_sheets/ggae2025_01_04.png`
  - `outputs/literature_method_work/2026-07-03_ggae2025/contact_sheets/ggae2025_05_08.png`
  - `outputs/literature_method_work/2026-07-03_ggae2025/contact_sheets/ggae2025_09_12.png`
  - `outputs/literature_method_work/2026-07-03_ggae2025/contact_sheets/ggae2025_13_16.png`

## Core Idea

The paper proposes implicit full waveform inversion (IFWI) for GPR. Instead of treating every grid cell's permittivity and conductivity as independent trainable variables, IFWI represents the subsurface parameters as the output of a coordinate neural network:

`m(x, z) = N_theta(x, z)`

The network is trained through a differentiable time-domain GPR forward model, so the neural network weights are the optimization variables. The intended benefit is that neural networks tend to learn lower spatial frequencies first, then finer details. The authors use this spectral-bias/frequency-principle behavior as an automatic multiscale inversion mechanism, avoiding manual low-to-high frequency band selection.

## Problem Being Addressed

Traditional GPR FWI is high resolution but sensitive to local minima, cycle skipping, and poor initial models. Standard multiscale FWI helps, but still requires:

- a useful initial model,
- accessible low-frequency information or artificial low-frequency extraction,
- manual frequency band design,
- careful balancing of multiparameter sensitivity.

The paper positions IFWI as a physics-constrained neural representation that reduces dependence on initial model quality.

## Traditional FWI Formulation In Paper

The paper uses time-domain Maxwell equations and minimizes an L2 waveform misfit over sources, receivers, and time samples. The inverted parameter vector is relative permittivity and conductivity, with conductivity scaled in `mS/m` for numerical stability:

`m = [epsr, sigma * 1000]^T`

The forward data are the electric-field component from GPR acquisitions. Gradients can be computed by adjoint methods or, in an RNN/differentiable-programming implementation, by automatic differentiation through the time-stepping operator.

Implementation note: the authors emphasize that RNN-based FWI is theoretically consistent with adjoint-state FWI, but easier to implement inside deep-learning frameworks. They use Adam in the numerical examples.

## IFWI Formulation

The paper reformulates FWI as a physics-guided implicit neural representation:

- Input: spatial coordinates.
- Output: subsurface physical parameters, here `epsr` and `sigma`.
- Loss: waveform mismatch after running Maxwell forward modelling on the network-generated model.

The neural network does not replace the wave equation. The wave solver remains the physical constraint. The network is only the model parameterization.

## Network Architecture Used

The paper uses simple MLPs:

- 4 hidden layers.
- 128 or 256 neurons per layer in sensitivity studies.
- Sinusoidal activation similar to SIREN.
- Scaling factor `omega0`, often tested at `[1, 10, 20, 30]`.
- Output normalization by approximate global mean and standard deviation:
  - network predicts normalized parameters,
  - physical parameters are recovered by `m = m_tilde * std + mean`.

The authors state that the global mean/std do not need to be exact. They are used to keep network outputs near zero mean and unit variance, accelerating convergence.

## Regularization And Tuning

Important tuning controls:

- `omega0` controls the spatial-frequency capacity of the sinusoidal network.
- Too small `omega0`, such as `1`, only recovers broad trends.
- Larger `omega0`, such as `20-30`, can represent detailed structures.
- Too large a frequency capacity can introduce high-frequency artifacts.
- Dropout can regularize high-frequency artifacts.

The paper's tuning guidance:

- Start with a relatively large `omega0`, around `20` or `30`.
- For shallow-to-middle targets, a wider network with dropout is recommended.
- For deeper targets, a narrower network with reduced `omega0` may be preferable, because widening/dropout can compromise deep accuracy.
- Data misfit alone can be misleading: the visually/structurally best model may not be the minimum-misfit model.

For our GSSI rebar work, the shallow-to-middle guidance matters more than the deep-target guidance.

## Numerical Examples

### Cross-Shape Model

Synthetic setup:

- 2D cross-shaped anomalies.
- Relative permittivity and conductivity inverted simultaneously.
- Dense surrounding acquisition with 32 transmitting and 64 receiving antennas.
- Ricker source, dominant frequency `100 MHz`.
- Time-domain simulation.

Findings:

- FWI works when the initial model is already a smooth version of the truth.
- FWI from a homogeneous initial model fails or gives distorted conductivity.
- Multiscale FWI improves recovery, but requires manual stages and frequency selection.
- IFWI from the same homogeneous model recovers anomaly locations and shapes better.
- Dropout-IFWI gives sharper anomaly boundaries and reduces background artifacts.

Visual note:

- Figures 7-8 are the most useful cross-shape comparison. They show conventional FWI, multiscale FWI, IFWI, and dropout-IFWI side by side.

### Overthrust Model

Synthetic setup:

- 2D Overthrust section.
- Width about `12.5 m`, depth about `4.7 m`.
- Grid spacing `5 cm`.
- Air layer above the model.
- 12 sources at 1 m spacing.
- Receiver at each grid point near surface.
- Ricker source, dominant frequency `100 MHz`.
- Multioffset on-ground acquisition.

Findings:

- Multiscale FWI succeeds with accurate 1D initial models.
- Multiscale FWI degrades when the 1D initial model is inaccurate.
- IFWI from the inaccurate initial model gives better structure and lower residuals than multiscale FWI.
- Preliminary IFWI still shows high-frequency artifacts and imperfect parameter values, motivating hyperparameter analysis.

Visual note:

- Figures 10-15 are the main Overthrust evidence.

## Hyperparameter Sensitivity

Metrics:

- `R2` for model-value accuracy.
- `SSIM` for structural similarity.
- `SNR` for high-frequency noise.
- `MAPE` for data misfit.

Key observations:

- `omega0=1` underfits detailed subsurface structure.
- Increasing `omega0` improves representation capacity.
- Very high frequency capacity increases artifacts.
- In the zero-dropout comparison, `omega0=20` performs best for both `128x4` and `256x4` MLPs.
- With `omega0=30`, increasing dropout does not clearly improve IFWI and can increase data misfit.
- With `omega0=20`, dropout improves high-frequency artifact suppression and shallow-layer accuracy.
- Wider `256x4` networks can slightly improve middle-depth features, but not always deep accuracy.

Visual note:

- Figures 16-24 are a useful tuning atlas: `omega0`, width, and dropout are varied systematically.

## What Is State Of The Art Here

The useful methodological contribution is not "use a neural net instead of physics". It is:

- keep a differentiable Maxwell/FDTD forward model,
- replace grid-cell independent material variables with an implicit coordinate neural representation,
- optimize network weights by waveform misfit,
- exploit spectral bias as automatic multiscale behavior,
- tune representation bandwidth with `omega0`, width, and dropout.

This makes IFWI a regularized parameterization for waveform inversion.

## Limits For Our Field Rebar Problem

The paper is not a direct match to our current GSSI data:

- It is synthetic, not field-data validated.
- It uses dense multioffset acquisition, not one limited B-scan profile.
- It inverts continuous `epsr` and `sigma` fields, not explicit steel rebar geometry.
- It does not solve the diameter identifiability issue for metallic cylinders.
- It does not address source wavelet uncertainty, time-zero uncertainty, antenna coupling, or real concrete clutter.

Therefore, it should not replace the current Jazayeri/Liu/Giannakis field evidence. It should be used as a toolbox component for parameterization and regularization.

## Most Relevant Adaptation To Our GSSI 51600S Data

The best near-term adaptation is a shallow-window IFWI adapter around the current g3 field anchor:

1. Keep the existing differentiable PyTorch 2D TMz/FDTD field runner and measured-wavelet objective.
2. Replace, or augment, the grid/material parameterization with a coordinate MLP over the local g3 window.
3. Let the MLP output smooth `epsr(x,z)` and possibly `sigma(x,z)` for concrete/background.
4. Keep explicit geometry parameters for the rebar or use a hybrid level-set/anomaly parameterization rather than asking a smooth MLP to learn steel diameter directly.
5. Start with `omega0=20`, `4` hidden layers, `128` or `256` neurons, dropout `0.1-0.2`.
6. Compare against the current g3 LBFGS anchor:
   - waveform loss,
   - x location,
   - cover depth,
   - diameter range or non-uniqueness,
   - runtime/evaluations,
   - robustness across initial radius.

## Why Not Use IFWI Directly For Diameter

The current field evidence already shows diameter non-uniqueness for g3 even when waveform fit is good. A coordinate MLP may fit waveforms better by bending smooth permittivity/conductivity fields, but that does not automatically identify the steel radius. It may even make radius less identifiable by giving the background more freedom.

To make IFWI useful for diameter, we need constraints:

- explicit steel/rebar geometry parameter,
- shared concrete background across events,
- source/time-zero calibration,
- multiple profiles or offsets,
- priors on realistic concrete permittivity/conductivity,
- holdout traces or profiles.

Without those, IFWI should be treated as a regularized field-fit/initial-model tool, not a diameter validator.

## Candidate Implementation Branches

### Branch A: G3 IFWI Background Adapter

Goal: determine whether an implicit neural background improves g3 waveform fit while keeping location/cover stable.

Inputs:

- `PROJECT001C__014`
- existing g3 event window
- measured wavelet
- current LBFGS geometry anchor

Model:

- explicit rebar x/cover/radius parameters,
- MLP background field for `epsr(x,z)` and optional `sigma(x,z)`,
- regularization toward plausible concrete values,
- dropout or reduced `omega0`.

Acceptance:

- lower loss than current LBFGS without moving x/cover implausibly,
- holdout traces do not degrade,
- diameter uncertainty narrows only if radius sweep shows a real loss separation.

### Branch B: IFWI-Only Smooth Field Sanity Check

Goal: test whether a pure coordinate MLP can fit the local g3 field window better than homogeneous concrete.

Model:

- no explicit rebar diameter claim,
- MLP outputs smooth `epsr/sigma`,
- compare residual structure only.

Use:

- good for diagnosing whether background heterogeneity is driving residuals,
- not sufficient for rebar diameter prediction.

### Branch C: Shared-Material Multi-Event Hybrid IFWI

Goal: use one shared concrete/background MLP across g1/g2/g3 and separate explicit rebar geometry parameters.

This is closer to the paper's multiparameter logic, but riskier because g2 currently fits poorly and may corrupt the shared model.

## Recommended Next Use

Do not jump straight to a full IFWI field claim. Implement Branch A first as a bounded paper-method adapter:

- method track: `sun_2025_ifwi_gpr` or `ggae2025_ifwi_gpr`
- output root: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/`
- first run: g3-only local measured-wavelet adapter
- required artifacts:
  - prediction CSV,
  - loss/history CSV,
  - holdout-trace residual CSV,
  - model/fit/convergence figures,
  - script snapshot and manifest,
  - leaderboard update.

## Strategy Takeaway

This paper gives us a principled way to regularize field FWI with a coordinate neural representation and automatic multiscale behavior. For our immediate rebar prediction problem, it is most valuable as a controlled parameterization experiment to test whether the g3 residuals are caused by overly simple concrete/background assumptions. It does not, by itself, solve the diameter ambiguity or replace explicit geometry inversion.
