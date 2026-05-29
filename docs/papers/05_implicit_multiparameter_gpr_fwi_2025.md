# Implicit Multiparameter GPR-FWI 2025: Technical Notes

Source PDF:

```text
paper/ggae2025.pdf
```

Paper:

```text
Sun, Liu, Lin, Xing, Liu.
Implicit multiparameter full waveform inversion of multioffset ground
penetrating radar data.
Geophysical Journal International, 2025 issue / accepted 2024.
```

## Why This Paper Matters

This paper is relevant because it attacks two major FWI problems:

```text
strong initial-model dependence,
and unstable multiparameter inversion of permittivity and conductivity.
```

Instead of representing material parameters directly on a grid, the method uses
a neural implicit representation:

```text
spatial coordinate -> neural network -> permittivity and conductivity
```

The key idea for us is not "use deep learning" generically. The useful idea is
that the neural representation has a frequency-principle bias: it tends to learn
smooth/low-frequency structure first and fine detail later. This acts like an
automatic multiscale inversion path.

## Core Method: IFWI

Traditional FWI optimizes model cells:

```text
model grid m -> forward solver -> data misfit
```

Implicit FWI optimizes neural-network weights:

```text
coordinates x,z -> N_theta(x,z) -> model parameters -> forward solver -> data
misfit
```

The paper uses this for GPR multiparameter inversion:

```text
N_theta(x,z) outputs relative permittivity and conductivity.
The forward model is still Maxwell/FDTD.
The loss is waveform mismatch.
Optimization uses deep-learning tooling such as Adam.
```

The authors also discuss an RNN-style differentiable FDTD framing, where
automatic differentiation can provide gradients consistent with adjoint-state
methods.

## Frequency Principle

The paper relies on the frequency principle of neural networks:

```text
early training learns broad/low-frequency model structure,
later training learns fine/high-frequency model structure.
```

This is similar in spirit to multiscale FWI, but it does not require manually
choosing frequency bands. That is the paper's main practical advantage over
classic multiscale schedules.

## Findings

Important findings:

```text
IFWI can reconstruct useful subsurface structure from poorer initial models
than standard FWI.

Multiscale FWI still helps, but still depends on frequency-band choices and
initial model quality.

IFWI can invert permittivity and conductivity simultaneously without the same
manual parameter weighting emphasized in older multiparameter FWI workflows.

Network architecture strongly matters.
```

Architecture notes from the paper:

```text
SIREN/sinusoidal activation can represent fine detail.
The scaling factor omega0 controls frequency/detail sensitivity.
Too small omega0 misses detailed structures.
Too large omega0 can introduce high-frequency noise.
Dropout can reduce high-frequency artifacts in some settings.
Wider networks may help shallow targets but can hurt deeper accuracy.
```

## How This Applies To Rebar Size And Depth

Our current target is low-dimensional:

```text
x position,
z depth,
radius,
possibly material/effective conductivity later.
```

So full IFWI is not the next fastest improvement for the single-rebar pipeline.
However, the paper is important for the next research branch:

```text
multi-rebar geometry,
unknown concrete/background properties,
field data with imperfect starting models,
grid-based permittivity/conductivity reconstruction around targets.
```

The neural implicit representation may also become useful as a smooth shape
prior. Instead of optimizing every grid cell, we could represent a local
material anomaly field with a compact network or analytic shape decoder.

## Safe Adaptation Path

Do not jump directly to differentiable FDTD over full 2D grids. That would
combine too many hard problems at once.

Adapt in stages:

1. Use the frequency-principle lesson to design schedules and regularization.
2. Prototype a small implicit shape model only after objective behavior is
   understood.
3. Keep geometry parameters as the primary inversion variables until radius
   ambiguity is resolved.
4. Later, use neural implicit fields for residual material anomalies around the
   recovered geometry.

## Candidate Prototype For This Project

The smallest useful IFWI-inspired prototype is:

```text
coordinates near the rebar -> small MLP/SIREN -> local permittivity/sigma
background perturbation
geometry parameters remain explicit
loss = current B-scan objective or W2/LS hybrid
regularize MLP output to be smooth and small
```

This would test whether unresolved radius error is actually being absorbed by a
missing material/background correction.

## Risks And Guardrails

```text
Risk: neural representation can fit noise.
Guardrail: hold out sources, use dropout/weight decay/output smoothness, report
generalization across scan positions.

Risk: too many degrees of freedom can hide radius errors.
Guardrail: freeze geometry first, then test local material residuals separately.

Risk: differentiable FDTD may require a major framework rewrite.
Guardrail: begin with derivative-free or finite-difference experiments and only
prototype differentiable solvers after objective evidence supports it.

Risk: architecture tuning can become open-ended.
Guardrail: predefine a small architecture matrix and stopping rules.
```

## Bottom Line

The IFWI paper is a serious later-stage direction, especially for multiparameter
and field-data work. For the current two-week plan, its main role is to guide
regularization, multiscale thinking, and a contained neural implicit feasibility
spike after the PEBDD/W2/frequency-weighted objectives have been tested.
