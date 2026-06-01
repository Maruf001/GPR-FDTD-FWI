# Experiment 37: Stage 4C Noise-Seed Replication

## Goal

Replicate the Stage 4C local multi-rebar x/z/r coupling test over additional
10% noise seeds before promoting a full 9-parameter optimizer.

The first target is the left rebar because it had the weakest Stage 4C margin:

```text
left rebar, noise10_seed13 margin: 2.263e-04, confidence: weak
```

## Decision Rule

For each new seed:

```text
pass: true x/z/r remains best and margin is positive
warn: true x/z/r remains best but confidence remains weak
fail: deeper/larger or other wrong branch wins
```

If a fail appears, the next development step should be ambiguity intervals or
fallback reporting, not a single-point full optimizer.

## 071_multi_rebar_left_local_geometry_noise10_seed21

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 148:152:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases "noise10_seed21:1.0,0.0,1.0,0.10,21|source_mismatch_noise10_seed21:1.1,-50.0,1.1,0.10,21" \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name multi_rebar_left_local_geometry_noise10_seed21
```

Status:

```text
completed
```

GPU check:

```text
NVIDIA GB10, FNO Python process active, GPU utilization about 88% shortly after
launch.
```

Progress:

```text
25/325 candidates, elapsed 399.6 s
50/325 candidates, elapsed 799.3 s
75/325 candidates, elapsed 1199.0 s
100/325 candidates, elapsed 1598.4 s
125/325 candidates, elapsed 1998.2 s
150/325 candidates, elapsed 2397.8 s
175/325 candidates, elapsed 2797.1 s
200/325 candidates, elapsed 3196.8 s
225/325 candidates, elapsed 3596.7 s
250/325 candidates, elapsed 3996.8 s
275/325 candidates, elapsed 4396.8 s
300/325 candidates, elapsed 4796.6 s
325/325 candidates, elapsed 5196.2 s
```

Output:

```text
outputs/experiments/071_multi_rebar_left_local_geometry_noise10_seed21
```

Case summary:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin | Relative margin | Confidence | Source profile |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| noise10_seed21 | 150.0 | 90.0 | 6.0 | 6.2 | 5.112e-04 | 0.647% | moderate | fc=1.0, shift=0 ps, amp=0.997 |
| source_mismatch_noise10_seed21 | 150.0 | 90.0 | 6.0 | 6.2 | 3.894e-04 | 0.442% | weak | fc=1.1, shift=-50 ps, amp=1.097 |

Top candidates:

| Case | Rank | x [mm] | z [mm] | r [mm] | J |
| --- | ---: | ---: | ---: | ---: | ---: |
| noise10_seed21 | 1 | 150.0 | 90.0 | 6.0 | 7.906e-02 |
| noise10_seed21 | 2 | 150.0 | 90.0 | 6.2 | 7.957e-02 |
| noise10_seed21 | 3 | 150.0 | 91.0 | 6.8 | 7.974e-02 |
| noise10_seed21 | 4 | 150.0 | 91.0 | 6.6 | 8.004e-02 |
| source_mismatch_noise10_seed21 | 1 | 150.0 | 90.0 | 6.0 | 8.818e-02 |
| source_mismatch_noise10_seed21 | 2 | 150.0 | 90.0 | 6.2 | 8.857e-02 |
| source_mismatch_noise10_seed21 | 3 | 150.0 | 91.0 | 6.8 | 8.941e-02 |
| source_mismatch_noise10_seed21 | 4 | 150.0 | 89.0 | 5.4 | 8.962e-02 |

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png: 1617x920 px, dynamic range 255, std 31.976
```

