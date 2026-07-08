# Field Experiment 020: GSSI 51600S Profile Network Alignment

Date: 2026-06-17

## Purpose

CPU-only pairwise shallow-pattern alignment across all four imported local GSSI
profiles:

```text
PROJECT001C__013.DZT
PROJECT001C__014.DZT
PROJECT001C__015.DZT
PROJECT001C__016.DZT
```

Experiments 018 and 019 showed that the short profiles 014/016 repeat strongly.
This run asks whether the long profiles and short profiles form a repeat or
nested profile network, or whether the dataset remains separate 2D line-profile
evidence.

No FDTD, FWI, or GPU command was run.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/020_gssi51600s_profile_network_alignment
```

Artifacts:

```text
data/profile_network_alignment_pairs.csv
data/profile_network_alignment_lag_scan.csv
data/profile_network_alignment_summary.json
data/figure_validation.csv
figures/profile_network_alignment.png
run_manifest.json
```

## Method

The reducer re-imports all four DZT profiles, applies the existing field
preprocessing pipeline, builds a shallow-response signature from the 95th
percentile envelope cue over:

```text
0.45-1.25 ns
```

For each profile pair it scans direct and reversed orientation. Unequal-length
pairs use an embedding-style overlap correlation with at least 80% overlap of
the shorter profile.

## Result

Pairwise best alignments:

| Pair | Best orientation | Best correlation | Label |
| --- | --- | ---: | --- |
| `014` / `016` | reversed | 0.9312 | `repeat_candidate` |
| `013` / `015` | direct | 0.7244 | `repeat_candidate` |
| `014` / `015` | reversed | 0.4234 | `weak_or_unrelated` |
| `015` / `016` | direct | 0.3454 | `weak_or_unrelated` |
| `013` / `014` | reversed | 0.2495 | `weak_or_unrelated` |
| `013` / `016` | direct | 0.2221 | `weak_or_unrelated` |

Summary counts:

```text
pairs:                     6
repeat candidates:          2
embedded-segment candidates: 0
weak/unrelated pairs:       4
strongest pair:             014/016, reversed, corr=0.9312
```

## Interpretation

The field dataset contains two internally repeatable profile pairs:

```text
short pair: 014/016, strong reversed repeat
long pair:  013/015, moderate direct repeat
```

The weak long-short correlations mean the short profiles should not be treated
as clean embedded segments of the long profiles. This strengthens the current
field boundary:

```text
Use the local GSSI data as repeatability/QC and timing-calibration evidence.
Do not treat the four DZT files as a recovered 3D survey grid.
Do not report field radius, cover depth, geometry, or FWI recovery without
external survey layout and target metadata.
```

## Validation

The network figure was validated as nonblank:

```text
profile_network_alignment.png nonwhite=0.4670, dynamic range=255
```
