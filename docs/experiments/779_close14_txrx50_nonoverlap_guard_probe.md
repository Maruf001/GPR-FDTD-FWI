# Experiment 779: Close14 Tx/Rx50 Non-Overlap Guard Probe

Date: 2026-06-17

## Purpose

Validate the new physical-overlap guard on a meaningful synthetic 2D boundary
case instead of creating another overlapping-cylinder result. The target1 and
target2 radii are 6 mm and 8 mm, so close14 is the tangent non-overlap spacing
for this branch.

This run checks whether the existing close14 Tx/Rx50 target2 recovery remains
clean when candidate geometries that overlap any circular rebar cross-section
are skipped.

## Output

```text
outputs/experiments/1257_coordinate_optimizer_close14_seed34_sources4_txrx50_nonoverlap_objectives
```

## Setup

```text
true x values:      190, 250, 264 mm
true z values:      90, 90, 90 mm
truth radii:        5, 6, 8 mm
target index:       2
sources:            4
Tx/Rx offset:       50 mm
noise RMS:          10%
seed:               34
backend:            gpu-cpml
grid step:          1 mm
candidate grid:     105 raw local candidates
accepted candidates: 93 after non-overlap filtering
```

The command used the default-off guard:

```text
--enforce-nonoverlap-candidates
```

and evaluated both nominal 10% noise and a source-mismatch case with frequency
scale 1.1, time shift -50 ps, amplitude scale 1.1, and 10% noise.

## Result

Both cases recovered the exact tangent target2 geometry:

```text
x = 264 mm
z = 90 mm
radius = 8 mm
```

| Case | Candidate count | Best misfit | Next radius | Margin | Confidence | Ambiguity width |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| noise10_seed34 | 93 | 3.053568e-2 | 7.5 mm | 2.303891e-3 | strong | 0 mm |
| source_mismatch_noise10_seed34 | 93 | 4.944868e-2 | 7.5 mm | 4.787018e-3 | strong | 0 mm |

The base and highband diagnostic objectives both selected the exact tangent
geometry as rank 1. The nearest geometric competitor in the base objective was
the same radius shifted from x=264 mm to x=265 mm.

## Interpretation

This run confirms that the close14 Tx/Rx50 target2 branch remains clean when
the local candidate grid is constrained to physically non-overlapping circular
rebars. It also gives a concrete smoke test for the guard itself: 12 of the 105
raw local candidates were excluded, tangent contact was allowed, and the
optimizer still chose the exact geometry.

This should be cited differently from the close10/close12 results. Close14 is
the current physical tangent boundary for the 6 mm / 8 mm target1-target2
pair. Close10 and close12 remain useful algorithmic stress tests, but not
physical separated-rebar spacing claims.

## Validation

Figures were validated as nonblank:

```text
coordinate_confidence_margins.png:          nonwhite=0.3575, dynamic range=238
coordinate_objective_radius_candidates.png: nonwhite=0.0516, dynamic range=238
coordinate_radius_decision_panel.png:       nonwhite=0.2193, dynamic range=241
system_scene_geometry.png:                  nonwhite=0.7301, dynamic range=255
```

