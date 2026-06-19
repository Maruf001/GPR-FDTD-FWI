# Experiment 839: Exact-Radius Detector Seed Non-Overlap Preflight

Date: 2026-06-18

## Purpose

Audit the ten stable detector-exported coordinate seeds from run `081` under
the controlled exact-radius prior from run `089`.

This is the CPU preflight implied by the fixed-radius pilot in experiment
`838`: before launching more local optimizer runs, verify which saved seeds
are physically non-overlapping when radii are fixed to `5,6,8` mm.

## Output

```text
outputs/summary_tables/091_local_2d_detector_exact_radius_seed_nonoverlap_preflight
```

Key artifacts:

```text
data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_cases.csv
data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_pairs.csv
data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_gates.csv
data/local_2d_detector_exact_radius_seed_nonoverlap_preflight_summary.json
figures/local_2d_detector_exact_radius_seed_nonoverlap_preflight.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_exact_radius_seed_nonoverlap_preflight_cpu_no_fwi
stable seed cases:                    10
component pairs checked:              30
direct fixed-radius pilot ready:       7
overlap-blocked cases:                 3
repair-within-2mm cases:               3
minimum pair clearance:               -2.0 mm
maximum repair required:               2.0 mm
close14 direct-ready cases:            3 / 6
close50 linear29.5 direct-ready cases: 4 / 4
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Overlap-blocked seeds:

| Case | Overlap pair | Repair mm |
| --- | --- | ---: |
| `target2_close14|seed13|source_mismatch` | `1-2` | 0.584 |
| `target2_close14|seed21|nominal` | `1-2` | 2.000 |
| `target2_close14|seed34|nominal` | `1-2` | 1.000 |

## Interpretation

The controlled exact-radius route is narrower than the run `090` budget alone
suggested. Seven stable seeds can be used directly for one-case-at-a-time
fixed-radius pilots, but three close14 seeds become physically overlapping
when exact radii are imposed on the detector x/z seeds.

This explains why the nominal seed21 pilot attempt in output run `1339`
failed before simulation, while the source-mismatch seed21 pilot in output run
`1340` ran successfully. The next useful step is a CPU repair/preflight design
for the three overlap-blocked close14 seeds, not a broad GPU queue.

## Validation

```text
tests/test_local_2d_detector_exact_radius_seed_nonoverlap_preflight.py
2 passed
```

Figure validation:

```text
local_2d_detector_exact_radius_seed_nonoverlap_preflight.png: 2314x1005,
nonwhite=0.2060, dynamic range=255
```
