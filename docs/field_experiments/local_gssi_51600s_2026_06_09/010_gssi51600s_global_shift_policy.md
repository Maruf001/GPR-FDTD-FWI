# Field Experiment 010: GSSI 51600S Global Shift Policy

## Purpose

CPU-only policy analysis of the experiment 009 shift surface. Experiment 009
showed that shifted field-to-synthetic waveform correlations are high, but it
did not prove whether those shifts need to be event-specific. This run asks
whether a single global synthetic time shift can explain most of the waveform
agreement.

This run reads an existing CSV only. It does not run FDTD, FWI, or GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/010_gssi51600s_global_shift_policy
```

Artifacts:

```text
data/global_shift_summary.csv
data/global_shift_by_epsr.csv
data/global_shift_by_phase.csv
data/event_specific_best_candidates.csv
data/global_vs_event_specific_shift.csv
data/global_shift_policy_summary.json
data/figure_validation.csv
figures/global_shift_policy.png
figures/global_shift_penalty.png
run_manifest.json
```

## Result

The best shared shift is:

```text
global synthetic time shift: +0.2 ns
valid candidate rows:        18
mean |corr|:                 0.7908
min |corr|:                  0.6367
same-polarity fraction:      1.0
```

Event-specific best shifts give mean `|corr|=0.8331`, so the global-shift
penalty is modest:

```text
mean penalty: -0.0423
worst penalty: -0.1977
best penalty: 0.0000
```

The largest penalties occur in profile 016 cue-time candidates, whose
event-specific best shift is +0.1 ns rather than +0.2 ns. Most top-envelope
candidates prefer the same +0.2 ns shift as the global policy.

## Interpretation

The field waveform evidence supports a shared positive time correction, but it
does not uniquely identify event geometry, radius, or dielectric. Candidate
scores remain clustered under the global shift.

The field policy should therefore be:

```text
Use +0.2 ns as the current shared field-to-synthetic timing hypothesis.
Do not treat shifted waveform correlation as a field inversion result.
Do not run field FWI without independent geometry or cover-depth metadata.
```

## Validation

Both figures were validated as nonblank:

```text
global_shift_policy.png nonwhite=0.0785
global_shift_penalty.png nonwhite=0.3842
```

## Next Decision

The next field work, if needed, should test whether this +0.2 ns timing
correction remains stable on additional profiles or known-target measurements.
The current local profiles remain calibration/QC evidence only.
