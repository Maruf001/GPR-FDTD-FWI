# Experiment 36: Multi-Rebar Confidence Reporting

## Goal

Convert local multi-rebar geometry profiles into decision-grade outputs:

```text
best x/z/r,
top-k ambiguity,
best-vs-next distinct-radius margin,
relative margin,
nearest competing x/z branch,
source-profile selection,
confidence label.
```

This addresses the main Stage 4C caveat: correct candidates win, but the
per-rebar radius margins are small relative to the noisy objective floor.

## Code Changes

Added:

```text
inversion/candidate_confidence.py
tests/test_candidate_confidence.py
run_candidate_confidence_report.py
```

The confidence labels are conservative:

| Label | Rule |
| --- | --- |
| strong | abs margin >= 1.0e-03 and relative margin >= 1.0e-02 |
| moderate | abs margin >= 5.0e-04 and relative margin >= 5.0e-03 |
| weak | positive but below moderate thresholds |
| ambiguous | zero/negative margin |
| missing | missing next-radius margin |

## Validation Before Report

Focused tests:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_candidate_confidence.py \
  -q
```

Result:

```text
4 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  inversion/candidate_confidence.py \
  run_candidate_confidence_report.py
```

Result:

```text
passed
```

## 070_multi_rebar_stage4c_confidence_report

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_candidate_confidence_report.py \
  outputs/experiments/067_multi_rebar_left_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/068_multi_rebar_center_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  outputs/experiments/069_multi_rebar_right_local_geometry_noise10/data/multi_rebar_local_geometry_summary.json \
  --run-name multi_rebar_stage4c_confidence_report
```

Output:

```text
outputs/experiments/070_multi_rebar_stage4c_confidence_report
```

Report artifacts:

```text
data/candidate_confidence_report.csv
data/candidate_confidence_report.json
figures/candidate_confidence_margins.png
```

Plot validation:

```text
candidate_confidence_margins.png: 1463x903 px, dynamic range 255, std 62.815
```

## Results

All Stage 4C cases select the true target geometry:

```text
left:   x=150 mm, z=90 mm, r=6.0 mm
center: x=250 mm, z=90 mm, r=6.0 mm
right:  x=350 mm, z=90 mm, r=6.0 mm
```

Confidence table:

| Target/case | Margin | Relative margin | Label | Competing x/z/r branch | Source profile |
| --- | ---: | ---: | --- | --- | --- |
| left noise10 | 2.263e-04 | 0.281% | weak | x=150, z=91, r=6.8 | fc=1.0, shift=0 ps, amp=0.998 |
| left source mismatch noise10 | 3.117e-04 | 0.348% | weak | x=150, z=91, r=6.8 | fc=1.1, shift=-50 ps, amp=1.100 |
| center noise10 | 3.194e-04 | 0.397% | weak | x=250, z=89, r=5.4 | fc=1.0, shift=0 ps, amp=0.998 |
| center source mismatch noise10 | 3.314e-04 | 0.370% | weak | x=250, z=91, r=6.8 | fc=1.1, shift=-50 ps, amp=1.100 |
| right noise10 | 4.766e-04 | 0.593% | weak | x=350, z=91, r=6.8 | fc=1.0, shift=0 ps, amp=0.998 |
| right source mismatch noise10 | 5.033e-04 | 0.562% | moderate | x=350, z=91, r=6.8 | fc=1.1, shift=-50 ps, amp=1.100 |

## Interpretation

The pipeline is now honest about uncertainty:

```text
Stage 4C recovers correct geometry and radius for all three rebars under
10% noise and source mismatch, using GPU-generated candidate profiles.
```

But:

```text
Five of six confidence labels are weak. The correct radius wins, but the
objective gap to the next radius is small.
```

The most common competing branch is:

```text
same x, 1 mm deeper z, larger r around 6.8 mm
```

This is the same physical ambiguity seen in the single-rebar work: a slightly
deeper, larger bar can mimic the best trace set closely under noise.

## Decision

The confidence/reporting layer is promoted as mandatory for future local and
multi-rebar outputs.

Next action:

```text
Run the full validation suite, then start the next GPU-backed robustness branch:
replicate Stage 4C confidence over additional noise seeds before attempting a
full 9-parameter multi-rebar optimizer.
```
