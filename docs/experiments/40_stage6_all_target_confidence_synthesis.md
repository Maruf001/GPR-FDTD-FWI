# Experiment 40: Stage 6 All-Target Confidence Synthesis

## Goal

Combine the left, center, and right multi-rebar local x/z/r seed replications
into one confidence matrix.

Inputs:

```text
left:   seeds 13, 21, 34, 55
center: seeds 13, 21, 34, 55
right:  seeds 13, 21, 34, 55
```

Each seed has:

```text
nominal 10% noise
source-mismatch 10% noise
```

Total:

```text
3 targets x 4 seeds x 2 source/noise cases = 24 cases
```

## 079_multi_rebar_stage6_all_targets_confidence_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/067_multi_rebar_left_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/071_multi_rebar_left_local_geometry_noise10_seed21/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/073_multi_rebar_left_local_geometry_noise10_seeds34_55/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/068_multi_rebar_center_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/075_multi_rebar_center_local_geometry_noise10_seeds21_34_55/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/069_multi_rebar_right_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/077_multi_rebar_right_local_geometry_noise10_seeds21_34_55/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_stage6_all_targets_confidence_report
```

Output:

```text
outputs/experiments/079_multi_rebar_stage6_all_targets_confidence_report
```

Artifacts:

```text
data/candidate_confidence_report.csv
data/candidate_confidence_report.json
figures/candidate_confidence_margins.png
```

Plot validation:

```text
candidate_confidence_margins.png: 3691x903 px, dynamic range 255, std 62.937
```

## Aggregate Results

Overall:

| Metric | Value |
| --- | ---: |
| Cases | 24 |
| Correct x/z/r | 24 |
| Weak confidence labels | 22 |
| Moderate confidence labels | 2 |
| Strong confidence labels | 0 |
| Minimum margin | 1.257e-04 |
| Mean margin | 3.394e-04 |
| Maximum margin | 5.112e-04 |
| Minimum relative margin | 0.140% |
| Mean relative margin | 0.403% |
| Maximum relative margin | 0.647% |

By target:

| Target | Cases | Correct x/z/r | Weak | Moderate | Strong | Margin min | Margin mean | Margin max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| left index 0 | 8 | 8 | 7 | 1 | 0 | 2.263e-04 | 3.635e-04 | 5.112e-04 |
| center index 1 | 8 | 8 | 8 | 0 | 0 | 1.257e-04 | 3.202e-04 | 3.992e-04 |
| right index 2 | 8 | 8 | 7 | 1 | 0 | 1.947e-04 | 3.344e-04 | 5.033e-04 |

## Interpretation

The geometry/radius selector is repeatable across this controlled synthetic
matrix:

```text
All 24 target/case rows recover the true target x, z, and radius.
```

The confidence story is the limiting factor:

```text
22 of 24 rows are weak-confidence.
No row is strong-confidence.
```

The recurring competing geometry branch is:

```text
same x, 1 mm deeper z, larger radius near 6.8 mm.
```

## Decision

Stage 6 passes as a robustness check for the local geometry/profile search:

```text
the true radius wins across left, center, and right targets for four 10% noise
seeds and source mismatch.
```

But it does not justify unqualified single-point radius reporting:

```text
future multi-rebar outputs must include confidence labels, top-k candidates,
and an ambiguity interval or fallback warning when margins are weak.
```

Next action:

```text
implement ambiguity interval reporting from the ranked candidate set before
building or promoting a full 9-parameter optimizer.
```
