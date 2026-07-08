# BEM Experiment 628: 128-Panel Frequency-Subset Endpoint Validator

Date: 2026-06-30

## Purpose

Validate run `627`, which tested whether the 128-panel two-dimensional CPU BEM
endpoint closes the high-frequency-only accuracy gap seen at 64 panels.

This validator checks the saved run `627` rows, summary, figure, script
snapshots, and NPZ array package. It confirms that all nine frequency subsets
pass the `1e-3` target, that the 128-panel high-band result is a real closure of
the 64-panel high-band failure, and that the result remains limited to the
two-dimensional analytic-cylinder BEM validation problem.

## Output

```text
outputs/bem_experiments/628_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validator.png
scripts/
```

## Result

```text
validation checks:                           6
failed checks:                               0
panels:                                      128
frequency subsets:                           9
frequency subsets below 1e-3:                9
frequency subsets above/equal 1e-3:          0
128-panel high-band relative L2:             0.0004276569548253307
64-panel high-band relative L2:              0.001736291511432671
high-band improvement factor versus 64:      4.060009995960033
128 panels close 64-panel high-band gap:     true
project FDTD comparison ready:               false
real 3D validation ready:                    false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

All six validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source endpoint audit ready | pass |
| 2 | frequency subset rows all pass | pass |
| 3 | high-frequency endpoint closure preserved | pass |
| 4 | saved arrays match summary hashes and errors | pass |
| 5 | claim boundary remains analytic 2D only | pass |
| 6 | figure and scripts exist | pass |

## Interpretation

Run `628` guards the run `627` endpoint result as a stable artifact. The saved
NPZ arrays match the summary hashes and error values, all nine frequency subsets
remain below the `1e-3` target, and the high-frequency-only improvement from
64 panels to 128 panels is preserved.

The operating policy remains:

```text
64 panels: default for cheaper broad/low/mid-band screening and receiver-line
studies.
128 panels: high-frequency endpoint for claims depending on the 2.08-3.00 GHz
band or on tighter accuracy.
```

This remains an analytic two-dimensional BEM result. It does not validate
project FDTD, field data, three-dimensional Maxwell modeling, GPU/HPC execution,
or field FWI.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit.py
tests/test_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validator.py

6 passed
```

Figure check:

```text
2321x867, dynamic range=255
```
