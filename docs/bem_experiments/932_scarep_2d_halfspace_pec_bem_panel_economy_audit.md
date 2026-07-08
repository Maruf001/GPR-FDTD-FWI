# BEM Experiment 932: Half-Space PEC BEM Panel Economy Audit

Date: 2026-07-01

## Purpose

Turn the saved half-space PEC adapter result from run `016` into an operating
rule for future BEM sweeps.

Run `016` used 32 BEM panels as the half-space reference. This audit asks
whether the cheaper 16-panel result is accurate enough for preliminary
geometry sweeps while keeping 32 panels as the final comparison reference.

This is a saved-data audit. It does not rerun BEM, run FDTD, use field data,
launch GPU work, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/932_scarep_2d_halfspace_pec_bem_panel_economy_audit
```

## Result

```text
source half-space adapter ready:             true
reference BEM panels:                        32
panel rows audited:                          2
preliminary error gate:                      0.001
recommended preliminary panels:              16
16-panel relative L2 vs 32-panel reference:  0.0004746867074423852
16-panel wall seconds:                       23.183080262038857
16-panel speedup vs 32-panel reference:      3.2873864069744765
16-panel wall-time savings:                  69.58069797093482%
best FDTD relative L2 vs reference BEM:      0.030998297443390457
16-panel error / best FDTD mismatch:         0.015313315458994644
use 16 panels for preliminary sweeps:        true
keep 32 panels for final comparison:         true
project-core FDTD matched:                   false
field transfer ready:                        false
3D validation ready:                         false
gpu priority:                                none
```

## Interpretation

The 16-panel half-space PEC BEM result is a practical preliminary-sweep
setting. Its difference from the 32-panel reference is below the `0.001`
relative-L2 gate and is only about `1.53%` of the best saved FDTD mismatch in
the same half-space benchmark.

The 32-panel solve should remain the final comparison reference because it is
the highest-panel saved result in this half-space branch.

## Decision

Use 16 panels for preliminary half-space PEC BEM sweeps and keep 32 panels for
final comparison checkpoints.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_panel_economy_audit.py
3 passed
```

Figure check:

```text
3111x845, dynamic range=255
```
