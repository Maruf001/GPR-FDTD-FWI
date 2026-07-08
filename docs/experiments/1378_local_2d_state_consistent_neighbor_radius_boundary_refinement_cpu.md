# Experiment 1378: Local 2D State-Consistent Neighbor Radius Boundary Refinement

Date: 2026-06-27

## Purpose

Refine the radius tolerance boundary found in run `1377`.

Run `1377` showed that the local target recovery is robust to plus or minus
1 mm fixed-neighbor perturbations, but not to all plus or minus 2 mm and plus
or minus 3 mm radius perturbations. This run narrows the two observed boundary
intervals:

```text
near-neighbor radius increase: between +2.0 mm and +3.0 mm
far-neighbor radius decrease:  between -1.0 mm and -2.0 mm
```

This is a bounded CPU-only local 2D experiment. It does not launch broad
batches, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/experiments/1378_local_2d_state_consistent_neighbor_radius_boundary_refinement_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_neighbor_radius_boundary_refinement_results.csv
data/local_2d_state_consistent_neighbor_radius_boundary_refinement_candidates.csv
data/local_2d_state_consistent_neighbor_radius_boundary_refinement_summary.json
figures/local_2d_state_consistent_neighbor_radius_boundary_refinement.png
docs/LOCAL_2D_STATE_CONSISTENT_NEIGHBOR_RADIUS_BOUNDARY_REFINEMENT.md
scripts/run_local_2d_state_consistent_neighbor_radius_boundary_refinement.py
scripts/test_local_2d_state_consistent_neighbor_radius_boundary_refinement.py
scripts/script_snapshot_manifest.json
```

## Result

```text
perturbations tested:                    11
objectives tested:                       2
result rows:                             22
correct-state all objectives true:       true
perturbed result rows:                   20
perturbed truth-geometry rows:           11
perturbed failure rows:                  9
minimum wrong-minus-truth misfit:        -0.005491178027970001
tolerance boundary detected:             true
near +radius last all-objectives pass:   +2.0 mm
near +radius first any-objective fail:   +2.25 mm
far -radius last all-objectives pass:    -1.5 mm
far -radius first any-objective fail:    -1.75 mm
broad batch ready:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
elapsed seconds:                         189.674
```

Failure rows:

| Perturbation | Objective | Selected x mm | Wrong minus truth misfit |
| --- | --- | ---: | ---: |
| near_neighbor_radius_plus_2p25mm | base | 188.0 | -0.00027061154662177955 |
| near_neighbor_radius_plus_2p50mm | base | 188.0 | -0.0024765730662480168 |
| near_neighbor_radius_plus_2p75mm | base | 188.0 | -0.0024765730662480168 |
| near_neighbor_radius_plus_3p00mm | base | 188.0 | -0.005491178027970001 |
| near_neighbor_radius_plus_3p00mm | highband | 188.0 | -0.0017510934049712878 |
| far_neighbor_radius_minus_1p75mm | base | 188.0 | -0.0000372744339579012 |
| far_neighbor_radius_minus_1p75mm | highband | 188.0 | -0.0022434737551220996 |
| far_neighbor_radius_minus_2p00mm | base | 188.0 | -0.0000372744339579012 |
| far_neighbor_radius_minus_2p00mm | highband | 188.0 | -0.0022434737551220996 |

## Interpretation

The local target recovery has a measurable radius-state tolerance, but the
boundary is not symmetric.

Near-neighbor radius overestimation:

```text
+2.0 mm:  base and high-band both pass
+2.25 mm: base fails, high-band still passes
+3.0 mm:  base and high-band both fail
```

Far-neighbor radius underestimation:

```text
-1.5 mm:  base and high-band both pass
-1.75 mm: base and high-band both fail
-2.0 mm:  base and high-band both fail
```

The wrong geometry selected by every failure is:

```text
x = 188 mm
z = 90 mm
radius = 5 mm
```

## Decision

The state-consistent local 2D branch now has a bounded radius tolerance
statement:

```text
The corrected target recovery is stable through near-neighbor radius +2.0 mm
and far-neighbor radius -1.5 mm. It begins failing at near-neighbor +2.25 mm
for the base objective and at far-neighbor -1.75 mm for both tested objectives.
```

This is a local mechanism-and-tolerance result. It does not justify broad local
2D batches, GPU work, field transfer, or field FWI.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_neighbor_radius_boundary_refinement.py
sha256: ed05a9bb5131fe9f2807be8d40123e35609fe2a95eb0ca3b2830f8a23406ca87

test_local_2d_state_consistent_neighbor_radius_boundary_refinement.py
sha256: 0ddb0e301263f69a26b911402adf47c1a0925b773bdda545bcad50a1a03d77eb
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_neighbor_radius_boundary_refinement.py
2 passed
```

Figure check:

```text
local_2d_state_consistent_neighbor_radius_boundary_refinement.png
2356x1421, dynamic range=255
```
