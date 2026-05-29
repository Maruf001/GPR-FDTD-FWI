# Wavefield Reconstruction Inversion 2022: Working Notes

Source PDF:

```text
paper/Wavefield Reconstruction_2022.pdf
```

Paper:

```text
Feng, Ding, Wang, Su, Liu, Cao.
Wavefield Reconstruction Inversion Based on the Multi-Scale Cumulative
Frequency Strategy for Ground-Penetrating Radar Data: Application to Urban
Underground Pipeline.
Remote Sensing, 2022.
```

## Why This Paper Matters For Our Project

Our current single-rebar pipeline estimates a small set of geometry
parameters from time-domain FDTD B-scans. It now locates the bar well, but the
radius can sit in a nearby depth/radius tradeoff basin unless we add a final
grid polish.

This paper attacks the same class of GPR inverse problem from a broader FWI
perspective: underground circular pipeline targets, inaccurate starting models,
multi-parameter inversion, and the tendency of standard FWI to get trapped by
nonlinearity. Its main lesson is not just "use more frequencies"; it is:

```text
Relax the wave equation early, control the frequency content deliberately, and
add higher frequencies cumulatively rather than all at once.
```

## Core Method

The paper uses frequency-domain wavefield reconstruction inversion (WRI).
Traditional FWI enforces the wave equation exactly for every model update. WRI
instead treats the wavefield and model as coupled unknowns and puts the wave
equation into the objective as a penalty term.

In plain terms:

```text
FWI: candidate model must explain data through an exact simulated wavefield.
WRI: candidate model may use a reconstructed wavefield that balances data fit
     against wave-equation consistency.
```

That relaxation expands the search space early in inversion. The goal is to
reduce cycle skipping and reduce dependence on the starting model. As the
penalty weight grows, WRI approaches ordinary FWI behavior.

The paper solves the wavefield subproblem with variable projection:

```text
1. Hold the material model fixed.
2. Solve a least-squares problem for the best reconstructed wavefield.
3. Substitute that wavefield back into a reduced objective over material
   parameters.
4. Optimize the material model with L-BFGS.
```

They invert both relative permittivity and conductivity in the frequency
domain.

## Frequency Strategy

The most directly reusable part is the multi-scale cumulative frequency
strategy.

The paper compares:

```text
S:  simultaneous weighted multi-frequency inversion
B1: cumulative strategy adding 1 frequency per stage
B2: cumulative strategy adding 2 frequencies per stage
B3: cumulative strategy adding 3 frequencies per stage
B4: cumulative strategy adding 4 frequencies per stage
B5: cumulative strategy adding 6 frequencies per stage
```

The cumulative schedules always keep the lower frequencies while adding higher
ones. That means each stage inherits the broad-scale information from earlier
stages and only then adds sharper details.

The paper also weights frequency components to prevent high-frequency data from
dominating the objective. The weighting is stronger for lower frequencies,
using an inverse-frequency-squared style normalization.

Practical interpretation for us:

```text
Do not run a single full-band objective and hope Powell/DE finds radius.
Use a deliberate schedule:
  low/limited band for stable location,
  cumulative wider band for radius/detail,
  final fine/local polish only after the model is in the right basin.
```

## Numerical Findings

The paper tested two synthetic pipeline cases and one physical/field-style
pipeline case.

Important observations:

- Cumulative frequency strategies were more stable and accurate than using all
  selected frequencies simultaneously.
- Adding fewer new frequencies per stage improved accuracy but required more
  PDE solves.
- Adding more frequencies per stage reduced runtime but increased
  reconstruction error.
- Relative permittivity was generally reconstructed better than conductivity.
- Deep targets and targets near limited-aperture boundaries were harder.
- Conductivity reconstructions were more artifact-prone.
- Field data still showed artifacts, but the method recovered plausible
  pipeline locations and material contrasts.

Reported high-level comparison:

