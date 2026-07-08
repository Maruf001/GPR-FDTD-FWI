# Paper Notes: Qin, Bohlen, and Allroggen 2023, Frequency-Dependent GPR FWI

Source PDF: `paper/ggac319.pdf`

Rendered visual pages inspected: `outputs/literature_method_work/2026-07-03_paper_vision_pages/ggac319/`

Text extraction used for equations/tables: `outputs/literature_method_work/2026-07-03_paper_vision_pages/raw_text/ggac319.txt`

## Bibliographic Details

Title: Full-waveform inversion of ground-penetrating radar data in frequency-dependent media involving permittivity attenuation

Authors: Tan Qin, Thomas Bohlen, Niklas Allroggen

Journal: Geophysical Journal International, 2023, volume 232, pages 504-522

DOI: `10.1093/gji/ggac319`

## Main Problem

The paper extends GPR full-waveform inversion from the usual frequency-independent parameterization to a frequency-dependent medium model. Standard GPR FWI often inverts only relative permittivity and electrical conductivity as if both were constant over the GPR bandwidth. That assumption can produce false or unstable estimates when shallow materials have dispersive dielectric behavior or strong attenuation.

The authors introduce a permittivity attenuation parameter, `tau_epsilon`, using the tau-method from seismic viscoelastic wave modeling. The key point is not simply adding another unknown; they reformulate Maxwell's equations so that the forward and adjoint problems remain self-adjoint and therefore compatible with the same time-domain wave solver.

## Core Method

The forward problem starts from Maxwell's equations with convolutional constitutive relations:

```text
B = mu H
D = epsilon * E
Jc = sigma * E
```

The convolution terms `epsilon * dE/dt` and `sigma * E` are replaced by auxiliary differential equations and memory variables. For dielectric permittivity, the authors use a Debye relaxation model and define:

```text
tau_epsilon = 1 - tau_E / tau_D
```

where `tau_E` and `tau_D` are relaxation times for the electric field and displacement in the Debye model. `tau_epsilon` is dimensionless, bounded by `0 <= tau_epsilon < 1`, and is meant to represent attenuation/dispersion caused by complex permittivity.

For conductivity, the paper also discusses a Kelvin-Voigt-type relaxation parameter `tau_sigma`, but the actual examples set `tau_sigma = 0` so that the analysis focuses on permittivity attenuation.

The method replaces convolution with:

```text
epsilon * dE/dt + sigma * E = epsilon_e_inf dE/dt + sigma_e_inf E + sum(memory variables)
```

The effective optical parameters are linked to the static parameters and attenuation parameters. The inversion can update either static parameters or effective parameters at the reference angular frequency.

## Inversion Objective

The FWI objective is the standard least-squares waveform residual:

```text
Phi(m) = 0.5 || R u(m) - d_obs ||_2^2
```

where:

- `u(m)` is the modeled wavefield.
- `R` restricts the wavefield to receiver positions.
- `d_obs` is observed data.
- `Delta d = R u(m) - d_obs` is the residual.

The model is updated iteratively:

```text
m_{k+1} = m_k + lambda * Delta m_{k+1}
```

The update direction is conjugate-gradient based, using a Polak-Ribiere scale factor and a preconditioner. Step length is found by line search. The authors use separate step lengths for different parameter classes because permittivity, conductivity, and attenuation have different data sensitivities.

They also use multiscale inversion to reduce cycle skipping. In the field case, the frequency bands progress through approximately:

```text
5-30 MHz, 5-40 MHz, 5-50 MHz, 5-70 MHz, 5-100 MHz
```

## Adjoint and Gradient

The important technical contribution is the self-adjoint form of the modified Maxwell system. Because the modified operators are self-adjoint, the same forward solver can be reused for adjoint backpropagation by reversing time.

The residual is injected as the adjoint source:

```text
adjoint source = R^T Delta d
```

The gradient is computed by zero-lag cross-correlation of forward and adjoint wavefields:

```text
dPhi/dm = integral adjoint_wavefield * (dM1/dm d_t forward_wavefield + dM2/dm forward_wavefield) dt
```

The paper emphasizes that the reformulation keeps model parameters on diagonal terms in the system matrices, simplifying the gradient expressions.

Parameters of interest in this paper:

- Effective relative permittivity at reference frequency, `epsilon_r`.
- Effective conductivity at reference frequency, `sigma`.
- Static permittivity/conductivity variants via chain rule.
- Permittivity attenuation, `tau_epsilon`.
- Conductivity relaxation `tau_sigma`, discussed but not actively estimated in the examples.

## Figure-Level Notes From Visual Reading

### Figure 1: Waveform and spectrum behavior

This figure compares homogeneous 1-D responses for:

- Non-attenuating medium.
- Conductivity attenuation only.
- Frequency-dependent permittivity attenuation.

The plot shows that permittivity attenuation acts like a low-pass filter: higher frequencies are attenuated more strongly, the waveform is distorted, and the spectrum shifts toward lower frequencies. Conductivity attenuation mostly scales amplitudes more uniformly over frequency.

This matters for field data because a simple frequency-independent conductivity term can mimic some amplitude loss but cannot reproduce frequency-dependent waveform distortion.

