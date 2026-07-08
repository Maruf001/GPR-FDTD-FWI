# Experiment 1377: Local 2D State-Consistent Neighbor Tolerance Radius Ladder

Date: 2026-06-27

## Purpose

Extend the local 2D state-consistency tolerance check from run `1376`.

Run `1376` showed that plus or minus 1 mm fixed-neighbor x/radius errors did
not flip the target recovery. This run widens the perturbation ladder to plus
or minus 2 mm and plus or minus 3 mm to locate a practical tolerance boundary.

This is a bounded CPU-only local 2D experiment. It does not launch broad
batches, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/experiments/1377_local_2d_state_consistent_neighbor_tolerance_radius_ladder_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_neighbor_tolerance_radius_ladder_results.csv
data/local_2d_state_consistent_neighbor_tolerance_radius_ladder_candidates.csv
data/local_2d_state_consistent_neighbor_tolerance_radius_ladder_summary.json
figures/local_2d_state_consistent_neighbor_tolerance_radius_ladder.png
docs/LOCAL_2D_STATE_CONSISTENT_NEIGHBOR_TOLERANCE_RADIUS_LADDER.md
scripts/run_local_2d_state_consistent_neighbor_tolerance_radius_ladder.py
scripts/test_local_2d_state_consistent_neighbor_tolerance_radius_ladder.py
scripts/script_snapshot_manifest.json
```

## Result

```text
perturbations tested:               17
objectives tested:                  2
result rows:                        34
correct-state all objectives true:  true
perturbed result rows:              32
perturbed truth-geometry rows:      26
perturbed failure rows:             6
minimum wrong-minus-truth misfit:   -0.011240888041512048
wide neighbor tolerance supported:  false
tolerance boundary detected:        true
bounded local continuation ready:   true
broad batch ready:                  false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
elapsed seconds:                    289.151
```

The failures are concentrated in neighbor-radius perturbations:

| Perturbation | Objective | Selected x mm | Wrong minus truth misfit |
| --- | --- | ---: | ---: |
| near_neighbor_radius_plus_3mm | base | 188.0 | -0.005491178027970001 |
| near_neighbor_radius_plus_3mm | highband | 188.0 | -0.0017510934049712878 |
| far_neighbor_radius_minus_2mm | base | 188.0 | -0.0000372744339579012 |
| far_neighbor_radius_minus_2mm | highband | 188.0 | -0.0022434737551220996 |
| far_neighbor_radius_minus_3mm | base | 188.0 | -0.00883014626506995 |
| far_neighbor_radius_minus_3mm | highband | 188.0 | -0.011240888041512048 |

The smallest passing margins are:

| Perturbation | Objective | Selected x mm | Wrong minus truth misfit |
| --- | --- | ---: | ---: |
| near_neighbor_radius_plus_2mm | base | 190.0 | 0.0040033297797000544 |
| far_neighbor_x_plus_2mm | highband | 190.0 | 0.0045159392920220455 |
| far_neighbor_x_plus_3mm | highband | 190.0 | 0.0045159392920220455 |

## Interpretation

The plus or minus 1 mm tolerance result from run `1376` does not extend
uniformly to the wider radius ladder. Position perturbations at plus or minus
2 mm and plus or minus 3 mm kept selecting the truth target in this bounded
setup, but selected radius perturbations crossed the decision boundary.

The practical boundary is asymmetric:

```text
near-neighbor radius +2 mm: pass
near-neighbor radius +3 mm: fail
far-neighbor radius -1 mm: pass from run 1376
far-neighbor radius -2 mm: fail
far-neighbor radius -3 mm: fail
```

The far-neighbor radius minus 2 mm base-objective failure is nearly tied, but
it is still a failure because the wrong x=188 mm candidate has the lower
misfit.

## Decision

The local 2D branch now has a bounded tolerance statement:

```text
Corrected fixed-neighbor state is robust to plus or minus 1 mm perturbations.
It is not robust to all plus or minus 2 mm and plus or minus 3 mm radius
perturbations.
```

This supports a local mechanism-and-tolerance claim. It does not justify broad
local 2D batches, GPU work, or field transfer.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_neighbor_tolerance_radius_ladder.py
sha256: 9b1043a4ff90e3138f76725ac362b545c8990e0c1939feb05659040f0cc96bd4

test_local_2d_state_consistent_neighbor_tolerance_radius_ladder.py
sha256: fe93aec3ffdc2bd466ff7a8231c071da5262a3572f3caec51e1d239bc7aadd44
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_neighbor_tolerance_radius_ladder.py
2 passed
```

Figure check:

```text
local_2d_state_consistent_neighbor_tolerance_radius_ladder.png
2356x1422, dynamic range=255
```
