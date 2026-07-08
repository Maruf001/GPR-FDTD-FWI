My honest conclusion: **yes, there is a real publishable path here — but the paper should not be framed as “we used a newer deep-learning architecture for GPR.”** That would be weak, because the GPR literature has already moved past plain CNN/U-Net into attention U-Nets, GAN inversion, transformer/recurrent “wave-to-permittivity” models, implicit neural FWI, CNN-filtered FWI, CUDA/PyTorch accelerated FWI, and even GPR-specific neural-operator work. The stronger gap is:

> **label-scarce / label-free field GPR rebar inversion using a calibrated physics-aware neural operator or implicit-neural FWI, with explicit uncertainty over non-unique rebar geometry and concrete permittivity.**

That is much more defensible than “FNO for GPR” by itself.

## 1. Where the field already is

There are roughly four literature buckets.

### A. Rebar detection/localization from B-scans

This bucket is mostly object detection or hyperbola localization. A strong example is Liu et al. 2020: they trained an SSD detector on **3,992 real GPR images containing 13,026 rebar targets**, then used migration/binarization to estimate horizontal position and depth; they report 90.9% detection accuracy, depth error under 1.5 mm in a lab experiment, and lateral position error under 0.7 cm. ([Illinois Experts][1])

This is important because it means a paper that only does “detect hyperbolas with YOLO/Faster R-CNN/SSD” is probably not enough unless you add something genuinely new: close-spacing ambiguity, diameter/radius estimation, unlabeled field adaptation, uncertainty, or physics consistency.

### B. B-scan/C-scan to permittivity-map inversion

This is where GPRInvNet, DMRF-UNet, PICGAN, GPRTransNet, and 3DInvNet live. GPRInvNet maps B-scan data to permittivity maps using a trace-to-trace encoder/decoder, explicitly addressing the spatial-alignment problem between time-series radar traces and spatial permittivity maps. ([arXiv][2]) DMRF-UNet then adds a two-stage approach for heterogeneous soil: first clutter/noise suppression, then inverse mapping to permittivity. ([arXiv][3]) PICGAN uses a conditional GAN for B-scan-to-permittivity inversion. ([ScienceDirect][4]) GPRTransNet, from 2025, explicitly argues that many GPR inversion methods are CNN-limited and proposes a “wave-to-permittivity” translation architecture with recurrent/attention mechanisms. ([ScienceDirect][5])

3DInvNet is a major reference because it goes from **GPR C-scans to 3D permittivity maps** using a 3D CNN denoiser plus a 3D U-shaped encoder-decoder with multi-scale feature aggregation; their repo also provides code and simulated/real measured datasets. ([arXiv][6]) But note the key mismatch: **3DInvNet is C-scan → 3D permittivity map**, while your current field data sound like mostly unlabeled B-scans with unknown antenna model and unknown material parameters. So the 83 GB dataset is useful, but probably as pretraining/benchmark data, not as a direct plug-and-play supervised solution for your rebar field inversion.

### C. Physics + deep learning / FWI hybrids

This is the most relevant bucket for your project. The 2019 reinforced concrete FWI paper is still very important because it directly targets rebar mapping and diameter estimation: it uses surface-coupled common-offset GPR B-scans, sparse blind deconvolution to estimate the source wavelet, ray-based analysis to initialize geometry, and then FWI to improve diameter estimates. ([ScienceDirect][7])

Then the field moves toward hybrid approaches. PDD-FWI combines normalized range migration with a DNN reconstruction network to recover target location, shape, and permittivity, with attention-gated U-Net-style components and simulated plus real data. ([Beijing Institute of Technology][8]) The 2025 implicit multiparameter FWI paper is also highly relevant: it represents subsurface parameters as an implicit continuous neural function, exploiting the deep-learning “frequency principle” so the inversion tends to recover large-scale/low-frequency structure before fine details, reducing dependence on the initial model.  The adaptive CNN-filtered FWI paper embeds a CNN directly inside the FWI loop to filter model parameters and gradients, while keeping the whole process differentiable. ([arXiv][9]) The fast GPR dual-parameter FWI paper uses custom CUDA kernels integrated with PyTorch autodiff to invert permittivity and conductivity more efficiently. ([arXiv][10])

