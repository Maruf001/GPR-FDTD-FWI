# BEM Experiment 853: 116-Panel Combined Stress Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `852` validator by applying damaged or prematurely
promoted states to the run `851` scorecard inputs.

The sensitivity set checks whether the validator rejects changes to source
readiness, row shape, panel identity, target error, guard margin, pass counts,
controlling-case identity, frequency-grid policy, project-FDTD promotion,
3D/GPU/field promotion, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/853_scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validation_sensitivity_case_rows.csv
data/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validation_sensitivity.png
scripts/
```

## Result

```text
sensitivity cases:                        18
expected pass cases:                      1
expected fail cases:                      17
actual pass cases:                        1
actual fail cases:                        17
unexpected cases:                         0
damaged cases:                            17
sensitivity ready:                        true
field transfer ready:                     false
field FWI ready:                          false
```

## Decision

The validator accepts only the exact saved scorecard state and rejects damaged
or prematurely promoted states. Use runs `851-853` as the guarded combined
frequency/receiver stress scorecard block for the analytic 116-panel 2D BEM
endpoint.

## Validation

Figure check:

```text
2861x851, dynamic range=255
```

Script snapshots:

```text
2
```
