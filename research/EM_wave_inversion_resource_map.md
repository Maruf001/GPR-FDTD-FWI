# EM Wave Inversion Research Notes and Resource Map

Prepared on 2026-03-21

## 1. Problem framing

The task is a compact GPR-style electromagnetic simulation and inversion problem for reinforced concrete.
The core ingredients are:

- forward EM simulation in time domain,
- moving source/receiver acquisition,
- inversion from synthetic radargrams,
- optional GPU acceleration.

The best strategy is to combine:
- classic FDTD references,
- GPR full-waveform inversion literature,
- a small number of modern open-source codebases for validation and acceleration ideas.

## 2. Most relevant scientific papers

### A. Core GPR / FDTD / FWI papers

1. **Ernst, Green, Maurer, Holliger**
   *Full-waveform inversion of crosshole georadar data*
   - Early and important FDTD-based GPR waveform inversion paper.
   - Good reference for the inversion objective and waveform-matching philosophy.

2. **Kuroda, Takeuchi, Kim (2007)**
   *Full-waveform inversion algorithm for interpreting crosshole radar data: A theoretical approach*
   - Useful for explaining theoretical inversion structure and conjugate-gradient style updates.

3. **Meles et al. (2012)**
   *GPR Full-Waveform Sensitivity and Resolution Analysis Using an FDTD Adjoint Method*
   - Strongest directly relevant reference for explaining adjoint-state sensitivity in GPR.
   - Especially useful for interview discussion of gradient efficiency and resolution.

4. **Soydan et al. (2024)**
   *On the utilization of the adjoint method in microwave tomography*
   - More modern discussion of adjoint formulations across imaging scenarios.
   - Helpful for framing the adjoint method in broader EM inversion language.

5. **Wang et al. (2025)**
   *GPR-FWI-Py: Open-source Python Software for Multi-Scale Regularized Full Waveform Inversion in Ground Penetrating Radar Using Random Excitation Sources*
   - Modern open-source software paper directly tied to a public repository.
   - Strong reference if you want to discuss multiscale inversion and regularization.

6. **Liu et al. (2025/2026)**
   *Fast ground penetrating radar dual-parameter full waveform inversion method accelerated by hybrid compilation of CUDA kernel function and PyTorch*
   - Very relevant for bonus GPU/CUDA discussion.
   - Good evidence that hybrid CUDA + Python + autodiff is a contemporary direction in GPR FWI.

### B. Concrete / rebar / parameter sanity papers

7. **Klysz et al. (2008)**
   *Evaluation of dielectric properties of concrete by a numerical model of a ground-penetrating radar coupled antenna*
   - Helpful for concrete permittivity ranges and realistic GPR-concrete coupling discussion.

8. **Wong et al. (2022)**
   *Characterization of Complex Dielectric Permittivity of Concrete by GPR Numerical Simulation and Spectral Analysis*
   - Useful if you want stronger justification for concrete dielectric choices.

9. **Oikonomopoulou et al. (2022)**
   *Reliability and limitations of GPR for identifying objects embedded in concrete*
   - Good qualitative reference for the strengths and limitations of rebar detection in concrete.

## 3. Most relevant open-source repositories

### Primary repos to study

1. **gprMax**
   GitHub: https://github.com/gprMax/gprMax
   Docs: https://docs.gprmax.com/

   Why it matters:
   - Gold-standard open-source GPR simulator.
   - Clear 2D examples using metal cylinders and B-scan generation.
   - Useful for checking parameter scales, waveform choices, and scan setup.
   - Includes GPU support notes for FDTD solver loops.

   How to use it for this task:
   - As validation and reference.
   - Not as the main implementation unless you explicitly decide to wrap or reproduce its setup.

2. **GPR-FWI-Py**
   GitHub: https://github.com/nephilim2016/GPR-FWI-Py

   Why it matters:
   - Modern Python codebase for GPR FWI.
   - Good source for inversion workflow ideas, regularization structure, and experiment organization.

   Caveat:
   - Larger than needed for the interview task.
   - Better mined for ideas than adopted wholesale.

3. **Fast-GPR-FWI**
   GitHub: https://github.com/songc0a/Fast-GPR-FWI
   Paper: https://arxiv.org/abs/2506.20513

   Why it matters:
   - One of the most relevant recent GPU/FWI repos for this problem class.
   - Good reference for what a high-performance path could look like.

   Caveat:
   - Likely too heavy to reproduce fully in interview prep.

### Secondary repos / frameworks