So yes: Codex combining IFWI-like representation, PyTorch autodiff, CUDA acceleration, AdamW, and FWI losses is not crazy. That direction is actually aligned with where the field is moving.

### D. Neural operators / FNO / calibration

This is the most interesting “modern ML” angle, but also the easiest to overclaim.

There is already GPR-specific operator-learning work. The “Deep Calibration and Operator Learning for GPR Imaging” paper extends Born FNO to realistic GPR acquisition and explicitly says the major bottleneck is the mismatch between idealized forward models and real antenna systems; real GPR systems have antenna-ground multiple reflections, frequency-dependent antenna behavior, and a 3D measurement system that people often reduce to a 2D computational domain.  That paper combines BFNO with a learned calibration network for a realistic GSSI-400 MHz receiver and shows recovery of permittivity distributions on simulated data with robustness to noise. 

This is extremely relevant to you because your real problem is not just “can an FNO learn Maxwell/FDTD?” The real problem is **unknown antenna, unknown source wavelet, unknown time-zero, unknown concrete permittivity, unknown coupling, and no labels**. A plain FNO will not magically solve that. A **calibrated neural operator + physics-constrained inverse loop** is much more plausible.

## 2. Brutal feasibility check

### What is realistically identifiable?

From a **single 2D B-scan**, you can often estimate:

**x position**, approximate **depth z**, and sometimes an effective velocity/permittivity if the hyperbola is clear. Radius/diameter is harder but possible with waveform/amplitude/FWI constraints. The 2019 rebar FWI paper matters because traditional GPR processing struggles with diameter, and FWI improves that by using the full waveform rather than just ray geometry. ([ScienceDirect][7])

But from one B-scan, you generally **cannot reliably infer the rebar length along y** unless the scan geometry crosses rebar ends, uses multiple parallel survey lines, or forms a C-scan/3D volume. A long rebar perpendicular to the scan line often appears like a 2D cylindrical scatterer. The along-axis extent is invisible unless your acquisition samples that dimension. So for your paper, do not promise x, y, z, radius, length, and permittivity from ordinary single-line B-scans unless you actually have multi-line/C-scan coverage.

### What will reviewers attack?

They will attack synthetic-to-real generalization. This is already recognized in GPR inversion: 2025 work applies unsupervised domain adaptation to deep-learning-based GPR inversion using a domain classifier inside the inversion network. ([IEEE Xplore][11]) There are also semi-supervised GPR target recognition methods, which shows the community already knows labels are scarce and is moving beyond fully supervised training. ([PMC][12])

They will also attack non-uniqueness: rebar radius, permittivity, conductivity, source wavelet, coupling, and antenna response can trade off against each other. A model that gives one clean answer without uncertainty may look impressive but not trustworthy.

They will not be impressed by “we used AdamW” or “we used JAX.” AdamW/PyTorch/JAX are implementation choices unless you show they enable a new inversion formulation, a major runtime improvement, or a stability/generalization improvement. PyTorch already has strong neural-operator support through the NeuralOperator library, which includes FNO and related models; JAX now has emerging neural-operator tooling such as jNO, but switching frameworks is not a scientific contribution by itself. ([Neural Operator][13])

## 3. The strongest publishable gap

The best paper idea is not:

> “FNO for GPR object detection.”

The stronger version is:

> **A physics-calibrated neural-operator/FWI framework for label-scarce rebar inversion from field GPR B-scans, jointly estimating rebar geometry and effective concrete permittivity while reporting ambiguity/uncertainty.**

That gap is defensible because existing deep GPR papers often do direct supervised B-scan/C-scan → permittivity mapping, while FWI papers often require careful initialization, source/antenna assumptions, or expensive forward solves. IFWI reduces initial-model dependence, CUDA/PyTorch FWI reduces runtime, BFNO-style operator learning reduces repeated FDTD cost, and domain adaptation addresses the synthetic-to-real problem — but combining these into a practical rebar-specific, label-scarce field inversion workflow is still a meaningful research direction. 

## 4. What architecture I would actually build

I would not start with a giant black-box detector. I would build a hybrid system:

