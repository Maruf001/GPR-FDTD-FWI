# Experiment 38: Center-Rebar Noise-Seed Replication

## Goal

Replicate the Stage 4C center-rebar local x/z/r coupling result over additional
10% noise seeds.

Left-rebar replication in Experiment 37 showed:

```text
8/8 cases recovered true x/z/r, but 7/8 confidence labels were weak.
```

The center rebar has neighboring rebars on both sides, so it is the next
important target before any full multi-rebar optimizer is promoted.

## Decision Rule

For each seed/case:

```text
pass: true x=250 mm, z=90 mm, r=6.0 mm remains best and margin is positive
warn: true x/z/r remains best but confidence is weak
fail: another x/z/r branch wins
```

## 075_multi_rebar_center_local_geometry_noise10_seeds21_34_55

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 1 \
  --target-x-values-mm 248:252:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases "noise10_seed21:1.0,0.0,1.0,0.10,21|source_mismatch_noise10_seed21:1.1,-50.0,1.1,0.10,21|noise10_seed34:1.0,0.0,1.0,0.10,34|source_mismatch_noise10_seed34:1.1,-50.0,1.1,0.10,34|noise10_seed55:1.0,0.0,1.0,0.10,55|source_mismatch_noise10_seed55:1.1,-50.0,1.1,0.10,55" \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name multi_rebar_center_local_geometry_noise10_seeds21_34_55
```

Status:

```text
started
```

GPU check:

```text
NVIDIA GB10, FNO Python process active, GPU utilization about 88% shortly after
launch.
```

Progress:

```text
1/325 candidates, elapsed 16.0 s
25/325 candidates, elapsed 401.5 s
50/325 candidates, elapsed 801.6 s
75/325 candidates, elapsed 1202.9 s
100/325 candidates, elapsed 1604.1 s
125/325 candidates, elapsed 2005.3 s
150/325 candidates, elapsed 2405.9 s
175/325 candidates, elapsed 2807.1 s
200/325 candidates, elapsed 3208.0 s
225/325 candidates, elapsed 3608.5 s
250/325 candidates, elapsed 4009.4 s
275/325 candidates, elapsed 4410.0 s
300/325 candidates, elapsed 4811.4 s
325/325 candidates, elapsed 5212.5 s
```

Output:

```text
outputs/experiments/075_multi_rebar_center_local_geometry_noise10_seeds21_34_55
```

Case summary:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin | Relative margin | Confidence | Source profile |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| noise10_seed21 | 250.0 | 90.0 | 6.0 | 6.2 | 2.509e-04 | 0.317% | weak | fc=1.0, shift=0 ps, amp=0.997 |
| source_mismatch_noise10_seed21 | 250.0 | 90.0 | 6.0 | 6.2 | 3.734e-04 | 0.423% | weak | fc=1.1, shift=-50 ps, amp=1.097 |
| noise10_seed34 | 250.0 | 90.0 | 6.0 | 6.2 | 3.992e-04 | 0.501% | weak | fc=1.0, shift=0 ps, amp=0.998 |
| source_mismatch_noise10_seed34 | 250.0 | 90.0 | 6.0 | 6.2 | 3.743e-04 | 0.421% | weak | fc=1.1, shift=-50 ps, amp=1.098 |
| noise10_seed55 | 250.0 | 90.0 | 6.0 | 6.2 | 3.873e-04 | 0.478% | weak | fc=1.0, shift=0 ps, amp=0.995 |
| source_mismatch_noise10_seed55 | 250.0 | 90.0 | 6.0 | 6.2 | 1.257e-04 | 0.140% | weak | fc=1.1, shift=-50 ps, amp=1.101 |

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png: 1617x920 px, dynamic range 255, std 39.142
```

## 076_multi_rebar_center_seed13_21_34_55_confidence_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/068_multi_rebar_center_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/075_multi_rebar_center_local_geometry_noise10_seeds21_34_55/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_center_seed13_21_34_55_confidence_report
```

Output:

```text
outputs/experiments/076_multi_rebar_center_seed13_21_34_55_confidence_report
```

Plot validation:

```text
candidate_confidence_margins.png: 1464x903 px, dynamic range 255, std 59.970
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Cases | 8 |
| Correct x/z/r | 8 |
| Weak confidence labels | 8 |
| Moderate confidence labels | 0 |
| Strong confidence labels | 0 |
| Minimum margin | 1.257e-04 |
| Mean margin | 3.202e-04 |
| Maximum margin | 3.992e-04 |
| Minimum relative margin | 0.140% |
| Mean relative margin | 0.381% |
| Maximum relative margin | 0.501% |

## Center-Rebar Replication Decision

The center-rebar local x/z/r result is repeatable across tested 10% noise
seeds:

```text
seeds 13, 21, 34, 55 all recover x=250 mm, z=90 mm, r=6.0 mm in nominal and
source-mismatched 10% noise cases.
```

But the confidence is weaker than the left rebar:

```text
8 of 8 center cases are weak-confidence, with one very thin source-mismatch
seed55 margin of 1.257e-04.
```

Decision:

```text
Move replication to the right rebar. Full optimizer promotion still requires
weak-confidence reporting or ambiguity intervals; center seed replication does
not justify a single unqualified radius estimate.
```
