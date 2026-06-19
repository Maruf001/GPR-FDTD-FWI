# Neural-Network Relevance Triage For Local 2D And Field Work

Date: 2026-06-18

## Scope

This is a local-paper triage of the neural-network PDFs in
`paper/neural_network/`. It does not launch NN training, GPU experiments, field
FWI, or 3D work.

## Papers Reviewed

```text
paper/neural_network/1-s2.0-S0926580519301347-main.pdf
paper/neural_network/1907.09997v1.pdf
paper/neural_network/2207.06527v1.pdf
paper/neural_network/2305.05425v1.pdf
```

## Relevance

Lei et al. 2019, automatic hyperbola detection and fitting:

- Relevant as a possible baseline cue detector for B-scan hyperbola boxes,
  clustering, and peak fitting.
- Not a replacement for the current identifiability/margin framework, because
  it detects/fits candidate hyperbolas rather than quantifying near-best wrong
  branches.

Xiang et al. 2019, AlexNet rebar detection:

- Relevant as a classifier baseline and as prior-art support that dense/uneven
  rebar arrangements are harder because signal interference increases.
- Not immediately useful for the measured field data because the local field
  set has only four profiles and no known-truth rebar labels.

Dai et al. 2022, 2D deep-learning GPR forward solver:

- Relevant as a future synthetic surrogate direction if the project later needs
  many forward solves.
- Not an immediate replacement for FDTD-backed margin claims. A surrogate would
  need a train/test protocol that preserves objective ordering, ambiguity
  margins, close-spacing failures, and seed robustness.

Dai et al. 2023, 3DInvNet:

- Relevant to the separate HPC/3D track.
- Not applicable to the current local GSSI field dataset, which is classified
  as independent 2D line profiles and lacks recoverable crossline/C-scan grid
  metadata.

## Local Decision

Do not start local neural-network training now. The current local contribution
is better framed as controlled acquisition-aware identifiability:

```text
synthetic known-truth resolution and ambiguity margins
field 2D timing/repeatability and spacing QC
explicit cross-domain claim separation
```

If NN work is added later, keep it as one of these bounded roles:

- baseline hyperbola detector for comparison against parametric inversion
- synthetic forward surrogate only after a margin-preservation validation plan
- 3D/C-scan inversion only on the separate HPC/3D branch with appropriate data

The local field data should not be used to train or validate a supervised NN
for rebar resolution, cover depth, radius, field FWI, or 3D inversion.
