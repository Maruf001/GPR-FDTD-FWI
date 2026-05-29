# Five Papers: One Section Each, Tuned to Our Project

Each section is intentionally short and presentation-ready. It pairs the
paper's core idea with the specific way we adapted (or rejected) it for the
single-rebar radius problem.

PDFs:

```text
paper/Wavefield Reconstruction_2022.pdf
paper/FWI_improvement_by_progressively expanded bandwidths of the data.pdf
paper/FWI_Optimal_Transport_2025.pdf
paper/FWI_twoParam_GPR_Quadratic-Wasserstein-Distance_2024.pdf
paper/ggae2025.pdf
```

Repo-side summaries: `docs/papers/01..05_*.md`.

---

## 1. Wavefield Reconstruction Inversion (Feng et al., Remote Sensing 2022)

**Core idea.** Standard FWI enforces the wave equation exactly each iteration,
which makes the objective highly nonlinear and easy to trap. WRI relaxes the
wave equation into the objective as a penalty term, so the wavefield and the
model are co-updated. As the penalty grows, WRI approaches ordinary FWI. The
paper also runs a **multi-scale cumulative frequency strategy**: start with a
low frequency, then add higher frequencies one (or a few) at a time, carrying
previous frequencies forward each stage. It also uses a per-frequency weighting
to prevent high frequencies from dominating.

**What we adopted.** The cumulative-frequency *idea*, not the WRI solver. We
added per-frequency objective contributions, then a frequency-weighting CLI,
and ran weighted vs unweighted matrices to see how frequency choice affects
the actual radius margin.

**What we rejected.** Full WRI itself. Our solver is time-domain FDTD; a
faithful WRI would need a frequency-domain Helmholtz path, complex sparse
solves, and a new adjoint. Documented as too large for this stage.

**Useful single line for slides.** *Borrow the cumulative-frequency
philosophy; defer the WRI solver.*

---

## 2. Progressive Expanded Bandwidth FWI / PEBDD (Zhou et al., NSG 2021)

**Core idea.** Don't fit full-band data immediately. Apply the same bandpass
filter to both observed and modeled data, start with a low-band objective,
then expand the high cut in small stages. Each stage's recovered model seeds
the next. After the staged build-up, run final full-band FWI. Repeatedly
estimate the effective source wavelet by deconvolution along the way.

**What we adopted.** A trace-filter inside the objective with matched
filtering of `d_obs` and `d_syn`, then a multi-stage bandwidth runner. We
also built a spectrum-design tool to choose band edges from actual residual
spectra rather than by guessing.

**What we learned.** A guessed 0.2–0.8 GHz low band contains almost none of
the radius-discriminating residual energy. Spectrum-driven design relocated
the useful bands to 0.35–2.5 GHz, but a faithful staged Powell still left the
high-radius bias, which only the grid polish removed. **PEBDD is a useful
seed-builder but does not solve radius on its own.**

**Useful single line for slides.** *Bandwidth scheduling improves seeds;
radius selection still needs polish.*

---

## 3. Optimal-Transport / Least-Squares FWI (Hunziker et al., JAG 2025)

**Core idea.** Use an OT-based distance early because its objective basin is
broader and less cycle-skipping-prone. Once enough modeled traces are within
half a period of the observed traces, switch back to least-squares for
sharpness. The switch is governed by a relative cross-correlation criterion
RCCC = |trace shift| / dominant period, with `NRCCC` as the fraction of traces
having RCCC < 0.5; switch when `NRCCC > Cs ≈ 0.7`.

**What we adopted.** Trace-shift diagnostics. We added an RCCC / NRCCC
computation, saved it in every summary, and ran it post-hoc against earlier
high-radius candidates.

**What we learned.** Across the high-radius Powell solution and every polish
top candidate (exact, 5%, and 10% noise), `NRCCC = 1.0`. The single-rebar
radius problem is not a trace-shift problem. OT-driven basin correction
won't help here, although it would still be worth keeping as a diagnostic
for poor initial models or field-data scenarios.

**Useful single line for slides.** *Trace-shift criterion confirms the
radius issue is amplitude/detail, not cycle skipping.*

---

## 4. Quadratic Wasserstein GPR FWI (Lu et al., Remote Sensing 2024)

**Core idea.** Replace L2 with quadratic Wasserstein (W2). To make signed
oscillatory traces usable with optimal transport, apply Softplus
normalization. Compute W2 via Sinkhorn iterations with entropy regularization.
The authors report improved convexity to shifts, better noise robustness, and
better conductivity recovery.

**What we adopted.** A standalone Softplus / Sinkhorn W2 trace distance with
unit tests. We first replicated the paper's convexity claim on shifted Ricker
traces (it holds — clearly smoother than L2). Then we ran the same W2 on the
actual rebar radius landscape.

**What we learned.** On the rebar landscape, W2 collapses the radius margin
by roughly four orders of magnitude (1.06e-7 vs 1.04e-3 for L2). The
Softplus normalization removes the amplitude content that radius depends on.
We *reject* W2 as the final radius objective for this specific problem.

**Useful single line for slides.** *W2 fixes the shift problem we did not
have; it would damage the amplitude problem we do have.*

---

## 5. Implicit Multiparameter GPR FWI / IFWI (Sun et al., GJI 2025)

**Core idea.** Don't store material parameters on a grid; let a neural
network map `(x, z) → (εr, σ)`. The neural "frequency principle" means the
network learns smooth structure first and detail later, which acts like an
automatic multi-scale prior. The paper handles permittivity and conductivity
together without manual parameter weighting.

**What we adopted.** Nothing yet. We wrote a feasibility note instead. The
single-rebar geometry parameter vector is tiny `[x, z, r]` and the radius
issue we are seeing is already explained by source-wavelet handling and
amplitude weighting. Adding a free neural residual field at this stage would
risk absorbing radius errors into a flexible "background correction" and
make the radius estimate less meaningful, not more.

**What we plan.** Reserved as a later-stage option for multi-rebar work or
field data when explicit nuisance parameters become insufficient. Any IFWI
prototype here would need to keep geometry explicit and hold out scan
positions to validate that the implicit field doesn't soak up radius bias.

**Useful single line for slides.** *Deferred; reserved for multi-parameter
field data after the source-profiled pipeline is mature.*

---

## Summary table for the deck

| Paper | What we kept | What we rejected/deferred | Direct slide artifact |
| --- | --- | --- | --- |
| WRI 2022 | per-frequency / weighted LS objective | full WRI solver | freq-weight margin plot (exp 046, 047, 049) |
| PEBDD 2021 | objective bandpass + spectrum-driven schedule | full-band Powell as a radius selector | spectrum design (exp 043) + staged result (exp 045) |
| OT-LS 2025 | RCCC / NRCCC trace-shift diagnostic | OT inside the optimizer (not needed here) | trace-shift conclusion text (exp 024–026) |
| W2 GPR 2024 | Softplus/Sinkhorn W2 module + landscape gate | W2 as a radius objective | W2 convexity (exp 048) + landscape margin (exp 050) |
| IFWI 2025 | feasibility note | full neural field (this stage) | conceptual slide only |
