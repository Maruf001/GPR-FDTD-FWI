# BEM Experiment 028: Project-Core Source Injection Mode Direct-Wave Audit

Date: 2026-06-25

## Purpose

Compare several project-core FDTD source injection formulations on the
no-target direct-wave transfer gate.

Modes tested:

```text
post_soft_field
pre_soft_field
post_current_density_minus
post_current_density_plus
post_hard_field
```

The goal is to test whether the bridge blocker is simply the current
post-update soft-field source injection.

## Output

```text
outputs/bem_experiments/028_project_core_source_injection_mode_direct_wave_audit
```

Key artifacts:

```text
data/source_injection_mode_direct_wave_summary.json
data/source_injection_mode_summary.csv
data/source_injection_mode_offset_metrics.csv
data/source_injection_mode_direct_wave_arrays.npz
figures/source_injection_mode_direct_wave_summary.png
docs/SOURCE_INJECTION_MODE_DIRECT_WAVE_AUDIT.md
```

## Result

```text
pair count:                              98
selected frequency bins:                 17
best mode:                               pre_soft_field
best all-pair symmetric L2:              1.5877141638561911
best reference-offset transfer L2:       1.3021562348784914
best max per-offset symmetric L2:        0.4438290344803543
source-mode bridge ready:                false
```

Mode summary:

| Mode | All-pair L2 | Reference-transfer L2 | Max per-offset L2 |
| --- | ---: | ---: | ---: |
| post_soft_field | 1.5877541421023187 | 1.3021931375154743 | 0.4439027868440553 |
| pre_soft_field | 1.5877141638561911 | 1.3021562348784914 | 0.4438290344803543 |
| post_current_density_minus | 1.5877541421023205 | 1.3021931375154754 | 0.4439027868440554 |
| post_current_density_plus | 1.5877541421023205 | 1.3021931375154754 | 0.4439027868440554 |
| post_hard_field | 1.5383549016076972 | 1.3177369246359572 | 0.5423037386587691 |

## Interpretation

Simple injection-mode changes do not repair the bridge. Current-density-scaled
variants are equivalent after per-frequency fitting, as expected. Hard-source
injection improves the all-pair metric slightly but worsens the per-offset
metric and still fails the transfer gate.

## Decision

Do not change the project source injection based on this audit. The bridge
needs a more substantial source/receiver or scattered-field calibration
strategy.

## Validation

```text
python -m py_compile run_project_core_source_injection_mode_direct_wave_audit.py
conda run -n gpr-fdtd-fwi python run_project_core_source_injection_mode_direct_wave_audit.py
```

Figure check:

```text
1 PNG figure, nonblank dynamic range, 1816x811
```