```text
Synthetic case 1:
  cumulative strategies improved reconstruction errors over simultaneous
  strategy by roughly 7-11% for permittivity and 7-15% for conductivity.

Synthetic case 2:
  cumulative strategies improved reconstruction errors over simultaneous
  strategy by roughly 20-40% for permittivity and 17-24% for conductivity.
```

The paper's own discussion says the best practical choice is a compromise:
increase frequency content gradually, but not necessarily one frequency at a
time if runtime is important.

## Limitations The Authors Admit

The paper identifies several unresolved issues that matter to us:

- WRI can still produce numerical oscillations and artifacts.
- Regularization is still needed for clean models.
- Deep-media reconstruction can benefit from depth weighting.
- Real materials can be frequency-dependent, while the paper assumes constant
  material parameters.
- Field-data wavelet estimation is difficult.
- More efficient optimization remains important.

These are useful warnings. WRI is not a magic replacement for the current
single-rebar pipeline. It is a principled way to reduce nonlinearity, but it
adds complexity.

## Relevance To Our Current Codebase

Current relevant code:

```text
inversion/single_rebar_pipeline.py
run_single_rebar_inversion.py
docs/experiments/07_multiscale_frequency.md
docs/experiments/12_radius_refinement_worklog.md
docs/experiments/14_grid_polish_speed_worklog.md
```

The current single-rebar pipeline already supports multiple center
frequencies, but it evaluates them as one objective. The WRI paper suggests we
should add a cumulative frequency schedule rather than only a simultaneous
multi-frequency objective.

The paper's full WRI formulation is frequency-domain and solves a Helmholtz
system. Our simulator is time-domain FDTD. A faithful WRI implementation would
therefore be a major new solver path. That should not be the immediate next
step.

## Practical Ideas To Reuse First

### 1. Cumulative Frequency Schedules

Add an experiment runner that executes:

```text
stage 1: low or narrow frequency set
stage 2: stage 1 frequencies + next higher frequency
stage 3: stage 2 frequencies + next higher frequency
...
final: full target frequency set + local polish
```

For our current synthetic target, candidate frequencies could be:

```text
0.8, 1.0, 1.2, 1.5 GHz
```

or, if runtime is too high:

```text
1.0, 1.2, 1.5 GHz
```

The result of each stage should seed the next stage.

### 2. Frequency Weighting

When multiple frequencies are evaluated together, avoid equal weighting if
high-frequency residuals dominate. Track per-frequency residual contribution
and add a weighting option that approximately equalizes or intentionally
upweights low frequencies during early stages.

### 3. Use Frequency Stages Before Radius Polish

The current radius issue is a depth/radius coupling. Cumulative bandwidth may
reduce the chance that Powell lands in the high-radius basin before polish.
The right experiment is:

```text
2 mm global seed
-> cumulative frequency Powell at 1 mm
-> coarse grid polish
-> compare radius/top-candidate margins against current single-frequency runs
```

### 4. Defer Full WRI

A faithful WRI implementation would require either:

```text
frequency-domain forward operator + reconstructed wavefield solve
```

or a carefully designed time-domain analog. That is a larger research branch.
The paper-backed low-risk step is cumulative frequency scheduling first.

## Concrete Next Experiment

Recommended first implementation:

```text
run_single_rebar_frequency_schedule.py
```

Features:

- accepts comma-separated stages, such as `1.0|1.0,1.2|1.0,1.2,1.5`
- runs `SingleRebarInversionEngine` stage by stage
- carries recovered parameters forward as the next initial guess
- records per-stage misfit, recovered geometry, top polish candidates, and
  runtime
- optionally runs `--grid-polish-preset coarse` only at the final stage

Success criteria:

```text
1. Powell radius bias is reduced before grid polish, or
2. grid polish top-candidate margin for radius=6.0 mm increases, or
3. same accuracy is achieved with fewer global evaluations.
```

If none of these happen, the cumulative schedule is not useful for the current
simple single-rebar problem, but it may still be useful when moving to multiple
rebars or field-style data.

