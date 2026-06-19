# Experiment 837: Close50 Sampling Boundary Synthesis

Date: 2026-06-18

## Purpose

Consolidate the close50 target2 sampling-boundary evidence after the legacy
270/280 concern and the newer nearest-versus-linear receiver analyses. This
run reads existing saved policy outputs only. It does not run FDTD, FWI, GPU
kernels, field FWI, 3D/HPC jobs, or neural-network training.

The practical question is whether the close50 manuscript boundary should be
described as a clean sub-30 mm result, a 30 mm clean threshold, or a mixed
near-boundary caveat.

## Output

```text
outputs/experiments/1338_close50_sampling_boundary_synthesis
```

Key artifacts:

```text
data/close50_sampling_boundary_rows.csv
data/close50_sampling_boundary_synthesis_summary.json
data/figure_validation.csv
figures/close50_sampling_boundary_synthesis.png
figures/FIGURE_NOTES.md
```

Source evidence:

```text
outputs/experiments/1317_close50_legacy_270_280_policy_audit_post_28p75_seed13_replicate
outputs/experiments/1303_close50_linear29p5_three_seed_frequency_policy
outputs/experiments/1275_close50_linear_sub30_bracket_policy
outputs/experiments/1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency
```

## Result

```text
policy label:                         close50_sampling_boundary_synthesis_cpu_no_gpu
boundary rows:                         8
nearest rows:                          6
linear rows:                           2
nearest first clean replicated Tx/Rx:  30.0 mm
nearest nonclean offsets:              25,27.5,28.75 mm
nearest clean offsets:                 30,35,40 mm
nearest max nonclean below clean:      28.75 mm
linear exact-strong-not-clean offsets: 29.5,29.75 mm
linear 29.5 seed count:                3
linear 29.5 ambiguous seeds:           1
linear 29.5 ambiguous seed values:     seed13
linear 29.5 strict-clean rows:         5 / 6
legacy run270 truth fraction:          1.0
legacy run280 Tx/Rx40 truth fraction:  1.0
paper sampling boundary ready:         true
sub-30 clean threshold claim ready:    false
GPU probe ready:                       false
gpu priority:                          none
```

Boundary rows:

| Sampling | Tx/Rx mm | Rows | Truth frac | Strict clean | X ambiguous | Status | Paper role |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| linear | 29.5 | 6 | 1.000 | 5 | 1 | exact strong, not clean | sub-30 exact/strong caveat |
| linear | 29.75 | 2 | 1.000 | 1 | 1 | exact strong, not clean | single-seed sub-30 caveat |
| nearest | 25.0 | 12 | 0.333 | 0 | 12 | mixed/ambiguous | supporting boundary evidence |
| nearest | 27.5 | 4 | 1.000 | 0 | 4 | single-seed nonclean | supporting boundary evidence |
| nearest | 28.75 | 4 | 1.000 | 1 | 3 | replicated nonclean | supporting boundary evidence |
| nearest | 30.0 | 6 | 1.000 | 6 | 0 | clean replicated | paper-safe clean threshold |
| nearest | 35.0 | 6 | 1.000 | 6 | 0 | clean replicated | supporting boundary evidence |
| nearest | 40.0 | 6 | 1.000 | 6 | 0 | clean replicated | supporting boundary evidence |

## Interpretation

The legacy 270/280-style evidence was not wasted or failed. The Tx/Rx 40 mm
legacy endpoint remains clean, and the newer 28.75 mm midpoint/replicate work
is useful because it shows the transition is not simply "truth selected" versus
"truth missed." Below 30 mm, the solver can select the true geometry while
still leaving x-ambiguity or non-clean margins.

The paper-safe close50 target2 sampling statement is:

```text
Use nearest-sampled Tx/Rx 30 mm as the replicated clean threshold for the
current close50 target2 setup. Treat 28.75 mm nearest-sampled and 29.5 mm
linear-receiver evidence as sub-30 caveats, not as a clean replicated sub-30
threshold.
```

No additional close50 GPU probe is justified under the current objective. A
new run would need a new acquisition or objective hypothesis rather than just
more sampling around the already documented boundary.

## Validation

```text
tests/test_close50_sampling_boundary_synthesis.py
3 passed
```

Figure validation:

```text
close50_sampling_boundary_synthesis.png: 2399x903,
nonwhite=0.3236, dynamic range=255
```
