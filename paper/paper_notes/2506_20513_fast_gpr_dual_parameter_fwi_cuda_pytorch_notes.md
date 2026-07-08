# Paper Notes: Liu et al. 2025, Fast Dual-Parameter GPR FWI With CUDA and PyTorch

Source PDF: `paper/accelerator/2506.20513v1.pdf`

Rendered visual pages inspected: `outputs/literature_method_work/2026-07-03_paper_vision_pages/accelerator_2506/`

Text extraction used for equations/tables: `outputs/literature_method_work/2026-07-03_paper_vision_pages/raw_text/accelerator_2506.txt`

## Bibliographic Details

Title: Fast ground penetrating radar dual-parameter full waveform inversion method accelerated by hybrid compilation of CUDA kernel function and PyTorch

Authors: Lei Liu, Chao Song, Liangsheng He, Silin Wang, Xuan Feng, Cai Liu

Version: arXiv preprint, `arXiv:2506.20513v1`, submitted 2025-06-25

## Main Problem

This paper focuses on making GPR full-waveform inversion fast enough for practical use. The scientific inversion target is dual-parameter reconstruction of relative permittivity and electrical conductivity from GPR waveform data. The engineering contribution is a CUDA/PyTorch hybrid implementation that accelerates forward and adjoint modeling while keeping the optimizer and loss interface in PyTorch.

The paper is not specifically about rebar radius estimation. It is relevant to our work because it gives a modern adjoint-gradient GPR FWI implementation strategy with Adam, TV regularization, staged learning rates, and field-data dual-parameter inversion.

## Core Method

The physical model is time-domain Maxwell/FDTD in 2-D transverse magnetic (TM) mode. The modeled field component used in the objective is electric field, written in the paper as `E_z`.

The FDTD update uses:

- electric field update with conductivity attenuation,
- magnetic field updates,
- PML boundary updates,
- source injection,
- receiver sampling.

The conductivity term is explicitly included in Ampere's law to account for Ohmic losses in lossy dielectric media such as wet soil and clay.

## Objective Function

The paper uses a standard least-squares waveform objective:

```text
J(epsilon, sigma) = 0.5 * sum_{r,t} [E_cal(x_r, t; epsilon, sigma) - E_obs(x_r, t)]^2
```

where:

- `E_cal` is simulated electric wavefield data,
- `E_obs` is observed electric wavefield data,
- `x_r` is receiver location,
- `t` is time.

This is a direct waveform-fitting FWI objective, not hyperbola fitting and not template matching.

## Adjoint Equations and Gradients

The paper derives adjoint equations by introducing Lagrange multipliers for electric and magnetic fields.

Adjoint termination condition:

```text
lambda_E(T) = 0
lambda_H(T) = 0
```

The adjoint field is backpropagated from final time to initial time, driven by the waveform residual.

The model gradients are:

```text
dJ/dsigma(x) = integral lambda_E(x,t) dot E(x,t) dt
```

```text
dJ/depsilon(x) = integral lambda_E(x,t) dot dE(x,t)/dt dt
```

Interpretation:

- conductivity gradient is a cross-correlation of adjoint electric field and forward electric field,
- permittivity gradient is a cross-correlation of adjoint electric field and the time derivative of forward electric field.

This is the important adjoint-FWI content for our purposes.

## Optimizer

The paper uses Adam for model updates. Separate learning rates can be assigned to `epsilon_r` and `sigma` through PyTorch parameter groups.

The paper's example code pattern:

```text
epsilon.requires_grad_()
sigma.requires_grad_()
optimizer = torch.optim.Adam([
    {"params": epsilon, "lr": ...},
    {"params": sigma, "lr": ...}
])
loss = MSE(predicted_data, observed_data)
loss.backward()
optimizer.step()
```

They also explicitly zero gradients near the source region to suppress source artifacts.

## CUDA/PyTorch Design

The implementation is built around custom CUDA kernels embedded in a PyTorch `torch.autograd.Function`.

The visual workflow in Figure 3 shows:

- initial model on GPU,
- forward CUDA kernels,
- saved forward fields,
- receiver output,
- loss function,
- backward CUDA kernels,
- adjoint source,
- gradient calculation,
- PyTorch optimizer,
- predicted/inverted model.

The implementation design separates:

- low-level CUDA kernels for fast FDTD updates,
- PyTorch for loss functions, automatic differentiation interface, optimizers, and configuration.

The interface to CUDA is described as using `ctypes`.

## Algorithm Flow

Forward modeling algorithm:

1. Save receiver data.
2. Update magnetic wavefield.
3. Update magnetic PML.
4. Update electric wavefield.
5. Update electric PML.
6. Inject the source function.
7. Save wavefield.

Backward modeling algorithm:

1. Inject adjoint source function.
2. Update electric wavefield.
3. Update electric PML.
4. Update magnetic wavefield.
5. Update magnetic PML.
6. Calculate gradients for relative permittivity and conductivity.

The paper notes that forward wavefields must be available to compute gradients, so memory management and GPU storage are key practical issues.

## Regularization and Stabilization

The paper uses several optimization strategies:

- total variation regularization,
- staged learning-rate scheduling,
- gradient pruning,
- multiscale inversion.

### Total Variation

TV regularization is used to preserve sharp edges while suppressing oscillatory noise in inverted models.

The regularization term is:

```text
TV(X) = sum_{i,j} sqrt((D_x X)^2 + (D_y X)^2)
```

where `X` can be relative permittivity or conductivity.

The implementation uses auxiliary variables approximating first derivatives in the horizontal and vertical directions, with soft-thresholding to enforce sparsity and preserve edges. The resulting TV gradient is added to the raw `epsilon.grad` and `sigma.grad`.

### Multiscale Inversion

The paper describes frequency continuation: start from low-frequency data, then progressively include higher frequencies. Purpose:

- reduce local-minimum risk,
- suppress high-frequency noise early,
- stabilize gradient-based optimization,
- recover large-scale structures before fine-scale features.

### Staged Learning Rate

Learning rates are reduced at predefined stages. The idea is to allow large early updates, then smaller late updates to reduce oscillation around a local minimum.

## Figure-Level Notes From Visual Reading

### Figure 1: Basic GPR FWI loop

The figure shows the standard FWI loop:

observed data and current model produce simulated data, residual drives adjoint-state gradient, the relative permittivity/conductivity model is updated, and the process continues until termination.

### Figure 2: CUDA thread/cell structure

The diagram shows the GPU hierarchy: grid, blocks, and threads. The point is that each CUDA thread updates local field values over parts of the computational grid.

### Figure 3: Proposed CUDA/PyTorch workflow

This is the implementation centerpiece. The figure clearly separates forward and backward kernels inside a PyTorch autograd wrapper. Forward saves receiver data and fields; backward injects adjoint source and computes `epsilon`/`sigma` gradients. The optimizer is external PyTorch.

### Figures 4-5: Synthetic inversion panels

Figure 4 shows a cross-hole dual-parameter experiment with true, initial, and inverted relative permittivity and conductivity. The permittivity result is visually stronger than the conductivity result; conductivity anomalies are captured but amplitudes are less accurate.

Figure 5 shows an Overthrust-style single-parameter relative-permittivity inversion. The comparison against a CPU method is used for both quality and timing.

### Figures 6-9: Real data

Figure 6 shows the controlled pit test site and a MALA 500 MHz GPR. Figure 7 shows raw observed data with strong direct waves. Figure 8 shows direct-wave-removed data after SVD filtering. Figure 9 shows inverted relative permittivity and conductivity maps.

The visual result in Figure 9 is not a rebar-specific interpretation. It is a material/anomaly map: six anomalous bodies in permittivity and four high-conductivity regions.

## Numerical Experiments

### Cross-Hole Dual-Parameter FWI

Purpose: test simultaneous inversion of relative permittivity and conductivity.

Setup:

- 2-D domain.
- Grid spacing: 0.05 m.
- Time step: 1e-10 s.
- Time window: 1e-7 s.
- Model size: 120 by 220 grid points.
- Source: vertical Hertzian dipole.
- Source wavelet: Ricker, 100 MHz.
- Receivers: 200 positions.
- PML thickness: 10 grid points.
- Optimizer: Adam.
- TV regularization used.

Two-stage learning strategy:

- Stage 1, less than 50 epochs: optimize only `epsilon_r`, learning rate 0.2.
- Stage 2: jointly optimize `epsilon_r` and `sigma`, with learning rates 0.1 and 0.0001.

Rationale: reduce dual-parameter crosstalk by first updating permittivity because it controls wave speed more directly.

Reported runtime:

- 150 epochs.
- 1.14 s per epoch.
- Total 195.11 s, less than 4 minutes.

### Surface Overthrust Single-Parameter Test

Purpose: benchmark single-parameter relative permittivity FWI.

Setup:

- Grid spacing: 0.02 m.
- Model size: 220 by 120 grid points.
- Time step: 4e-11 s.
- Time window: 1.4e-8 s.
- Source: vertical Hertzian dipole.
- Source wavelet: Ricker, 400 MHz.
- PML thickness: 10 grid points.
- 200 epochs.
- TV regularization.
- Overall learning rate: 0.02.

Reported comparison:

- GPU method: 2.17 s/epoch, 440.02 s total, SSIM 0.7277.
- CPU-based method: 54.79 s/epoch, 10773.02 s total, SSIM 0.5512.
- Claimed speedup: about 25x per epoch.

### Real Data Dual-Parameter FWI

Field setup:

