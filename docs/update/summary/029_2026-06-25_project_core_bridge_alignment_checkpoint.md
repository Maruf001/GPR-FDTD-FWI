# Project-Core Bridge Alignment Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the continuation after the BEM/field gate integration
checkpoint. It adds one local 2D design pack, two BEM/project-core bridge
diagnostics, and a refreshed presentation evidence pack/storyboard.

No broad GPU queue, field FWI, field 3D/HPC, or neural-network training was
launched.

## Local 2D

Run `138`:

```text
outputs/summary_tables/138_local_2d_new_hypothesis_candidate_pack
docs/experiments/872_local_2d_new_hypothesis_candidate_pack.md
```

Result:

```text
hypothesis candidates:               7
run-next CPU candidates:             4
design-first candidates:             2
field-blocked candidates:            1
CPU-adapter-ready candidates:        2
recommended next hypothesis:         matched_2d_bem_fdtd_dielectric_cylinder_adapter
new local 2D GPU ready:              false
field transfer ready:                false
```

Decision:

```text
Use CPU-scoped hypothesis/adaptor design next. Do not launch a new GPU/FWI
branch from the fixed-radius result.
```

## BEM / Project-Core Bridge

Run `089`:

```text
outputs/bem_experiments/089_project_core_homogeneous_dielectric_cylinder_bridge
docs/bem_experiments/089_project_core_homogeneous_dielectric_cylinder_bridge.md
```

Result:

```text
direct/background relative L2:          0.21186906609266937
scattered time symmetric L2:            1.5075838091082052
residual best scale |beta|:             0.2303344587056435
homogeneous dielectric bridge ready:    false
next half-space rung ready:             false
```

Run `090`:

```text
outputs/bem_experiments/090_project_core_homogeneous_dielectric_bridge_alignment_diagnostic
docs/bem_experiments/090_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.md
```

Result:

```text
alignment candidates:                  9
direct calibrated symmetric L2:         1.5075838091082052
best candidate:                         per_frequency_complex_scale
best candidate symmetric L2:            1.0629842444792676
best simple candidate:                  global_time_shift
best simple symmetric L2:               1.4749859059106778
closed by global/simple alignment:      false
closed by per-frequency scale:          false
homogeneous bridge promotable:          false
half-space rung ready:                  false
```

Interpretation:

```text
The project-core homogeneous dielectric bridge failure is not a trivial sign,
scale, delay, tracewise alignment, or source-spectrum issue. Even
per-frequency complex scaling remains above the 0.75 symmetric-L2 gate.
```

Decision:

```text
Do not advance to half-space project-core promotion. The next BEM/project-core
branch should diagnose grid-aware scattering and finite-domain source/field
conventions.
```

## Presentation Pack

Refreshed outputs:

```text
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
```

Result:

```text
presentation claims:                  39
ready scoped/design/preflight/smoke:  32
blocked claims:                       7
storyboard slides:                    8
gpu/fwi/3d launch ready:              false
```

New presentation claims:

```text
local 2D new hypothesis queue:         ready design, 4 run-next CPU candidates
project-core homogeneous bridge:       blocked, best alignment symmetric L2=1.0629842444792676
```

## Script-Freezing

Major result outputs include frozen script snapshots:

```text
outputs/summary_tables/138_local_2d_new_hypothesis_candidate_pack/scripts/
outputs/bem_experiments/089_project_core_homogeneous_dielectric_cylinder_bridge/scripts/
outputs/bem_experiments/090_project_core_homogeneous_dielectric_bridge_alignment_diagnostic/scripts/
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack/scripts/
outputs/summary_tables/137_bem_field_2d_presentation_storyboard/scripts/
```

The checked snapshot manifests match their frozen files.

## Validation

Focused tests:

```text
tests/test_local_2d_new_hypothesis_candidate_pack.py
tests/test_project_core_homogeneous_dielectric_cylinder_bridge.py
tests/test_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py

10 passed
```

Compile check:

```text
run_local_2d_new_hypothesis_candidate_pack.py: pass
run_project_core_homogeneous_dielectric_cylinder_bridge.py: pass
run_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py: pass
run_bem_field_2d_presentation_evidence_pack.py: pass
run_bem_field_2d_presentation_storyboard.py: pass
```

Figure checks:

```text
run 138: 2637x954, dynamic range=255
run 089: 4 figures, dynamic range=255
run 090: 2 figures, dynamic range=255
pack 135: 2052x954, dynamic range=255
storyboard 137: 2286x851, dynamic range=255
```

Resource and formatting checks:

```text
git diff --check: clean
RAM: 17 GiB used of 119 GiB
GPU: NVIDIA GB10, utilization 6%
```

## Current Next Branch

The marathon remains active. The next defensible branch is a CPU-only
grid-aware scattering diagnostic using run `089`/`090` as the gate evidence,
or a compact report refresh if presentation material needs priority.