### Figure 2: Frequency-dependent material characteristics

The panels show quality factor, attenuation factor, phase velocity, effective conductivity, and effective permittivity versus frequency. The gray source spectrum highlights which part of the curves the source actually probes.

Important visual point: the same nominal reference medium can have frequency-dependent velocity and attenuation over the source band. If the GPR bandwidth overlaps the dispersive part of the material response, waveform fitting is sensitive to the choice of model parameterization.

### Figures 3-8: Synthetic inversion examples

The synthetic model figures compare true models, frequency-dependent inversion results, and frequency-independent inversion results. Visually:

- Frequency-dependent FWI can reduce artifacts in conductivity when attenuation is truly dominated by permittivity attenuation.
- `tau_epsilon` itself is weakly resolved and crosstalk-prone.
- Frequency-independent FWI can still reconstruct comparable permittivity when dispersion is weak, but it tends to introduce artifacts in conductivity and cannot represent attenuation-dominated conductivity behavior.
- Source/receiver artifacts are present enough that the authors apply gradient tapering around sources/receivers.

The synthetic figures also show that surface multioffset GPR data have relatively low sensitivity to `tau_epsilon` compared with permittivity and conductivity.

### Figure 9: Field inversion model panels

The field figure is central. It shows:

- Initial model.
- Frequency-dependent FWI result.
- Frequency-independent FWI result.

Rows:

- Relative permittivity.
- Conductivity.
- Permittivity attenuation.

The known target is the Ettlinger Line trench, marked as a dashed triangular feature. Both FWI variants image a triangular permittivity anomaly, but the frequency-dependent model gives a more geologically consistent attenuation/conductivity interpretation, especially on the right side of the trench.

### Table 2: Field acquisition parameters

Raw field acquisition:

- 165 sources.
- 56-125 traces per gather.
- Transmitter spacing about 0.2 m.
- Receiver spacing about 0.1 m.
- Offset range about 0.2-17 m.
- Sample rate 0.2 ns.
- Recording window 200 ns.

FWI subset:

- 18 sources.
- 100-175 traces per gather.
- Transmitter spacing 2 m.
- Receiver spacing 0.04 m.
- Offset range 0.3-8 m.
- Sample rate 0.08 ns.
- Recording window 164 ns.

This is a multioffset surface acquisition, not a single common-offset B-scan.

### Table 3: Field preprocessing

The field-data preprocessing sequence is:

1. Frequency-domain resampling.
2. Interpolation of clipped direct-arrival amplitudes.
3. DC-shift removal and dewow.
4. Bandpass filtering, 5-400 MHz.
5. Bad-trace removal and offset limitation.
6. Data gridding in the time-offset domain.
7. 3-D to 2-D transformation.

The last step is important. Their field data are acquired in the real 3-D world but inverted with a 2-D line-source solver. They explicitly correct reflected-wave phase/amplitude differences between 3-D and 2-D before FWI.

### Figure 10: Field data fitting and source wavelets

The data-fit panel shows observed, frequency-independent, and frequency-dependent traces for one radargram. Both FWIs struggle with air/ground waves because antenna radiation and antenna-ground coupling are not fully represented by the 2-D solver.

Frequency-dependent FWI better matches reflection amplitudes at larger offsets, especially beyond about 4 m. The estimated source wavelets also differ between the first 11 and last 7 gathers, likely due to acquisition over two days and changing near-surface moisture/coupling.

## Field Example Details

The field test is at Rheinstetten, Germany, over the Ettlinger Line, a refilled early-17th-century defensive trench. The site was previously studied using 3-D GPR migration, surface-wave methods, and seismic FWI, so there is independent geophysical context.

Instrument/setup:

- Single-channel pulseEKKO Pro GPR.
- pulseEKKO Ultra receiver.
- Nominal transmitter center frequency: 200 MHz.
- HH orientation to acquire TM wave data.
- Receiver moved on a sledge and tracked with RTK/total-station positioning.
- Multioffset gathers acquired by fixing transmitter and moving receiver.

Initial model:

- Domain: 7 m by 45.2 m.
- Grid spacing: 0.04 m.
- Air layer of 1 m exists but is omitted in the plotted model.
- Initial relative permittivity: 9 at the ground, decreasing to 8 at 6 m depth.
- Initial conductivity: 6 mS/m at ground, decreasing to 2 mS/m at 6 m depth.
- Initial `tau_epsilon`: 0.1.
- Debye relaxation frequency: 50 MHz.
- Reference angular frequency: `omega_0 = 2 pi f_l`.

Key field result:

- Both frequency-dependent and frequency-independent FWIs recover the trench as a permittivity anomaly.
- Frequency-dependent FWI gives better reflection-amplitude fitting at larger offsets and a more continuous/conservative conductivity interpretation in high attenuation areas.
- Final scalar misfits are similar, less than about 1 percent different, so the authors argue from reflection fit and model plausibility rather than only final objective value.

## Main Conclusions

The paper's main technical conclusion is that the tau-method gives a practical frequency-dependent GPR FWI formulation. It allows frequency-dependent attenuation/dispersion to be modeled while preserving a self-adjoint structure and relatively simple gradients.

