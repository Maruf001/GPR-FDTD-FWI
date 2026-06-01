# Experiment 39: Right-Rebar Noise-Seed Replication

## Goal

Replicate the Stage 4C right-rebar local x/z/r coupling result over additional
10% noise seeds.

So far:

```text
left rebar:   8/8 correct, mostly weak confidence
center rebar: 8/8 correct, all weak confidence
```

The right rebar had the strongest Stage 4C seed13 margins, so this experiment
checks whether that remains true across additional seeds.

## Decision Rule

For each seed/case:

```text
pass: true x=350 mm, z=90 mm, r=6.0 mm remains best and margin is positive
warn: true x/z/r remains best but confidence is weak
fail: another x/z/r branch wins
```

## 077_multi_rebar_right_local_geometry_noise10_seeds21_34_55

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 2 \
  --target-x-values-mm 348:352:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases "noise10_seed21:1.0,0.0,1.0,0.10,21|source_mismatch_noise10_seed21:1.1,-50.0,1.1,0.10,21|noise10_seed34:1.0,0.0,1.0,0.10,34|source_mismatch_noise10_seed34:1.1,-50.0,1.1,0.10,34|noise10_seed55:1.0,0.0,1.0,0.10,55|source_mismatch_noise10_seed55:1.1,-50.0,1.1,0.10,55" \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name multi_rebar_right_local_geometry_noise10_seeds21_34_55
```

Status:

```text
started
```

GPU check:

```text
NVIDIA GB10, FNO Python process active, GPU utilization about 87% shortly after
launch.
```

Progress:

```text
1/325 candidates, elapsed 16.0 s
25/325 candidates, elapsed 402.4 s
50/325 candidates, elapsed 805.0 s
75/325 candidates, elapsed 1207.6 s
100/325 candidates, elapsed 1610.2 s
125/325 candidates, elapsed 2012.5 s
150/325 candidates, elapsed 2414.6 s
175/325 candidates, elapsed 2816.6 s
200/325 candidates, elapsed 3218.7 s
225/325 candidates, elapsed 3621.1 s
250/325 candidates, elapsed 4023.3 s
275/325 candidates, elapsed 4425.6 s
300/325 candidates, elapsed 4827.8 s
325/325 candidates, elapsed 5230.0 s
```

Output:

```text
outputs/experiments/077_multi_rebar_right_local_geometry_noise10_seeds21_34_55
```

Case summary:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin | Relative margin | Confidence | Source profile |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| noise10_seed21 | 350.0 | 90.0 | 6.0 | 6.2 | 3.450e-04 | 0.436% | weak | fc=1.0, shift=0 ps, amp=0.997 |
| source_mismatch_noise10_seed21 | 350.0 | 90.0 | 6.0 | 6.2 | 3.184e-04 | 0.361% | weak | fc=1.1, shift=-50 ps, amp=1.097 |
| noise10_seed34 | 350.0 | 90.0 | 6.0 | 6.2 | 2.930e-04 | 0.368% | weak | fc=1.0, shift=0 ps, amp=0.998 |
| source_mismatch_noise10_seed34 | 350.0 | 90.0 | 6.0 | 6.2 | 1.947e-04 | 0.219% | weak | fc=1.1, shift=-50 ps, amp=1.098 |
| noise10_seed55 | 350.0 | 90.0 | 6.0 | 6.2 | 2.619e-04 | 0.323% | weak | fc=1.0, shift=0 ps, amp=0.995 |
| source_mismatch_noise10_seed55 | 350.0 | 90.0 | 6.0 | 6.2 | 2.825e-04 | 0.316% | weak | fc=1.1, shift=-50 ps, amp=1.101 |

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png: 1617x920 px, dynamic range 255, std 38.955
```

## 078_multi_rebar_right_seed13_21_34_55_confidence_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/069_multi_rebar_right_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/077_multi_rebar_right_local_geometry_noise10_seeds21_34_55/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_right_seed13_21_34_55_confidence_report
```

Output:

```text
outputs/experiments/078_multi_rebar_right_seed13_21_34_55_confidence_report
```

Plot validation:

```text
candidate_confidence_margins.png: 1464x903 px, dynamic range 255, std 60.606
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Cases | 8 |
| Correct x/z/r | 8 |
| Weak confidence labels | 7 |
| Moderate confidence labels | 1 |
| Strong confidence labels | 0 |
| Minimum margin | 1.947e-04 |
| Mean margin | 3.344e-04 |
| Maximum margin | 5.033e-04 |
| Minimum relative margin | 0.219% |
| Mean relative margin | 0.397% |
| Maximum relative margin | 0.593% |

## Right-Rebar Replication Decision

The right-rebar local x/z/r result is repeatable across tested 10% noise seeds:

```text
seeds 13, 21, 34, 55 all recover x=350 mm, z=90 mm, r=6.0 mm in nominal and
source-mismatched 10% noise cases.
```

Confidence remains weak:

```text
7 of 8 right cases are weak-confidence and 1 is moderate-confidence.
```

Decision:

```text
Stage 6 seed replication passes for left, center, and right rebars, but it
strongly confirms that weak-confidence reporting is mandatory. The next step
is a combined 24-case confidence synthesis and then an ambiguity interval /
fallback-reporting design before full optimizer promotion.
```
