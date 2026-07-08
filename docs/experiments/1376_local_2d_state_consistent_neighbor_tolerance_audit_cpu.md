# Experiment 1376: Local 2D State-Consistent Neighbor Tolerance Audit

Date: 2026-06-27

## Purpose

Quantify whether the state-consistent local 2D target recovery from runs `1374`
and `1375` requires an exact fixed-neighbor state or remains stable under small
fixed-neighbor errors.

Run `1375` showed that the corrected target state recovered the truth geometry
under six objective windows. This run keeps the same local target search and
perturbs the neighboring bars by plus or minus 1 mm in x-position and radius.

This is a bounded CPU-only local 2D experiment. It does not launch broad
batches, GPU work, field transfer, field FWI, 3D/HPC, or neural-network
training.

## Output

```text
outputs/experiments/1376_local_2d_state_consistent_neighbor_tolerance_audit_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_neighbor_tolerance_results.csv
data/local_2d_state_consistent_neighbor_tolerance_candidates.csv
data/local_2d_state_consistent_neighbor_tolerance_summary.json
figures/local_2d_state_consistent_neighbor_tolerance_audit.png
docs/LOCAL_2D_STATE_CONSISTENT_NEIGHBOR_TOLERANCE_AUDIT.md
scripts/run_local_2d_state_consistent_neighbor_tolerance_audit.py
scripts/test_local_2d_state_consistent_neighbor_tolerance_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
perturbations tested:              9
objectives tested:                 2
result rows:                       18
correct-state all objectives true: true
perturbed result rows:             16
perturbed truth-geometry rows:     16
perturbed failure rows:            0
minimum wrong-minus-truth misfit:  0.004106765164174454
neighbor tolerance supported:      true
bounded local continuation ready:  true
broad batch ready:                 false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
elapsed seconds:                   157.468
```

Perturbation outcomes:

| Perturbation | Objective | Best x mm | Best z mm | Best radius mm | Wrong minus truth misfit | Truth geometry |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| correct_state | base | 190.0 | 90.0 | 5.0 | 0.022485563942480497 | true |
| correct_state | highband | 190.0 | 90.0 | 5.0 | 0.01994705692712514 | true |
| near_neighbor_x_minus_1mm | base | 190.0 | 90.0 | 5.0 | 0.008950857267464904 | true |
| near_neighbor_x_minus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.008364060697730859 | true |
| near_neighbor_x_plus_1mm | base | 190.0 | 90.0 | 5.0 | 0.04041671882518223 | true |
| near_neighbor_x_plus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.03527471753325981 | true |
| near_neighbor_radius_minus_1mm | base | 190.0 | 90.0 | 5.0 | 0.03440052591401534 | true |
| near_neighbor_radius_minus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.029494344065706297 | true |
| near_neighbor_radius_plus_1mm | base | 190.0 | 90.0 | 5.0 | 0.016135929054836365 | true |
| near_neighbor_radius_plus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.014880379155380173 | true |
| far_neighbor_x_minus_1mm | base | 190.0 | 90.0 | 5.0 | 0.03963172658531125 | true |
| far_neighbor_x_minus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.03576136918113036 | true |
| far_neighbor_x_plus_1mm | base | 190.0 | 90.0 | 5.0 | 0.006007513873812487 | true |
| far_neighbor_x_plus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.0045159392920220455 | true |
| far_neighbor_radius_minus_1mm | base | 190.0 | 90.0 | 5.0 | 0.006343088963540772 | true |
| far_neighbor_radius_minus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.004106765164174454 | true |
| far_neighbor_radius_plus_1mm | base | 190.0 | 90.0 | 5.0 | 0.03946767397899065 | true |
| far_neighbor_radius_plus_1mm | highband | 190.0 | 90.0 | 5.0 | 0.03654163542077895 | true |

## Interpretation

The corrected local target recovery is not an exact-state-only result at the
plus or minus 1 mm level tested here. Both the base and high-band objective
windows keep selecting:

```text
x = 190 mm
z = 90 mm
radius = 5 mm
```

for every fixed-neighbor perturbation in this run.

The weakest margin occurs for the far-neighbor radius minus 1 mm case under the
high-band objective. It remains positive, so the nearest wrong target candidate
is still worse than the truth candidate.

## Decision

The state-consistent branch now has a small local tolerance band: plus or minus
1 mm fixed-neighbor x/radius errors did not flip the target recovery.

Keep the result bounded. It supports a local mechanism claim and a possible
next tolerance-radius extension, not broad local 2D batches, GPU work, or field
transfer.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_neighbor_tolerance_audit.py
sha256: e9bcaeb6a461cdae81b1d51bf23033d4304d0579a0c9839f71b7c204b8dafa30

test_local_2d_state_consistent_neighbor_tolerance_audit.py
sha256: 15be9e2b3892d554657c514d18b2e8067a659b205c21c311f188ac4ca9b43d72
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_neighbor_tolerance_audit.py
2 passed
```

Figure check:

```text
local_2d_state_consistent_neighbor_tolerance_audit.png
2356x1422, dynamic range=255
```