The main geophysical conclusion is more nuanced:

- `tau_epsilon` is physically meaningful and can improve conductivity reconstruction.
- Surface multioffset GPR data are weakly sensitive to `tau_epsilon`.
- Permittivity attenuation is difficult to estimate cleanly because of weak sensitivity and parameter crosstalk.
- Frequency-independent FWI can still work reasonably when attenuation is weak, but becomes less reliable when conductivity behavior is actually dominated by permittivity attenuation.

## Relevance to Our GSSI 51600S Field B-Scans

This paper is state-of-the-art for adjoint-gradient GPR FWI in dispersive media, but it is not immediately a drop-in method for our local GSSI common-offset files.

Directly transferable components:

- Least-squares waveform objective.
- Adjoint-state gradient structure.
- Multiscale frequency continuation.
- Separate parameter step lengths or optimizer schedules for different physical parameters.
- Field preprocessing discipline: dewow, DC shift, bad traces, bandpass, gridding, offset/window selection.
- Source wavelet estimation/handling as a core part of FWI rather than a cosmetic detail.

Major adaptation issues for our GSSI profiles:

- Their field method relies on multioffset gathers; our GSSI field data appear to be common-offset B-scans.
- Their data subset contains 18 source gathers with offsets from 0.3 to 8 m; our profile geometry must be inferred from DZT/DZX metadata and survey notes.
- Their inversion uses 2-D line-source correction for 3-D acquired reflections. If we use a 2-D solver for our common-offset data, we need a comparable decision about 3-D-to-2-D amplitude/phase correction or accept that amplitude fitting will be biased.
- Their targets are trench/near-surface geologic anomalies, not small metallic rebars. Rebar inversion would need a PEC or high-conductivity inclusion parameterization and a much higher center-frequency regime.
- `tau_epsilon` is likely too weakly constrained by single common-offset profiles unless we have strong attenuation/coupling evidence or multi-offset data.

## How To Test This Paper Separately On Our Field Data

A paper-faithful validation should not mix in rebar hyperbola fitting as the main inversion method. It should be a standalone frequency-dependent FWI track:

1. Import one GSSI profile and establish geometry from metadata.
2. Apply field preprocessing analogous to Table 3, adapted to common-offset data:
   - time-zero correction,
   - dewow/DC removal,
   - bandpass in plausible antenna band,
   - trace gridding if trace spacing is irregular,
   - direct-wave/background handling.
3. Estimate or parameterize the source wavelet.
4. Start with a 2-D effective medium model:
   - background `epsilon_r`,
   - background `sigma`,
   - optional `tau_epsilon` initialized to a constant.
5. Run frequency-independent FWI first only as the paper's comparison baseline.
6. Run frequency-dependent FWI with the same data, source, initial model, and windows.
7. Compare:
   - waveform residual by time window,
   - reflection amplitude fit,
   - stability of conductivity model,
   - sensitivity and spatial coherence of `tau_epsilon`.

For our rebar goal, this paper is more useful for material-field inversion and attenuation-aware waveform fitting than for estimating rebar radius directly. It may become important after a Jazayeri-style rebar geometry model is available and we need to account for concrete attenuation/conductivity.

## Implementation Notes

Minimum implementation pieces needed:

- 2-D TM FDTD solver with fields compatible with the paper's formulation.
- Memory variable update for Debye permittivity attenuation.
- Adjoint solver using the same forward operator in reversed time.
- Receiver restriction and residual injection.
- Gradients for `epsilon`, `sigma`, and optionally `tau_epsilon`.
- Frequency continuation.
- Per-parameter scaling or separate step lengths.
- Source/receiver gradient taper.
- Source wavelet estimation or joint source update.

Practical staged implementation for our codebase:

- First reproduce frequency-independent adjoint FWI on a tiny controlled 2-D profile.
- Then add the Debye memory variable and verify waveform differences against the paper's Figure 1 behavior.
- Then run a field-data comparison where the only variable is the frequency-dependent parameterization.

The important constraint is that this track should be kept separate from Jazayeri rebar FWI, accelerator CUDA/PyTorch FWI, and hyperbola fitting. It should answer only: does frequency-dependent GPR FWI improve field waveform fit/material reconstruction for our data?

## Risks and Limitations

- Common-offset B-scans may not constrain `tau_epsilon` enough.
- The paper's successful field case depends on multioffset gathers and known independent geologic target geometry.
- 2-D modeling of 3-D field data can bias amplitude fitting unless corrected.
- Rebar-scale high-frequency GSSI data may require much finer grids than the Rheinstetten 200 MHz example.
- Metallic rebar scattering may dominate attenuation effects, making `tau_epsilon` hard to interpret unless the inversion windows avoid direct rebar-dominated returns or explicitly model PEC inclusions.

## One-Sentence Takeaway

This paper is the right reference for adjoint-gradient, frequency-dependent GPR FWI of permittivity/conductivity/attenuation, but for our GSSI rebar data it should be tested as a separate attenuation-aware waveform-fit/material inversion track, not as the primary radius-estimation method.