## 072_multi_rebar_left_seed_confidence_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/067_multi_rebar_left_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/071_multi_rebar_left_local_geometry_noise10_seed21/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_left_seed_confidence_report
```

Output:

```text
outputs/experiments/072_multi_rebar_left_seed_confidence_report
```

Plot validation:

```text
candidate_confidence_margins.png: 1462x903 px, dynamic range 255, std 60.843
```

Seed comparison:

| Seed/case | Correct x/z/r? | Margin | Relative margin | Confidence |
| --- | --- | ---: | ---: | --- |
| seed13 noise10 | yes | 2.263e-04 | 0.281% | weak |
| seed13 source mismatch noise10 | yes | 3.117e-04 | 0.348% | weak |
| seed21 noise10 | yes | 5.112e-04 | 0.647% | moderate |
| seed21 source mismatch noise10 | yes | 3.894e-04 | 0.442% | weak |

## Interpretation

Seed 21 confirms the main Stage 4C result for the left rebar:

```text
true x=150 mm, z=90 mm, r=6.0 mm remains the best candidate under 10% noise
and source mismatch.
```

The confidence pattern remains cautious:

```text
one moderate case, one weak case for seed 21; both seed 13 cases were weak.
```

The common competing branch remains:

```text
same x, 1 mm deeper z, larger radius around 6.8 mm.
```

## Decision

Run more left-rebar seeds before moving to center/right replication. To avoid
wasting GPU solves, batch multiple new observed noise/source cases in one
candidate-grid run; the modeled candidate wavefields are shared across cases.

## 073_multi_rebar_left_local_geometry_noise10_seeds34_55

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_local_geometry_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --target-rebar-index 0 \
  --target-x-values-mm 148:152:1 \
  --target-z-values-mm 88:92:1 \
  --target-radius-values-mm 5.4:7.8:0.2 \
  --replication-cases "noise10_seed34:1.0,0.0,1.0,0.10,34|source_mismatch_noise10_seed34:1.1,-50.0,1.1,0.10,34|noise10_seed55:1.0,0.0,1.0,0.10,55|source_mismatch_noise10_seed55:1.1,-50.0,1.1,0.10,55" \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --progress-every 25 \
  --run-name multi_rebar_left_local_geometry_noise10_seeds34_55
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
25/325 candidates, elapsed 401.9 s
50/325 candidates, elapsed 803.4 s
75/325 candidates, elapsed 1205.0 s
100/325 candidates, elapsed 1606.6 s
125/325 candidates, elapsed 2007.5 s
150/325 candidates, elapsed 2409.1 s
175/325 candidates, elapsed 2810.8 s
200/325 candidates, elapsed 3212.7 s
225/325 candidates, elapsed 3614.2 s
250/325 candidates, elapsed 4015.5 s
275/325 candidates, elapsed 4417.2 s
300/325 candidates, elapsed 4818.7 s
325/325 candidates, elapsed 5220.0 s
```

Output:

```text
outputs/experiments/073_multi_rebar_left_local_geometry_noise10_seeds34_55
```

Case summary:

| Case | Best x [mm] | Best z [mm] | Best r [mm] | Next r [mm] | Margin | Relative margin | Confidence | Source profile |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| noise10_seed34 | 150.0 | 90.0 | 6.0 | 6.2 | 3.417e-04 | 0.429% | weak | fc=1.0, shift=0 ps, amp=0.998 |
| source_mismatch_noise10_seed34 | 150.0 | 90.0 | 6.0 | 6.2 | 4.672e-04 | 0.526% | weak | fc=1.1, shift=-50 ps, amp=1.098 |
| noise10_seed55 | 150.0 | 90.0 | 6.0 | 6.2 | 2.550e-04 | 0.315% | weak | fc=1.0, shift=0 ps, amp=0.995 |
| source_mismatch_noise10_seed55 | 150.0 | 90.0 | 6.0 | 6.2 | 4.052e-04 | 0.453% | weak | fc=1.1, shift=-50 ps, amp=1.101 |

Plot validation:

```text
multi_rebar_local_geometry_radius_profiles.png: 1617x920 px, dynamic range 255, std 36.585
```

## 074_multi_rebar_left_seed13_21_34_55_confidence_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/067_multi_rebar_left_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/071_multi_rebar_left_local_geometry_noise10_seed21/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/073_multi_rebar_left_local_geometry_noise10_seeds34_55/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_left_seed13_21_34_55_confidence_report
```

Output:

```text
outputs/experiments/074_multi_rebar_left_seed13_21_34_55_confidence_report
```

Plot validation:

```text
candidate_confidence_margins.png: 1464x903 px, dynamic range 255, std 62.696
```

Aggregate result:

| Metric | Value |
| --- | ---: |
| Cases | 8 |
| Correct x/z/r | 8 |
| Weak confidence labels | 7 |
| Moderate confidence labels | 1 |
| Strong confidence labels | 0 |
| Minimum margin | 2.263e-04 |
| Mean margin | 3.635e-04 |
| Maximum margin | 5.112e-04 |
| Minimum relative margin | 0.281% |
| Mean relative margin | 0.430% |
| Maximum relative margin | 0.647% |

## Left-Rebar Replication Decision

The left-rebar local x/z/r result is robust across the tested 10% noise seeds:

```text
seeds 13, 21, 34, 55 all recover x=150 mm, z=90 mm, r=6.0 mm in nominal and
source-mismatched 10% noise cases.
```

However, confidence remains weak:

```text
7 of 8 cases are weak-confidence, and no case is strong-confidence.
```

Decision:

```text
Move replication to the center rebar. Do not promote a single-point full
multi-rebar optimizer until center/right seed replication is also checked and
the final reporting layer can expose weak-confidence radius estimates.
```
