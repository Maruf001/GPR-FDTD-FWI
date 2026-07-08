# BEM Experiment 626: 64-Panel Frequency-Subset Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `625` validator for the run `624` frequency-subset audit.

The important result from run `624` is a boundary, not a blanket pass: the
64-panel default passes the full, low, and mid frequency bands, but the
high-frequency-only 2.08-3.00 GHz subset exceeds the `1e-3` relative-error
target. This run checks that the validator rejects damaged artifacts that erase
that boundary or promote the result into unsupported project FDTD, field, GPU,
or three-dimensional claims.

## Output

```text
outputs/bem_experiments/626_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       25
expected pass cases:                     1
expected fail cases:                     24
actual pass cases:                       1
actual fail cases:                       24
unexpected outcomes:                     0
exact source passes:                     true
damaged cases rejected:                  true
high-band boundary damage rejected:      true
claim-promotion cases rejected:          true
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

The rejected damage cases cover:

| Group | Examples |
| --- | --- |
| Source readiness | source audit, source validator, and source sensitivity readiness set false |
| Frequency design | row removal, renamed high-band subset, zero frequency count |
| Error boundary | full-band error damage, mid-band error damage, erased high-band failure |
| Summary consistency | pass-count, fail-count, max-error, and pass/fail flag damage |
| Claim boundary | project FDTD, 3D, GPU/HPC, field-transfer, and field-FWI promotion |
| Artifact integrity | figure damage and missing script snapshots |

## Interpretation

The frequency-subset branch is now guarded by an audit, validator, and
sensitivity test. The 64-panel BEM default can be used for cheaper broad-band,
low-band, and mid-band receiver-line sweeps on this analytic-cylinder problem.
The high-frequency-only 2.08-3.00 GHz band still needs the 128-panel endpoint or
a dedicated high-frequency confirmation before it can support a standalone
accuracy claim.

This result remains limited to the two-dimensional scarep analytic-cylinder BEM
validation problem. It does not compare against the project FDTD experiments,
does not validate a three-dimensional Maxwell solver, and does not justify
field-data inversion or GPU/HPC escalation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit.py
tests/test_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2716x886, dynamic range=255
```