**Stage 1: self-supervised / weakly supervised B-scan representation.**
Use your unlabeled field B-scans for background removal, denoising, time-zero stabilization, trace normalization, and contrastive/self-supervised feature learning. This is where your real field data are valuable even without labels.

**Stage 2: synthetic physics dataset.**
Generate gprMax/FDTD simulations for concrete slabs with variable rebar depth, radius, spacing, permittivity, conductivity, scan spacing, source wavelet, time-zero, noise, and antenna-like filtering. Include close rebars and ambiguous cases, because your existing project’s close-spacing ambiguity is actually a strength.

**Stage 3: learned forward surrogate.**
Train a neural operator or U-Net/FNO-style forward model:

[
(\epsilon(x,z), \sigma(x,z), \text{source/antenna params}) \rightarrow B(x,t)
]

This is where FNO/U-NO/BFNO makes sense. FNO is more naturally a **forward operator surrogate** than a pure detector. The original FNO idea is to learn mappings between function spaces for families of PDEs, rather than solving one discretized case at a time. ([arXiv][14])

**Stage 4: inverse loop over physical parameters.**
Instead of asking the network to directly hallucinate geometry, optimize a compact parameter vector:

[
\theta = {x_i, z_i, r_i, \epsilon_\text{concrete}, \sigma_\text{concrete}, a_\text{scale}, t_0, \text{wavelet/filter params}}
]

Then compare predicted and observed B-scans using a robust loss: waveform loss, envelope loss, low-frequency loss, time-shift-tolerant loss, and maybe a hyperbola-apex consistency loss.

**Stage 5: uncertainty / multiple hypotheses.**
Return top-k candidate geometries, not just one answer. For close rebars, this is scientifically honest and likely publishable. A “single best answer” can be wrong; a ranked ambiguity map is more useful.

## 5. What role should 3DInvNet data play?

Use it, but carefully.

3DInvNet’s dataset and code are valuable because they give you a real benchmark for learned inversion and 3D permittivity reconstruction. The repo explicitly provides simulated and real measured datasets plus training commands for the denoiser and inverter. ([GitHub][15]) But if your field data are 2D B-scans from a different antenna/frequency/material setting, then training directly on 3DInvNet and applying to your field scans is likely to fail or give misleading confidence.

The better use is:

1. **Benchmark:** reproduce 3DInvNet or a subset to prove your pipeline works on a known dataset.
2. **Pretraining:** learn radar feature representations or denoising priors.
3. **Architecture baseline:** compare your FNO/operator/implicit-FWI method against 3DInvNet-like 3D CNN/U-Net baselines where the input/output format matches.
4. **Transfer test:** show how badly direct transfer fails, then show your calibration/domain-adaptation method improves it.

That last point could become part of the paper: **“Why direct supervised inversion fails under domain shift, and how physics-calibrated neural operators/FWI recover useful field inversions.”**

## 6. What not to do

Do not make the paper only about “modern architecture.” GPR reviewers will ask: where is the physics? ML reviewers will ask: where is the novelty beyond applying FNO/Transformer to a niche dataset?

Do not claim full 3D rebar length from single B-scans. That is an identifiability trap.

Do not use field B-scan residual alone as proof of correctness. A wrong geometry can sometimes match a B-scan because permittivity, radius, wavelet, and depth can compensate for each other.

Do not spend months building a huge FNO before proving a small synthetic-to-real inverse loop works.

## 7. A practical paper plan

I would aim for this sequence:

**Paper 1 — strongest and fastest:**
“Implicit physics-constrained FWI for rebar geometry and concrete permittivity estimation from field GPR B-scans.”
Use IFWI/neural parameterization, CUDA/PyTorch acceleration, AdamW/L-BFGS comparison, source-wavelet calibration, uncertainty/top-k ambiguity, and comparison to the 2019 rebar FWI baseline.

**Paper 2 — deeper ML contribution:**
“Calibrated neural-operator surrogate for accelerated GPR full-waveform inversion under synthetic-to-real domain shift.”
Train FNO/BFNO/U-NO as the fast forward model, then invert through it. Include field adaptation and runtime comparisons against gprMax/FDTD and CUDA/PyTorch FWI.

