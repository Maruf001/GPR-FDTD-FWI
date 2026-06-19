# Local 2D Blind-Envelope Tuning Sensitivity

## Purpose

Decompose why the two close50 nominal cases from the blind-envelope policy
stability audit are tuning-sensitive. This is a CPU-only analysis over saved
detector summary rows from runs `059` and `063`; it does not run FDTD, FWI, GPU
kernels, 3D/HPC jobs, or neural-network training.

## Output

```text
outputs/summary_tables/066_local_2d_detector_blind_envelope_tuning_sensitivity
```

Files:

```text
data/local_2d_detector_blind_envelope_tuning_sensitivity_knob_values.csv
data/local_2d_detector_blind_envelope_tuning_sensitivity_knob_effects.csv
data/local_2d_detector_blind_envelope_tuning_sensitivity_features.csv
data/local_2d_detector_blind_envelope_tuning_sensitivity_failures.csv
data/local_2d_detector_blind_envelope_tuning_sensitivity_summary.json
figures/local_2d_detector_blind_envelope_tuning_sensitivity.png
```

## Key Result

```text
policy label:                 local_2d_detector_blind_envelope_tuning_sensitivity_cpu_no_fwi
tuning-sensitive cases:       2
cases:                        target2_close50_linear29p5|seed13|nominal;
                              target2_close50_linear29p5|seed34|nominal
maximum knob effect:          1.0
top-effect case:              target2_close50_linear29p5|seed34|nominal
top-effect knob:              structural_weight
top-effect best/worst values: 0.0 / 0.8
structural best values:       seed13 nominal=0.8; seed34 nominal=0.0
support best values:          seed13 nominal=0.0; seed34 nominal=0.12
structural direction conflict: true
support direction conflict:   true
span-threshold max effect:    0.0
ready for global tuning fix:  false
ready for detector-seeded FWI: false
gpu priority:                 none
```

Interpretation: the close50 nominal fragility is not a simple global retuning
problem. The two sensitive seeds prefer conflicting structural/support-weight
directions. That makes the result useful as a detector ambiguity boundary and
as manuscript evidence against launching detector-seeded FWI from this policy.

## Validation

Focused tests:

```text
tests/test_local_2d_detector_blind_envelope_tuning_sensitivity.py
```

Figure validation:

```text
local_2d_detector_blind_envelope_tuning_sensitivity.png: 2535x903,
nonwhite=0.1182, dynamic range=255
```
