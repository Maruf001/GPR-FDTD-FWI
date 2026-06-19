# Field Experiment 058: GSSI 51600S Long-Profile Pattern Holdout QC

Date: 2026-06-17

## Purpose

CPU-only holdout stress check for the long-profile 015/013 pattern-only
+0.06 ns shift. Field experiment 057 visualized the six stable anchors; this
run scores all eight stack-anchor candidates, including the two
repeat-limited anchors that were excluded from the claim-bearing stable set.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/058_gssi51600s_long_profile_pattern_holdout_qc
```

Artifacts:

```text
data/long_profile_pattern_holdout_qc_rows.csv
data/long_profile_pattern_holdout_qc_summary.json
data/figure_validation.csv
figures/long_profile_pattern_holdout_qc.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_pattern_holdout_qc_all_candidate_anchors_supported
```

Summary:

```text
pattern shift:                         +0.060000 ns
candidate anchors:                      8
stable anchors:                         6
stable supported anchors:               6
repeat-limited anchors:                 2
repeat-limited supported anchors:       2
minimum stable gain:                    0.019532
minimum stable shifted abs corr:        0.889509
minimum repeat-limited gain:            0.172819
minimum repeat-limited shifted abs corr: 0.961006
gpu priority:                           none
```

## Interpretation

The +0.06 ns long-profile pattern shift generalizes beyond the six stable
anchors used in the visual-QC package: both repeat-limited holdout anchors also
improve and clear the support threshold.

This strengthens the pattern-QC evidence for the 015/013 long pair, but it does
not change the claim boundary. Stable anchors remain the claim-bearing support,
and repeat-limited anchors are diagnostic holdouts only. Because profile 013
lacks phase-anchor picks, this is still not phase/time-zero calibration, 3D,
field inversion, radius, or cover-depth evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_pattern_holdout_qc.py: 3 passed
```

Figure validation:

```text
long_profile_pattern_holdout_qc.png: 1991x1209,
nonwhite=0.0996, dynamic range=255
```