- Controlled pit with fine sand.
- Buried metal pipes and voids.
- MALA 500 MHz radar.
- Direct waves removed using SVD.

FWI setup:

- 2-D domain.
- Grid spacing: 0.025 m.
- Model size: 80 by 374 grid points.
- Time window: 1.943611e-8 s.
- Time step: 4.871205e-11 s.
- Source: vertical Hertzian dipole.
- Source wavelet: Ricker, 500 MHz.
- Source location: 0.25 m, 0.25 m.
- Receiver location: 0.25 m, 0.425 m.
- Source/receiver step: 0.05 m in the y direction.
- PML thickness: 10 grid points.
- Epochs: 1000.
- TV regularization used.
- Learning rates:
  - `epsilon_r`: 0.1,
  - `sigma`: 0.0001.
- Initial model: uniform background for both relative permittivity and conductivity.

Important ambiguity:

The table lists source/receiver step fields, but the text says one source and one receiver position were actually used. This needs caution before copying the setup directly.

## Main Conclusions

The authors conclude that CUDA/PyTorch hybrid FWI can make dual-parameter GPR FWI much faster while preserving a convenient Python optimization interface.

Scientific inversion conclusions:

- Relative permittivity is recovered more robustly than conductivity.
- Conductivity is recoverable where anomalies are strong, but values may be less accurate.
- Sequential inversion can reduce crosstalk:
  - permittivity first,
  - then joint permittivity/conductivity.
- TV regularization helps suppress noisy artifacts while retaining sharp features.

Engineering conclusions:

- Custom CUDA kernels are much faster than CPU-only implementation.
- Wrapping kernels in PyTorch allows use of Adam, MSE, regularization, and parameter groups.
- GPU memory remains a limitation for larger 2-D/3-D problems.

## Relevance to Our GSSI 51600S Field Data

This paper is useful for a modern adjoint-gradient FWI implementation track, not directly for rebar radius estimation.

Directly transferable:

- 2-D TM FDTD forward/adjoint formulation.
- Least-squares waveform residual.
- Gradient equations for `epsilon_r` and `sigma`.
- Adam optimizer with separate learning rates.
- Sequential update strategy to reduce permittivity/conductivity crosstalk.
- TV regularization.
- Gradient zeroing near the source.
- SVD/direct-wave removal for field data.
- Multiscale inversion.

Not directly addressed:

- rebar geometry inversion,
- PEC cylinder diameter update,
- SBD source-wavelet estimation,
- common-offset rebar-specific ray initialization,
- small-object radius uncertainty.

## How To Test This Paper Separately On Our Field Data

This paper should be tested as a fast adjoint dual-parameter material inversion track:

1. Choose one GSSI B-scan profile.
2. Preprocess:
   - time-zero correction,
   - dewow/DC removal,
   - direct-wave/background removal, possibly SVD,
   - bandpass around antenna bandwidth.
3. Build a 2-D FDTD model with uniform initial `epsilon_r` and `sigma`.
4. Use a Ricker or estimated source wavelet.
5. Run `epsilon_r`-only inversion first.
6. Run joint `epsilon_r` and `sigma` inversion second.
7. Use Adam learning-rate separation similar to the paper.
8. Use TV regularization.
9. Compare:
   - data fit,
   - inverted `epsilon_r`,
   - inverted `sigma`,
   - stability across profiles,
   - whether strong hyperbola locations correspond to material anomalies.

This should not be mixed with Jazayeri's rebar-diameter FWI in the first validation. If later combined, the proper role would be as the fast adjoint engine underneath a rebar geometry parameterization.

## Implementation Priority

For our project, the paper suggests two useful implementation targets:

1. A CPU/PyTorch prototype of 2-D TM FDTD FWI with autograd or explicit adjoint, for small profiles.
2. A CUDA/PyTorch accelerated version if runtimes become limiting.

The state-of-the-art point is not Adam alone. It is the combination of:

- explicit Maxwell/FDTD physics,
- adjoint gradients,
- GPU-resident forward/backward kernels,
- PyTorch optimizer integration,
- TV/multiscale/staged optimization.

## Risks and Limitations For Our Data

- The real-data example is a controlled sand pit, not reinforced concrete.
- The paper's real result maps anomalies but does not estimate object radius.
- Conductivity inversion is less robust than permittivity inversion.
- GPU implementation may be hardware/CUDA-version sensitive.
- Full forward wavefield storage can exceed GPU memory for high-frequency, long-time-window GSSI profiles.
- If our goal is rebar size/location, this paper must be extended with explicit PEC cylinder geometry or a segmentation/level-set model.

## One-Sentence Takeaway

This paper gives a practical modern adjoint-gradient GPR FWI engine for fast dual-parameter `epsilon_r`/`sigma` inversion, but it needs a separate rebar geometry layer before it can estimate rebar diameter from our GSSI concrete B-scans.
