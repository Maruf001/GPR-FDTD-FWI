# Run089 Grid-Aware Scattering Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the next BEM/project-core bridge result after the
alignment replay. It adds a run-089-geometry grid-aware discrete Born replay,
refreshes the presentation pack, and preserves the current no-GPU/no-field-FWI
guardrails.

No broad GPU queue, field FWI, field 3D/HPC, or neural-network training was
launched.

## BEM Run 091

Output:

```text
outputs/bem_experiments/091_project_core_run089_geometry_discrete_born_replay
```

Tracker:

```text
docs/bem_experiments/091_project_core_run089_geometry_discrete_born_replay.md
```

Result:

```text
scan positions:                         7
cylinder epsr:                          4.0
cylinder center:                        x=0.25 m, z=0.15 m
cylinder radius:                        0.03 m
target cell count:                      753
selected frequency bins:                17
legacy analytic-cylinder time L2:       1.5075838091082052
best Born variant:                      receiver_conjugate_div_source
best Born time symmetric L2:            0.5800814918790829
best Born spectral symmetric L2:        0.5800814918790828
discrete Born scattering ready:         true
GPU required:                           false
```

Interpretation:

```text
The run 089 geometry is recoverable when target scattering is represented on
the project grid. The continuous analytic-cylinder bridge and simple alignment
replay failed, but the project-grid-aware target-cell operator passes the 0.75
gate.
```

Decision:

```text
The positive path is not more direct-wave calibration. It is a reusable
grid-aware BEM/project-core scattering adapter.
```

## Presentation Refresh

Refreshed outputs:

```text
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack
outputs/summary_tables/137_bem_field_2d_presentation_storyboard
```

Result:

```text
presentation claims:                  40
ready scoped/design/preflight/smoke:  33
blocked claims:                       7
storyboard slides:                    8
gpu/fwi/3d launch ready:              false
```

New/updated project-core claims:

```text
project-core homogeneous dielectric bridge:
  blocked, best alignment symmetric L2=1.0629842444792676

project-core grid-aware scattering replay:
  ready scoped, run-089 geometry best Born L2=0.5800814918790829
```

## Script-Freezing

The new result outputs include frozen script snapshots:

```text
outputs/bem_experiments/091_project_core_run089_geometry_discrete_born_replay/scripts/
outputs/summary_tables/135_bem_field_2d_presentation_evidence_pack/scripts/
outputs/summary_tables/137_bem_field_2d_presentation_storyboard/scripts/
```

The checked snapshot manifests match their frozen files.

## Validation

Focused tests:

```text
tests/test_project_core_run089_geometry_discrete_born_replay.py
tests/test_local_2d_new_hypothesis_candidate_pack.py
tests/test_project_core_homogeneous_dielectric_cylinder_bridge.py
tests/test_project_core_homogeneous_dielectric_bridge_alignment_diagnostic.py

12 passed
```

Full suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1121 passed in 30.19s
```

Formatting/resource checks:

```text
git diff --check: clean
RAM: 17 GiB used of 119 GiB
GPU: NVIDIA GB10, utilization 6%
```

Figure checks:

```text
run 091:      2533x716, dynamic range=255
pack 135:     2052x954, dynamic range=255
storyboard:   2286x851, dynamic range=255
```

## Current Next Branch

The marathon remains active. The next defensible branch is a CPU-only reusable
adapter contract for the run `091` grid-aware scattering operator: define the
interface items, required source/receiver/target-cell fields, scaling policy,
acceptance gate, and what must pass before any half-space or
`outputs/experiments` promotion.