4. **Meep**
   GitHub: https://github.com/NanoComp/meep
   Docs: https://meep.readthedocs.io/

   Why it matters:
   - Excellent general FDTD and adjoint-optimization reference.
   - Good for understanding how adjoint concepts are explained cleanly.

   Caveat:
   - More photonics-oriented than GPR.
   - No native CUDA GPU support in the current documentation.

5. **FDTDX**
   GitHub: https://github.com/ymahlau/fdtdx
   Docs: https://fdtdx.readthedocs.io/

   Why it matters:
   - Modern differentiable FDTD in JAX.
   - Useful if you want a JAX-native GPU path with autodiff.

   Caveat:
   - More photonic-device oriented than reinforced concrete GPR.
   - Best used as design inspiration for software architecture and GPU/autodiff strategy.

6. **PINN4GPR**
   GitHub: https://github.com/ThomasRigoni7/PINN4GPR

   Why it matters:
   - Shows a practical workflow connecting gprMax simulations to surrogate/PINN modeling.
   - Good inspiration for future acceleration ideas.

   Caveat:
   - Not the right first implementation path for this test.

## 4. Datasets and data resources

1. **Open_GPR_Dataset_for_Bridge_Deck**
   GitHub: https://github.com/InfraSmartLab/Open_GPR_Dataset_for_Bridge_Deck

   Why it matters:
   - Simulated rebar-detection dataset generated with gprMax.
   - Relevant if you want examples of realistic radargrams and downstream detection targets.

2. **MO-GPR_data**
   GitHub: https://github.com/Giacomo-Roncoroni/MO-GPR_data

   Why it matters:
   - Synthetic GPR data with multiple profiles and offsets.
   - Potentially useful for testing processing or inversion routines.

3. **Mendeley / Zenodo open GPR datasets**
   - Useful for future benchmarking.
   - Not essential for this assignment, because the task explicitly allows synthetic data generated by your own forward model.

## 5. Hugging Face / deep learning angle

There are some GPR-related papers and datasets discoverable through modern ML portals, but for this particular assignment there is **no strong reason to anchor the solution around Hugging Face models or spaces**.

Best use of modern ML ideas here:
- optional surrogate model after the classical solution works,
- optional learned prior or learned detector after the inversion is working.

Not recommended as the main first-pass solution.

## 6. Best implementation strategy after reviewing the literature

### Recommended architecture

#### Forward module
- `build_model(params)`
- `run_fdtd_shot(model, tx_rx_pos)`
- `run_bscan(model, scan_positions)`

#### Inversion module
- `misfit(params)`
- `simulate_from_params(params)`
- `optimizer_step(...)`
- optional `adjoint_gradient(...)`

#### Visualization module
- ground truth geometry
- initial model
- inverted model
- B-scan image
- waveform comparisons
- field animation

### Recommended inversion parameterization

Start with:
- one or two circular rebars,
- parameter vector `[x_i, y_i, r_i]` for each rebar,
- fixed concrete permittivity,
- fixed conductivity or a single global conductivity.

This balances physical realism and practical solvability.

## 7. Strongest technical story to tell in interview

1. I chose **2D TMz FDTD** because it is explicitly allowed and is the simplest model that still captures the relevant wave physics.
2. I used **circular rebar priors** because the task itself allows prior assumptions and this dramatically reduces ill-posedness.
3. I started with **geometry-only inversion** because it is more stable than simultaneous recovery of conductivity, permittivity, and geometry.
4. I treated **GPU acceleration** as a targeted optimization of the field-update and gradient-accumulation loops rather than trying to prematurely optimize everything.
5. I used external open-source packages mainly as **validation references and design inspiration**, not as a substitute for understanding.

## 8. What to borrow from each external source

### From gprMax
- 2D TMz survey setup
- practical B-scan generation pattern
- reasonable source frequencies and scan geometry
- PML usage expectations

### From Meles / Ernst / Kuroda
- formal inversion objective
- adjoint-state explanation
- sensitivity interpretation

### From GPR-FWI-Py
- inversion workflow organization
- regularization ideas
- multiscale strategy

### From Fast-GPR-FWI
- GPU narrative
- hybrid CUDA + Python structure
- modern high-performance framing

### From FDTDX
- differentiable FDTD architecture ideas
- JAX/JIT/autodiff design inspiration

## 9. Final recommendation

If time is limited, the best fully defensible path is:

- custom CPU 2D TMz FDTD first,
- synthetic rebar B-scan generation,
- constrained geometry inversion,
- clean figures and metrics,
- optional JAX/CuPy/CUDA acceleration for the hotspot loops.

That is the highest signal-to-effort route for this assignment.