**Paper 3 — application paper:**
“Automated rebar localization and diameter estimation in reinforced concrete using hybrid detection, migration, and physics-constrained inversion.”
This can combine YOLO/SSD-style detection with FWI refinement, but the novelty must be diameter/permittivity/uncertainty, not just detection.

## 8. My recommendation

Stay with your current optimizer/FWI direction, but reframe it as a **hybrid inverse problem**, not merely an optimizer experiment. Then add neural-operator work only after you have a stable baseline.

The strongest immediate implementation is:

[
\text{Detector / hyperbola picker} \rightarrow \text{geometry initialization} \rightarrow \text{implicit-neural FWI} \rightarrow \text{top-k candidate ranking + uncertainty}
]

Then later replace the expensive forward solver with an FNO/BFNO surrogate:

[
\text{geometry/permittivity} \rightarrow \text{neural forward B-scan} \rightarrow \text{inverse optimization}
]

That gives you a clean story: **classical FWI is accurate but slow and initialization-sensitive; direct deep inversion is fast but domain-shift-sensitive; your method is calibrated, physics-constrained, accelerated, and honest about ambiguity.**

That is a real gap. But “use FNO because it is 2026” is not enough. The publishable contribution is **not the architecture name**. It is the formulation: label-scarce field GPR inversion with unknown antenna/material parameters, physics consistency, fast differentiable forward modeling, and uncertainty-aware rebar geometry recovery.

[1]: https://experts.illinois.edu/en/publications/detection-and-localization-of-rebar-in-concrete-by-deep-learning-/ "
        Detection and localization of rebar in concrete by deep learning using ground penetrating radar
      \-  Illinois Experts"
[2]: https://arxiv.org/abs/1912.05759?utm_source=chatgpt.com "GPRInvNet: Deep Learning-Based Ground Penetrating Radar Data Inversion for Tunnel Lining"
[3]: https://arxiv.org/abs/2205.07567?utm_source=chatgpt.com "DMRF-UNet: A Two-Stage Deep Learning Scheme for GPR Data Inversion under Heterogeneous Soil Conditions"
[4]: https://www.sciencedirect.com/science/article/abs/pii/S0926985123002422?utm_source=chatgpt.com "PICGAN: Conditional adversarial neural network-based ..."
[5]: https://www.sciencedirect.com/science/article/abs/pii/S0886779825001956?utm_source=chatgpt.com "GPRTransNet: A deep learning–based ground-penetrating ..."
[6]: https://arxiv.org/abs/2305.05425?utm_source=chatgpt.com "3DInvNet: A Deep Learning-Based 3D Ground-Penetrating Radar Data Inversion"
[7]: https://www.sciencedirect.com/science/article/abs/pii/S0950061819325449?utm_source=chatgpt.com "Reinforced concrete mapping using full-waveform ..."
[8]: https://pure.bit.edu.cn/en/publications/joint-physics-and-data-driven-full-waveform-inversion-for-undergr/ "
        Joint Physics and Data Driven Full-Waveform Inversion for Underground Dielectric Targets Imaging
      \-  Beijing Institute of Technology"
[9]: https://arxiv.org/html/2410.08568v1?utm_source=chatgpt.com "GPR Full-Waveform Inversion through Adaptive Filtering of Model ..."
[10]: https://arxiv.org/abs/2506.20513?utm_source=chatgpt.com "Fast ground penetrating radar dual-parameter full waveform inversion method accelerated by hybrid compilation of CUDA kernel function and PyTorch"
[11]: https://ieeexplore.ieee.org/iel8/36/10807682/10994693.pdf?utm_source=chatgpt.com "Enhancing Deep Learning-Based GPR Data Inversion With ..."
[12]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12116026/?utm_source=chatgpt.com "A Semi-Supervised Attention-Temporal Ensembling Method ..."
[13]: https://neuraloperator.github.io/?utm_source=chatgpt.com "Neural Operators in PyTorch — neuraloperator 2.0.0 ..."
[14]: https://arxiv.org/abs/2010.08895?utm_source=chatgpt.com "Fourier Neural Operator for Parametric Partial Differential Equations"
[15]: https://github.com/qiqi-dai/3dinvnet "GitHub - Qiqi-Dai/3DInvNet · GitHub"
